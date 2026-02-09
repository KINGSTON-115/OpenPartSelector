"""
API 模块 - FastAPI Web 服务
"""
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uuid
import logging

logger = logging.getLogger(__name__)


# ==================== 数据模型 ====================

class SelectRequest(BaseModel):
    """选型请求"""
    query: str = Field(..., description="自然语言查询")
    constraints: Optional[Dict] = None
    top_k: int = Field(default=5, ge=1, le=20)
    model: Optional[str] = None


class SelectResponse(BaseModel):
    """选型响应"""
    request_id: str
    query: str
    results: List[Dict]
    analysis: str
    bom: Optional[Dict] = None


class PriceRequest(BaseModel):
    """比价请求"""
    part_number: str
    quantity: int = Field(default=1, ge=1)


class PriceResponse(BaseModel):
    """比价响应"""
    part_number: str
    prices: List[Dict]
    best_option: Dict


class DatasheetParseRequest(BaseModel):
    """Datasheet 解析请求"""
    url: Optional[str] = None
    content: Optional[str] = None


class DatasheetParseResponse(BaseModel):
    """Datasheet 解析响应"""
    part_number: Optional[str]
    parameters: Dict
    summary: str


class BomGenerateRequest(BaseModel):
    """BOM 生成请求"""
    parts: List[str]
    quantities: Optional[List[int]] = None


class BomResponse(BaseModel):
    """BOM 响应"""
    bom_id: str
    items: List[Dict]
    total_cost: float


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    components: Dict


# ==================== FastAPI 应用 ====================

def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="OpenPartSelector API",
        description="AI-Driven Electronic Component Selection Engine API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 内存存储 (生产环境请使用数据库)
    bom_storage: Dict[str, Dict] = {}
    
    # ==================== 端点 ====================
    
    @app.get("/", tags=["Root"])
    async def root():
        """根路径"""
        return {
            "name": "OpenPartSelector API",
            "version": "0.1.0",
            "docs": "/docs"
        }
    
    @app.get("/health", response_model=HealthResponse, tags=["System"])
    async def health_check():
        """健康检查"""
        return HealthResponse(
            status="healthy",
            version="0.1.0",
            components={
                "api": "ok",
                "llm": "ready",
                "search": "ready"
            }
        )
    
    @app.post("/api/v1/select", response_model=SelectResponse, tags=["Selection"])
    async def select_component(request: SelectRequest):
        """
        元器件选型查询
        
        使用自然语言描述需求，AI 自动推荐合适的元器件。
        """
        import asyncio
        from ops.config import Config
        from ops.agent import Agent
        
        try:
            config = Config.load()
            agent = Agent(config)
            
            result = await agent.select(
                query=request.query,
                constraints=request.constraints,
                top_k=request.top_k
            )
            
            return SelectResponse(
                request_id=str(uuid.uuid4())[:8],
                query=request.query,
                results=[{
                    "part_number": r.part_number,
                    "description": r.description,
                    "manufacturer": r.manufacturer,
                    "specs": {
                        "voltage": r.specs.voltage,
                        "current": r.specs.current,
                        "package": r.specs.package
                    },
                    "price": r.price,
                    "compatibility_score": r.compatibility_score
                } for r in result.recommended_parts],
                analysis=result.analysis_report,
                bom={"items": result.bom_items}
            )
        except Exception as e:
            logger.error(f"Selection error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/v1/price/{part_number}", response_model=PriceResponse, tags=["Pricing"])
    async def get_price(part_number: str, quantity: int = 1):
        """
        获取元器件价格
        
        查询多个平台的价格和库存信息。
        """
        try:
            from ops.config import Config
            from ops.search import SearchEngine
            
            config = Config.load()
            engine = SearchEngine(config)
            await engine.initialize()
            
            prices = await engine.compare_prices(part_number)
            
            return PriceResponse(
                part_number=part_number,
                prices=prices.get("prices", []),
                best_option=prices.get("best_price", {})
            )
        except Exception as e:
            logger.error(f"Price error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/v1/parse/datasheet", response_model=DatasheetParseResponse, tags=["Parsing"])
    async def parse_datasheet(request: DatasheetParseRequest):
        """
        解析 Datasheet
        
        提取关键参数并生成通俗易懂的摘要。
        """
        try:
            from ops.config import Config
            from ops.parser import DatasheetParser
            
            config = Config.load()
            parser = DatasheetParser(config)
            
            if request.url:
                result = await parser.parse_url(request.url)
            elif request.content:
                result = await parser.parse_text(request.content)
            else:
                raise HTTPException(status_code=400, detail="url or content required")
            
            summary = await parser.generate_summary(result)
            
            return DatasheetParseResponse(
                part_number=result.get("part_number"),
                parameters=result.get("parameters", {}),
                summary=summary
            )
        except Exception as e:
            logger.error(f"Parse error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/v1/bom/generate", response_model=BomResponse, tags=["BOM"])
    async def generate_bom(request: BomGenerateRequest):
        """
        生成 BOM 清单
        
        根据元器件列表生成采购清单。
        """
        from ops.utils import BomBuilder
        
        bom_id = str(uuid.uuid4())[:8]
        builder = BomBuilder()
        
        for i, part in enumerate(request.parts):
            qty = request.quantities[i] if request.quantities and i < len(request.quantities) else 1
            builder.add_item(part_number=part, quantity=qty)
        
        bom = builder.get_bom()
        bom_storage[bom_id] = bom
        
        return BomResponse(
            bom_id=bom_id,
            items=bom["items"],
            total_cost=bom["total_estimated_cost"]
        )
    
    @app.get("/api/v1/bom/{bom_id}", tags=["BOM"])
    async def get_bom(bom_id: str):
        """获取已生成的 BOM"""
        if bom_id not in bom_storage:
            raise HTTPException(status_code=404, detail="BOM not found")
        return bom_storage[bom_id]
    
    @app.get("/api/v1/search", tags=["Search"])
    async def search(
        q: str,
        category: Optional[str] = None,
        limit: int = 10
    ):
        """
        搜索元器件
        
        在知识库中搜索匹配的元器件。
        """
        try:
            from ops.config import Config
            from ops.knowledge import VectorStore
            
            config = Config.load()
            store = VectorStore(config)
            await store.initialize()
            
            results = await store.search(q, limit=limit)
            return {"results": results}
        except Exception as e:
            logger.error(f"Search error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
