"""
单元测试 - Agent 模块
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch


class TestAgent:
    """Agent 测试类"""
    
    @pytest.fixture
    def config(self):
        """创建测试配置"""
        from ops.config import Config
        return Config()
    
    @pytest.fixture
    def agent(self, config):
        """创建 Agent 实例"""
        from ops.agent import Agent
        return Agent(config)
    
    def test_parse_query_basic(self, agent):
        """测试基础查询解析"""
        query = "为 ESP32 项目找一个 3.3V LDO"
        result = agent.parse_query(query)
        
        assert "original_query" in result
        assert "target_voltage" in result
        assert result["target_voltage"] == "3.3V"
    
    def test_parse_query_voltage(self, agent):
        """测试电压解析"""
        queries = [
            ("5V LDO", "5V"),
            ("12V DC-DC", "12V"),
            ("3.3V", "3.3V"),
        ]
        
        for query, expected_voltage in queries:
            result = agent.parse_query(query)
            assert result["target_voltage"] == expected_voltage, f"Failed for: {query}"
    
    def test_parse_query_package(self, agent):
        """测试封装解析"""
        queries = [
            ("SOP-8 封装", "SOP-8"),
            ("QFN 封装", "QFN"),
            ("SOT-223", "SOT-223"),
        ]
        
        for query, expected_pkg in queries:
            result = agent.parse_query(query)
            assert result["target_package"] == expected_pkg, f"Failed for: {query}"
    
    def test_parse_query_category(self, agent):
        """测试分类推断"""
        queries = [
            ("STM32 单片机", "mcu"),
            ("LDO 电源芯片", "power"),
            ("温度传感器", "sensor"),
            ("USB 转串口", "interface"),
        ]
        
        for query, expected_category in queries:
            result = agent.parse_query(query)
            assert result["category_hint"] == expected_category, f"Failed for: {query}"
    
    @pytest.mark.asyncio
    async def test_select_requires_initialize(self, agent):
        """测试初始化后可以正常选型"""
        # 初始化后应该可以正常工作
        await agent.initialize()
        assert agent._initialized is True
        
        # 验证初始化后搜索不会出错
        results = await agent.search_engine.search(query="LDO", limit=1)
        assert isinstance(results, list)
    
    @pytest.mark.asyncio
    async def test_bom_generation(self, agent):
        """测试 BOM 生成"""
        from ops.agent import SearchResult, PartSpec
        
        mock_results = [
            SearchResult(
                part_number="LD1117V33",
                description="LDO 3.3V",
                manufacturer="ST",
                category="power",
                specs=PartSpec(voltage="3.3V", current="1A"),
                price=0.5
            ),
            SearchResult(
                part_number="AMS1117-3.3",
                description="LDO 3.3V",
                manufacturer="AMS",
                category="power",
                specs=PartSpec(voltage="3.3V", current="1A"),
                price=0.3
            )
        ]
        
        bom = agent._generate_bom(mock_results)
        
        assert len(bom) == 2
        assert bom[0]["part_number"] == "LD1117V33"
        assert bom[0]["quantity"] == 1


class TestPartSpec:
    """PartSpec 测试类"""
    
    def test_spec_creation(self):
        """测试规格创建"""
        from ops.agent import PartSpec
        
        spec = PartSpec(
            voltage="3.3V",
            current="1A",
            package="SOT-223"
        )
        
        assert spec.voltage == "3.3V"
        assert spec.current == "1A"
        assert spec.package == "SOT-223"
    
    def test_spec_defaults(self):
        """测试默认值"""
        from ops.agent import PartSpec
        
        spec = PartSpec()
        
        assert spec.voltage is None
        assert spec.current is None
        assert spec.package is None


class TestSearchResult:
    """SearchResult 测试类"""
    
    def test_result_creation(self):
        """测试结果创建"""
        from ops.agent import SearchResult, PartSpec
        
        result = SearchResult(
            part_number="STM32F103",
            description="MCU",
            manufacturer="ST",
            category="mcu",
            specs=PartSpec(voltage="3.3V"),
            price=2.0,
            stock=1000
        )
        
        assert result.part_number == "STM32F103"
        assert result.price == 2.0
        assert result.stock == 1000
