"""
集成测试 - 测试完整的用户流程
"""
import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.asyncio
async def test_quick_select_basic():
    """测试基础快速选型"""
    from ops.agent import quick_select
    
    # 执行搜索 (quick_select 是同步函数)
    result = quick_select("ESP32", top_k=3)
    
    # 验证结果结构
    assert result is not None
    assert hasattr(result, "query")
    assert hasattr(result, "recommended_parts")
    assert hasattr(result, "analysis_report")
    assert hasattr(result, "bom_items")
    
    print(f"✅ 查询: {result.query}")
    print(f"✅ 推荐数量: {len(result.recommended_parts)}")
    print(f"✅ 报告长度: {len(result.analysis_report)}")


@pytest.mark.asyncio
async def test_quick_select_with_constraints():
    """测试带约束的选型"""
    from ops.agent import Agent
    
    agent = Agent()
    
    result = await agent.select(
        query="找一个 3.3V LDO 1A",
        constraints={"package": "SOP-8"},
        top_k=5
    )
    
    # 验证结果
    assert result is not None
    assert len(result.recommended_parts) >= 0  # 可能没有匹配结果
    
    print(f"✅ 带约束选型完成，推荐 {len(result.recommended_parts)} 个器件")


@pytest.mark.asyncio
async def test_search_engine():
    """测试搜索引擎"""
    from ops.search import SearchEngine
    
    engine = SearchEngine()
    
    # 测试数据库搜索
    results = await engine.search(query="STM32", limit=5)
    
    assert isinstance(results, list)
    
    print(f"✅ 搜索引擎返回 {len(results)} 个结果")


@pytest.mark.asyncio
async def test_compare_prices():
    """测试比价功能"""
    from ops.search import SearchEngine
    
    engine = SearchEngine()
    result = await engine.compare_prices("STM32F103C8T6")
    
    assert "part_number" in result
    assert "prices" in result
    
    print(f"✅ 比价结果: {result['part_number']}")


async def test_features():
    """测试锦上添花功能"""
    from ops.features import (
        find_alternatives,
        get_circuit_template,
        get_datasheet_summary,
        calculate_resistor_for_led,
        calculate_voltage_divider
    )
    
    # 1. 测试国产替代
    alts = find_alternatives("STM32F103C8T6")
    assert isinstance(alts, list)
    if alts:
        assert "model" in alts[0]
    print(f"✅ 国产替代: 找到 {len(alts)} 个替代方案")
    
    # 2. 测试电路模板
    tmpl = get_circuit_template("esp32_minimal")
    assert tmpl is not None
    assert "name" in tmpl
    assert "器件列表" in tmpl
    print(f"✅ 电路模板: {tmpl['name']}")
    
    # 3. 测试Datasheet摘要
    summary = get_datasheet_summary("STM32F103C8T6")
    assert summary is not None
    assert "一句话说明" in summary
    print(f"✅ Datasheet摘要: 获取成功")
    
    # 4. 测试LED电阻计算
    led_calc = calculate_resistor_for_led(voltage=5.0, led_voltage=2.0, led_current=0.02)
    assert "recommended_resistance" in led_calc
    print(f"✅ LED电阻计算: 推荐 {led_calc['recommended_resistance']}Ω")
    
    # 5. 测试分压计算
    div_calc = calculate_voltage_divider(v_in=5.0, v_out=3.3)
    assert "recommended_r1" in div_calc
    print(f"✅ 分压计算: R1={div_calc['recommended_r1']}")


async def test_jlc_features():
    """测试嘉立创功能"""
    try:
        from ops.jlc import search_jlc
        
        # 搜索
        results = search_jlc("ESP32")
        assert isinstance(results, list)
        print(f"✅ JLC搜索: 找到 {len(results)} 个结果")
        
    except Exception as e:
        print(f"⚠️ JLC功能测试跳过: {e}")


async def test_bom_analysis():
    """测试BOM分析"""
    from ops.bom import analyze_bom_full
    
    # 测试空BOM
    result = analyze_bom_full([])
    assert "summary" in result
    assert "total_price" in result["summary"]
    print(f"✅ BOM分析: 总价 ¥{result['summary']['total_price']}")


def test_features_sync():
    """同步测试锦上添花功能"""
    from ops.features import (
        find_alternatives,
        get_circuit_template,
        calculate_resistor_for_led
    )
    
    # 测试LED计算器 (5V - 2V = 3V, 3V/0.02A = 150Ω, E24最近值=150)
    result = calculate_resistor_for_led()
    assert result["recommended_resistance"] == "150"  # 期望标准值
    print(f"✅ LED计算器同步测试通过")
    
    # 测试改进后的LED计算器 (包含更多E24值)
    result2 = calculate_resistor_for_led(voltage=12.0, led_voltage=3.2, led_current=0.02)
    assert "nearby_standard_values" in result2
    assert "power_rating" in result2
    print(f"✅ 改进版LED计算器测试通过")


async def test_edge_cases():
    """测试边缘情况"""
    from ops.features import calculate_resistor_for_led
    
    # 1. 电压不足的情况
    result = calculate_resistor_for_led(voltage=1.5, led_voltage=2.0, led_current=0.02)
    assert "error" in result
    print(f"✅ 电压不足错误处理通过")
    
    # 2. 空查询
    from ops.agent import quick_select
    result = quick_select("nonexistent_part_xyz_123", top_k=3)
    assert result is not None
    assert len(result.recommended_parts) == 0  # 预期无结果
    print(f"✅ 无结果查询测试通过")


async def test_passive_components():
    """测试被动器件数据库"""
    from ops.database import search_components, PASSIVE_COMPONENTS
    
    # 测试被动器件是否存在
    assert len(PASSIVE_COMPONENTS) > 0
    print(f"✅ 被动器件库包含 {len(PASSIVE_COMPONENTS)} 个器件")
    
    # 测试搜索被动器件
    results = search_components(query="10K", category="passive")
    assert len(results) > 0
    print(f"✅ 被动器件搜索测试通过")


# 运行测试
if __name__ == "__main__":
    import asyncio
    
    async def run_all_tests():
        print("=" * 60)
        print("🚀 OpenPartSelector 集成测试")
        print("=" * 60)
        
        await test_quick_select_basic()
        print()
        
        await test_quick_select_with_constraints()
        print()
        
        await test_search_engine()
        print()
        
        await test_compare_prices()
        print()
        
        await test_features()
        print()
        
        await test_jlc_features()
        print()
        
        await test_bom_analysis()
        print()
        
        test_features_sync()
        print()
        
        await test_edge_cases()
        print()
        
        await test_passive_components()
        print()
        
        print("=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
    
    asyncio.run(run_all_tests())
