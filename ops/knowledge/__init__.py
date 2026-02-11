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
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat() + "Z"
    
    async def create_embeddings(self, model: str = "text-embedding-3-small"):
        """
        创建向量嵌入

        Args:
            model: 嵌入模型名称
        """
        logger.info(f"Creating embeddings with model: {model}")

        # 简单实现：使用 TF-IDF 风格的文本特征作为向量
        for part_number, data in self.index.items():
            if data.get("embeddings") is None:
                # 使用文本内容生成简单向量表示
                text_content = json.dumps(data.get("data", {}), ensure_ascii=False)
                embedding = self._generate_text_embedding(text_content)
                data["embeddings"] = embedding
                logger.debug(f"Generated embedding for {part_number}")

        await self.save_index()
        logger.info(f"Created embeddings for {len(self.index)} parts")

    def _generate_text_embedding(self, text: str) -> List[float]:
        """
        生成文本的简单向量表示 (TF-IDF 风格)

        Args:
            text: 输入文本

        Returns:
            嵌入向量
        """
        import hashlib

        # 使用词汇表生成固定维度的向量
        vocabulary = [
            "arduino", "raspberry", "esp32", "stm32", "arduino", "sensor",
            "voltage", "current", "power", "digital", "analog", "wireless",
            "bluetooth", "wifi", "i2c", "spi", "uart", "gpio", "pwm",
            "led", "motor", "display", "oled", "lcd", "touch", "audio",
            "battery", "charger", "ldo", "dc-dc", "amplifier", "amplify",
            "memory", "flash", "eeprom", "secure", "crypto", "wireless",
            "rf", "lora", "nbiot", "gps", "gprs", "4g", "5g", "usb",
            "can", "rs485", "ethernet", "usb-c", "hdmi", "mipi", "dvp",
            "camera", "vision", "ai", "machine", "learning", "neural"
        ]

        # 生成 64 维向量
        vector_dim = 64
        vector = [0.0] * vector_dim

        text_lower = text.lower()
        words = set(text_lower.split())

        for i, vocab_word in enumerate(vocabulary[:vector_dim]):
            if vocab_word in text_lower:
                # 多次出现增加权重
                count = text_lower.count(vocab_word)
                vector[i] = min(1.0, 0.1 + 0.1 * count)

        # 如果向量全为0，添加基于文本哈希的特征
        if all(v == 0.0 for v in vector):
            hash_val = int(hashlib.md5(text_lower.encode()).hexdigest(), 16)
            for i in range(min(8, vector_dim)):
                vector[i] = ((hash_val >> (i * 4)) & 0xF) / 15.0

        return vector

    async def semantic_search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        语义搜索 (使用向量相似度)

        Args:
            query: 查询文本
            top_k: 返回前 k 个结果

        Returns:
            按相似度排序的结果
        """
        query_embedding = self._generate_text_embedding(query)

        results = []
        for part_number, data in self.index.items():
            embeddings = data.get("embeddings")
            if embeddings:
                similarity = self._cosine_similarity(query_embedding, embeddings)
                results.append({
                    **data,
                    "similarity": similarity
                })

        # 按相似度排序
        results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        计算余弦相似度

        Args:
            vec_a: 向量 A
            vec_b: 向量 B

        Returns:
            余弦相似度 (0-1)
        """
        if not vec_a or not vec_b:
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        magnitude_a = sum(a * a for a in vec_a) ** 0.5
        magnitude_b = sum(b * b for b in vec_b) ** 0.5

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)
