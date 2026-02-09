"""
搜索引擎模块 - 多平台集成 + 内置数据库
"""
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
import logging
import asyncio

from ..config import Config
from .. import database

logger = logging.getLogger(__name__)


class BaseSearchEngine(ABC):
    """搜索基类"""
    
    def __init__(self, config: Config):
        self.config = config
    
    @abstractmethod
    async def search(
        self, 
        query: str, 
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """执行搜索"""
        pass
    
    @abstractmethod
    async def get_price_and_stock(self, part_number: str) -> Dict:
        """获取价格和库存"""
        pass


class BuiltinDatabaseEngine(BaseSearchEngine):
    """内置数据库搜索引擎 (离线/演示用)"""
    
    def __init__(self, config: Config):
        super().__init__(config)
    
    async def search(
        self, 
        query: str, 
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """内置数据库搜索"""
        results = database.search_components(
            query=query,
            category=category,
            constraints=constraints,
            limit=limit
        )
        
        logger.info(f"Builtin DB search for '{query}': {len(results)} results")
        return results
    
    async def get_price_and_stock(self, part_number: str) -> Dict:
        """获取价格和库存"""
        return database.get_price_comparison(part_number)


class DigiKeyEngine(BaseSearchEngine):
    """DigiKey 搜索"""
    
    BASE_URL = "https://api.digikey.com"
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.api_keys.digikey
    
    async def search(
        self, 
        query: str, 
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """DigiKey 搜索"""
        if not self.api_key:
            logger.warning("DigiKey API key not configured, using built-in DB")
            builtin = BuiltinDatabaseEngine(self.config)
            return await builtin.search(query, category, constraints, limit)
        
        # TODO: 实现 DigiKey API 调用
        logger.info(f"DigiKey search for '{query}' (API not implemented yet)")
        return []
    
    async def get_price_and_stock(self, part_number: str) -> Dict:
        """获取价格和库存"""
        if not self.api_key:
            builtin = BuiltinDatabaseEngine(self.config)
            return await builtin.get_price_and_stock(part_number)
        
        return {"part_number": part_number, "stock": 0, "price": 0.0}


class MouserEngine(BaseSearchEngine):
    """Mouser 搜索"""
    
    BASE_URL = "https://api.mouser.com"
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.api_keys.mouser
    
    async def search(
        self, 
        query: str, 
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Mouser 搜索"""
        if not self.api_key:
            logger.warning("Mouser API key not configured")
            builtin = BuiltinDatabaseEngine(self.config)
            return await builtin.search(query, category, constraints, limit)
        
        return []
    
    async def get_price_and_stock(self, part_number: str) -> Dict:
        if not self.api_key:
            builtin = BuiltinDatabaseEngine(self.config)
            return await builtin.get_price_and_stock(part_number)
        return {"stock": 0, "price": 0.0}


class LCSCEngine(BaseSearchEngine):
    """LCSC 立创搜索"""
    
    BASE_URL = "https://api.lcsc.com"
    
    def __init__(self, config: Config):
        super().__init__(config)
    
    async def search(
        self, 
        query: str, 
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """LCSC 搜索"""
        # 内置数据库已包含 LCSC 数据
        builtin = BuiltinDatabaseEngine(self.config)
        return await builtin.search(query, category, constraints, limit)
    
    async def get_price_and_stock(self, part_number: str) -> Dict:
        return database.get_price_comparison(part_number)


class OctopartEngine(BaseSearchEngine):
    """Octopart 跨平台比价"""
    
    BASE_URL = "https://api.octopart.com"
    
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.api_keys.octopart
    
    async def search(
        self, 
        query: str, 
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Octopart 搜索"""
        # 使用内置数据库
        builtin = BuiltinDatabaseEngine(self.config)
        return await builtin.search(query, category, constraints, limit)
    
    async def get_price_and_stock(self, part_number: str) -> Dict:
        return database.get_price_comparison(part_number)


class SearchEngine:
    """统一搜索入口"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # 初始化各平台引擎
        self.engines = {
            "builtin": BuiltinDatabaseEngine(config),
            "digikey": DigiKeyEngine(config),
            "mouser": MouserEngine(config),
            "lcsc": LCSCEngine(config),
            "octopart": OctopartEngine(config),
        }
        
        self._initialized = True
    
    async def search(
        self, 
        query: str, 
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10,
        platforms: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        统一搜索接口
        
        默认优先使用内置数据库，结果不足时尝试各平台
        """
        if platforms is None:
            platforms = ["builtin"]  # 默认使用内置数据库
        
        results = []
        
        for platform in platforms:
            if platform in self.engines:
                try:
                    platform_results = await self.engines[platform].search(
                        query=query,
                        category=category,
                        constraints=constraints,
                        limit=limit
                    )
                    
                    for result in platform_results:
                        result["source"] = platform
                        results.append(result)
                        
                except Exception as e:
                    logger.error(f"Search failed on {platform}: {e}")
        
        # 去重
        seen = set()
        unique_results = []
        for result in results:
            key = result.get("part_number", "").upper()
            if key and key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        return unique_results[:limit]
    
    async def compare_prices(self, part_number: str) -> Dict:
        """比价查询"""
        all_prices = []
        best_price = None
        
        for engine in self.engines.values():
            try:
                price_info = await engine.get_price_and_stock(part_number)
                if "prices" in price_info:
                    all_prices.extend(price_info["prices"])
                elif price_info.get("price", 0) > 0:
                    all_prices.append({
                        "vendor": "unknown",
                        "price": price_info["price"],
                        "stock": price_info.get("stock", 0)
                    })
            except Exception as e:
                logger.error(f"Price compare failed: {e}")
        
        if all_prices:
            best_price = min(all_prices, key=lambda x: x.get("price", float("inf")))
        
        return {
            "part_number": part_number,
            "prices": all_prices,
            "best_vendor": best_price.get("vendor") if best_price else None,
            "best_price": best_price.get("price") if best_price else None,
            "total_stock": sum(p.get("stock", 0) for p in all_prices)
        }
    
    async def get_alternatives(self, part_number: str) -> List[Dict]:
        """获取替代料"""
        return database.get_alternatives(part_number)
