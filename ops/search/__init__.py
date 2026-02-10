"""
🔍 多平台搜索引擎
Multi-Source Search Engine

支持:
- 内置数据库搜索
- Web API 搜索 (Octopart, Digi-Key, Mouser)
- 智能匹配与排序
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from ..config import Config
from ..database import search_components as db_search, get_price_comparison as db_get_price

# 导入 agent.py 中定义的 SearchResult，避免重复定义
from ..agent import SearchResult as AgentSearchResult


class SearchEngine:
    """多平台搜索引擎"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config.load()
        self.api_keys = {
            "octopart": self.config.api_keys.octopart,
            "digikey": self.config.api_keys.digikey,
            "mouser": self.config.api_keys.mouser,
        }
    
    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        constraints: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        综合搜索
        
        Args:
            query: 搜索关键词
            category: 器件分类
            constraints: 约束条件
            limit: 结果数量
            
        Returns:
            搜索结果列表
        """
        # 1. 首先搜索内置数据库
        db_results = await self._search_database(query, category, constraints, limit)
        
        # 2. 如果有 API Key，尝试在线搜索
        if self.api_keys["octopart"]:
            api_results = await self._search_octopart(query, constraints, limit)
            # 合并结果
            return self._merge_results(db_results, api_results)
        
        return db_results
    
    async def _search_database(
        self,
        query: str,
        category: Optional[str],
        constraints: Optional[Dict],
        limit: int
    ) -> List[Dict]:
        """搜索内置数据库"""
        try:
            results = db_search(query, category=category, limit=limit)
            for r in results:
                r["source"] = "database"
                r["score"] = self._calculate_score(r, query, constraints)
            return results
        except Exception as e:
            print(f"数据库搜索失败: {e}")
            return []
    
    async def _search_octopart(
        self,
        query: str,
        constraints: Optional[Dict],
        limit: int
    ) -> List[Dict]:
        """Octopart API 搜索"""
        # 模拟 Octopart API 响应
        # 实际实现需要使用 httpx 调用真实 API
        return []
    
    def _calculate_score(
        self,
        result: Dict,
        query: str,
        constraints: Optional[Dict]
    ) -> float:
        """计算相关性分数"""
        score = 0.5  # 基础分
        
        query_lower = query.lower()
        
        # 型号匹配
        if result.get("part_number", "").lower() in query_lower:
            score += 0.3
        
        # 描述匹配
        if result.get("description", "").lower() in query_lower:
            score += 0.1
        
        # 约束匹配
        if constraints:
            for key, value in constraints.items():
                if result.get(key) and value.lower() in str(result[key]).lower():
                    score += 0.1
        
        return min(score, 1.0)
    
    def _merge_results(
        self,
        db_results: List[Dict],
        api_results: List[Dict]
    ) -> List[Dict]:
        """合并搜索结果"""
        combined = {r["part_number"]: r for r in db_results}
        
        for r in api_results:
            pn = r["part_number"]
            if pn in combined:
                # 合并价格和库存信息
                if r.get("price"):
                    combined[pn]["price"] = r["price"]
                if r.get("stock"):
                    combined[pn]["stock"] = r["stock"]
                combined[pn]["vendors"] = combined[pn].get("vendors", []) + r.get("vendors", [])
            else:
                r["source"] = "api"
                combined[pn] = r
        
        return list(combined.values())[:20]
    
    async def compare_prices(self, part_number: str) -> Dict:
        """比价查询"""
        # 从数据库获取价格
        try:
            price_data = db_get_price(part_number)
            if price_data and price_data.get("prices"):
                return {
                    "part_number": part_number,
                    "prices": price_data["prices"],
                    "best_price": price_data.get("best_price"),
                    "best_vendor": price_data.get("best_vendor"),
                    "total_stock": price_data.get("total_stock", 0)
                }
        except Exception as e:
            print(f"比价失败: {e}")
        
        return {"part_number": part_number, "prices": [], "best_price": None, "total_stock": 0}
    
    async def get_alternatives(self, part_number: str) -> List[Dict]:
        """获取替代料"""
        try:
            from .database import get_alternatives as db_get_alts
            return db_get_alts(part_number)
        except Exception as e:
            print(f"获取替代料失败: {e}")
            return []


# 便捷函数
async def search(query: str, limit: int = 10) -> List[Dict]:
    """快速搜索"""
    engine = SearchEngine()
    return await engine.search(query, limit=limit)


def get_price_comparison_sync(part_number: str) -> List[Dict]:
    """价格对比 (同步版本)"""
    import asyncio
    engine = SearchEngine()
    
    # 检查是否已在事件循环中
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            async def do_compare():
                return await engine.compare_prices(part_number)
            return asyncio.run_coroutine_threadsafe(do_compare(), loop).result()
    except RuntimeError:
        pass
    
    return asyncio.run(engine.compare_prices(part_number))
