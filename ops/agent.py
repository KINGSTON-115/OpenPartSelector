"""
AI Agent 主模块 - 基于多 Agent 协作的选型引擎
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import logging

from .config import Config
from .search import SearchEngine
from .parser import DatasheetParser
from .knowledge import VectorStore

logger = logging.getLogger(__name__)


class PartCategory(Enum):
    """元器件分类"""
    POWER = "power"
    MCU = "mcu"
    SENSOR = "sensor"
    INTERFACE = "interface"
    ANALOG = "analog"
    DISCRETE = "discrete"
    PASSIVE = "passive"
    UNKNOWN = "unknown"


@dataclass
class PartSpec:
    """元器件规格"""
    voltage: Optional[str] = None
    current: Optional[str] = None
    power: Optional[str] = None
    package: Optional[str] = None
    temperature: Optional[str] = None
    speed: Optional[str] = None
    interface: Optional[str] = None
    additional: Dict[str, str] = field(default_factory=dict)


@dataclass  
class SearchResult:
    """搜索结果"""
    part_number: str
    description: str
    manufacturer: str
    category: str
    specs: PartSpec
    price: Optional[float] = None
    stock: Optional[int] = None
    vendors: List[Dict] = field(default_factory=list)
    datasheet_url: Optional[str] = None
    compatibility_score: float = 0.0
    matched_constraints: List[str] = field(default_factory=list)


@dataclass
class SelectionResult:
    """选型结果"""
    query: str
    recommended_parts: List[SearchResult]
    analysis_report: str
    compatibility_warnings: List[str]
    bom_items: List[Dict]
    generated_at: str


class Agent:
    """
    主选型 Agent
    
    负责协调搜索、分析、比较 Agent 完成选型任务
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.load()
        self.search_engine = SearchEngine(self.config)
        self.datasheet_parser = DatasheetParser(self.config)
        self.knowledge_base = VectorStore(self.config)
        
        # 各子 Agent 状态
        self._initialized = False
    
    async def initialize(self):
        """初始化 Agent"""
        await self.search_engine.initialize()
        await self.knowledge_base.initialize()
        self._initialized = True
        logger.info("Agent initialized successfully")
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        解析自然语言查询
        
        Args:
            query: 自然语言描述，如"为 ESP32 项目找一个 3.3V LDO"
            
        Returns:
            解析后的结构化查询
        """
        # TODO: 使用 LLM 解析查询意图
        parsed = {
            "original_query": query,
            "keywords": [],
            "constraints": {},
            "category_hint": None,
            "target_voltage": None,
            "target_package": None,
        }
        
        # 简单关键词提取
        keywords = query.lower().split()
        
        # 电压提取
        voltage_keywords = ["3.3v", "5v", "12v", "24v", "1.8v"]
        for kw in keywords:
            if kw in voltage_keywords:
                parsed["target_voltage"] = kw.upper()
                break
        
        # 封装提取
        package_keywords = ["sop-8", "sop-16", "qfn", "bga", "dip", "soic", "0402", "0603"]
        for kw in keywords:
            if kw.lower() in package_keywords:
                parsed["target_package"] = kw.upper()
                break
        
        # 分类推断
        category_keywords = {
            PartCategory.POWER: ["ldo", "dc-dc", "电源", "电压", "buck", "boost"],
            PartCategory.MCU: ["mcu", "单片机", "微控制器", "stm32", "esp32", "arduino"],
            PartCategory.SENSOR: ["传感器", "sensor", "温度", "湿度", "加速度"],
            PartCategory.INTERFACE: ["usb", "uart", "i2c", "spi", "以太网", "接口"],
            PartCategory.ANALOG: ["运放", "opamp", "adc", "dac", "放大"],
        }
        
        for category, cats in category_keywords.items():
            if any(kw in query.lower() for kw in cats):
                parsed["category_hint"] = category.value
                break
        
        return parsed
    
    async def select(
        self, 
        query: str, 
        constraints: Optional[Dict] = None,
        top_k: int = 5
    ) -> SelectionResult:
        """
        主选型接口
        
        Args:
            query: 自然语言选型需求
            constraints: 额外约束条件
            top_k: 返回前 N 个推荐
            
        Returns:
            SelectionResult: 选型结果
        """
        if not self._initialized:
            await self.initialize()
        
        # 1. 解析查询
        parsed_query = self.parse_query(query)
        if constraints:
            parsed_query["constraints"].update(constraints)
        
        logger.info(f"Parsed query: {json.dumps(parsed_query, ensure_ascii=False)}")
        
        # 2. 搜索候选元器件
        candidates = await self.search_engine.search(
            query=query,
            category=parsed_query.get("category_hint"),
            constraints=parsed_query.get("constraints", {}),
            limit=top_k * 3  # 多搜索一些以便筛选
        )
        
        # 3. 分析与排序
        results = await self._analyze_and_rank(candidates, parsed_query)
        
        # 4. 生成分析报告
        report = await self._generate_report(results, query)
        
        # 5. 生成 BOM
        bom = self._generate_bom(results[:top_k])
        
        return SelectionResult(
            query=query,
            recommended_parts=results[:top_k],
            analysis_report=report,
            compatibility_warnings=self._check_compatibility(results[:top_k], parsed_query),
            bom_items=bom,
            generated_at=self._timestamp()
        )
    
    async def _analyze_and_rank(
        self, 
        candidates: List[Dict], 
        query: Dict
    ) -> List[SearchResult]:
        """分析并排序候选元器件"""
        results = []
        
        for candidate in candidates:
            result = SearchResult(
                part_number=candidate.get("part_number", ""),
                description=candidate.get("description", ""),
                manufacturer=candidate.get("manufacturer", ""),
                category=candidate.get("category", ""),
                specs=self._parse_specs(candidate),
                price=candidate.get("price"),
                stock=candidate.get("stock"),
                vendors=candidate.get("vendors", []),
                datasheet_url=candidate.get("datasheet_url"),
            )
            
            # 计算兼容性分数
            result.compatibility_score = self._calculate_compatibility(result, query)
            result.matched_constraints = self._find_matched_constraints(result, query)
            
            results.append(result)
        
        # 按分数排序
        results.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        return results
    
    def _parse_specs(self, data: Dict) -> PartSpec:
        """解析规格数据"""
        return PartSpec(
            voltage=data.get("voltage"),
            current=data.get("current"),
            power=data.get("power"),
            package=data.get("package"),
            temperature=data.get("temperature"),
            speed=data.get("speed"),
            interface=data.get("interface"),
            additional={k: v for k, v in data.items() 
                       if k not in ["part_number", "description", "manufacturer", 
                                   "category", "price", "stock", "vendors", "datasheet_url"]}
        )
    
    def _calculate_compatibility(self, result: SearchResult, query: Dict) -> float:
        """计算兼容性分数"""
        score = 0.5  # 基础分
        
        constraints = query.get("constraints", {})
        
        # 电压匹配
        if result.specs.voltage and query.get("target_voltage"):
            if result.specs.voltage.upper() == query["target_voltage"].upper():
                score += 0.2
            elif result.specs.voltage.upper() in query["target_voltage"].upper():
                score += 0.1
        
        # 封装匹配
        if result.specs.package and query.get("target_package"):
            if result.specs.package.upper() == query["target_package"].upper():
                score += 0.2
        
        # 库存充足
        if result.stock and result.stock > 1000:
            score += 0.1
        
        return min(score, 1.0)
    
    def _find_matched_constraints(self, result: SearchResult, query: Dict) -> List[str]:
        """找出匹配的约束条件"""
        matched = []
        
        if result.specs.voltage and query.get("target_voltage"):
            if result.specs.voltage.upper() == query["target_voltage"].upper():
                matched.append(f"电压: {result.specs.voltage}")
        
        if result.specs.package and query.get("target_package"):
            if result.specs.package.upper() == query["target_package"].upper():
                matched.append(f"封装: {result.specs.package}")
        
        return matched
    
    async def _generate_report(self, results: List[SearchResult], query: str) -> str:
        """生成选型分析报告"""
        # TODO: 使用 LLM 生成详细报告
        report_lines = [
            f"## 选型报告",
            f"",
            f"**查询需求**: {query}",
            f"",
            f"**推荐元器件数量**: {len(results)}",
            f"",
        ]
        
        for i, result in enumerate(results[:3], 1):
            report_lines.extend([
                f"### {i}. {result.part_number}",
                f"- **厂商**: {result.manufacturer}",
                f"- **描述**: {result.description}",
                f"- **价格**: ${result.price}" if result.price else "- **价格**: 待查询",
                f"- **库存**: {result.stock}" if result.stock else "- **库存**: 待查询",
                f"- **兼容性分数**: {result.compatibility_score:.0%}",
            ])
        
        return "\n".join(report_lines)
    
    def _check_compatibility(self, results: List[SearchResult], query: Dict) -> List[str]:
        """检查兼容性问题"""
        warnings = []
        
        # TODO: 完善兼容性检查逻辑
        
        return warnings
    
    def _generate_bom(self, results: List[SearchResult]) -> List[Dict]:
        """生成 BOM 清单"""
        bom = []
        
        for result in results:
            bom.append({
                "part_number": result.part_number,
                "manufacturer": result.manufacturer,
                "quantity": 1,
                "reference": f"U{len(bom) + 1}",
                "description": result.description,
                "price_estimate": result.price,
            })
        
        return bom
    
    def _timestamp(self) -> str:
        """生成时间戳"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"


# 便捷函数
def create_agent(config_path: Optional[str] = None) -> Agent:
    """创建 Agent 实例"""
    config = Config.load(config_path)
    return Agent(config)
