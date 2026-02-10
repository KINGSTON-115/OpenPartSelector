"""
集成测试 - Search 模块
"""
import pytest
import asyncio


class TestSearchEngine:
    """搜索引擎测试类"""
    
    @pytest.fixture
    def config(self):
        """创建测试配置"""
        from ops.config import Config
        return Config()
    
    @pytest.fixture
    def engine(self, config):
        """创建 SearchEngine 实例"""
        from ops.search import SearchEngine
        return SearchEngine(config)
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self, engine):
        """测试引擎初始化"""
        await engine.initialize()
        assert engine._initialized is True
        
        # 清理
        await engine.close()
    
    @pytest.mark.asyncio
    async def test_search_returns_results(self, engine):
        """测试搜索返回结果"""
        await engine.initialize()
        
        results = await engine.search(
            query="LDO 3.3V",
            limit=5
        )
        
        # 应该返回列表
        assert isinstance(results, list)
        
        # 清理
        await engine.close()
    
    @pytest.mark.asyncio
    async def test_compare_prices(self, engine):
        """测试比价功能"""
        await engine.initialize()
        
        prices = await engine.compare_prices("LD1117V33")
        
        assert "part_number" in prices
        assert "prices" in prices
        
        # 清理
        await engine.close()
    
    @pytest.mark.asyncio
    async def test_search_with_constraints(self, engine):
        """测试带约束的搜索"""
        await engine.initialize()
        
        results = await engine.search(
            query="LDO",
            constraints={"voltage": "3.3V"},
            limit=10
        )
        
        assert isinstance(results, list)
        
        # 清理
        await engine.close()
