"""
知识库模块 - 向量存储与语义搜索
"""
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
import json

from ..config import Config

logger = logging.getLogger(__name__)


class VectorStore:
    """向量知识库"""
    
    def __init__(self, config: Config):
        self.config = config
        self.store_path = Path(config.vector_store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        self.index = {}  # 简单索引: part_number -> data
        self._initialized = False
    
    async def initialize(self):
        """初始化知识库"""
        await self._load_index()
        self._initialized = True
        logger.info(f"Vector store initialized with {len(self.index)} items")
    
    async def _load_index(self):
        """加载本地索引"""
        index_file = self.store_path / "index.json"
        
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
    
    async def save_index(self):
        """保存索引"""
        index_file = self.store_path / "index.json"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    async def add_datasheet(self, part_number: str, data: Dict):
        """
        添加 datasheet 到知识库
        
        Args:
            part_number: 元器件型号
            data: datasheet 解析数据
        """
        self.index[part_number.upper()] = {
            "part_number": part_number.upper(),
            "data": data,
            "embeddings": None,  # TODO: 添加向量嵌入
            "added_at": self._timestamp(),
        }
        
        await self.save_index()
        logger.info(f"Added {part_number} to knowledge base")
    
    async def search(
        self, 
        query: str, 
        filters: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        语义搜索
        
        Args:
            query: 搜索查询
            filters: 过滤条件
            limit: 返回数量
            
        Returns:
            匹配的元器件列表
        """
        results = []
        query_lower = query.lower()
        
        # 简单关键词搜索
        for part_number, data in self.index.items():
            content = json.dumps(data, ensure_ascii=False).lower()
            
            # 计算相关性分数
            score = self._calculate_relevance(query_lower, content)
            
            if score > 0:
                # 应用过滤器
                if filters:
                    if not self._matches_filters(data, filters):
                        continue
                
                results.append({
                    **data,
                    "relevance_score": score
                })
        
        # 排序
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """计算相关性分数"""
        score = 0.0
        
        # 分词查询
        keywords = query.split()
        for keyword in keywords:
            if len(keyword) < 2:
                continue
            
            if keyword in content:
                score += 0.1
        
        # 完整匹配
        if query in content:
            score += 0.5
        
        return min(score, 1.0)
    
    def _matches_filters(self, data: Dict, filters: Dict) -> bool:
        """检查是否匹配过滤器"""
        for key, value in filters.items():
            if key == "category":
                if data.get("category", "").lower() != value.lower():
                    return False
            elif key == "voltage":
                if value.lower() not in data.get("voltage", "").lower():
                    return False
            elif key == "package":
                if value.lower() not in data.get("package", "").lower():
                    return False
        
        return True
    
    async def get_part(self, part_number: str) -> Optional[Dict]:
        """获取特定元器件信息"""
        return self.index.get(part_number.upper())
    
    async def delete_part(self, part_number: str) -> bool:
        """删除元器件"""
        key = part_number.upper()
        
        if key in self.index:
            del self.index[key]
            await self.save_index()
            return True
        
        return False
    
    async def bulk_import(self, parts: List[Dict]):
        """批量导入"""
        for part in parts:
            part_number = part.get("part_number")
            if part_number:
                await self.add_datasheet(part_number, part)
        
        logger.info(f"Bulk imported {len(parts)} parts")
    
    def _timestamp(self) -> str:
        """生成时间戳"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
    
    async def create_embeddings(self, model: str = "text-embedding-3-small"):
        """
        创建向量嵌入
        
        TODO: 集成 OpenAI/HuggingFace embeddings
        """
        logger.info(f"Creating embeddings with model: {model}")
        # TODO: 实现嵌入逻辑
