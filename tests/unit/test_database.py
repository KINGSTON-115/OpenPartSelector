"""
数据库模块单元测试
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_search_components_basic():
    """测试基础组件搜索"""
    from ops.database import search_components
    
    # 搜索 LDO
    results = search_components(query="LDO", limit=10)
    
    assert isinstance(results, list)
    print(f"✅ LDO搜索: 找到 {len(results)} 个结果")
    
    if results:
        assert "part_number" in results[0]
        assert "description" in results[0]


def test_search_mcu():
    """测试 MCU 搜索"""
    from ops.database import search_components
    
    results = search_components(query="STM32", limit=5)
    
    assert isinstance(results, list)
    print(f"✅ STM32搜索: 找到 {len(results)} 个结果")


def test_get_price_comparison():
    """测试价格对比"""
    from ops.database import get_price_comparison
    
    result = get_price_comparison("LD1117V33")
    
    assert result is not None
    assert "part_number" in result
    assert "prices" in result
    assert isinstance(result["prices"], list)
    
    print(f"✅ 价格对比: {result['part_number']}")


def test_get_alternatives():
    """测试替代器件查询"""
    from ops.database import get_alternatives
    
    alts = get_alternatives("STM32F103C8T6")
    
    assert isinstance(alts, list)
    
    if alts:
        assert "part_number" in alts[0]
    
    print(f"✅ 替代器件: 找到 {len(alts)} 个替代方案")


def test_database_functions():
    """测试数据库导出函数"""
    from ops.database import (
        get_all_components,
        get_components_by_category,
        get_component_by_partnumber
    )
    
    # 测试获取所有组件（按分类）
    all_comps = get_all_components()
    assert isinstance(all_comps, dict)
    assert "power" in all_comps
    assert "communication" in all_comps
    assert "sensor" in all_comps
    print(f"✅ 总组件分类: {list(all_comps.keys())}")
    
    # 测试按类别获取
    power_comps = get_components_by_category("power")
    assert isinstance(power_comps, list)
    print(f"✅ 电源管理组件: {len(power_comps)}")
    
    # 测试按型号获取
    comp = get_component_by_partnumber("LD1117V33")
    if comp:
        assert comp["part_number"] == "LD1117V33"
        print(f"✅ 精确查询: {comp['part_number']}")


def test_database_sync():
    """同步测试数据库功能"""
    from ops.database import search_components
    
    # 简单查询测试
    results = search_components(query="ESP32")
    assert isinstance(results, list)
    print(f"✅ ESP32同步查询: {len(results)} 个结果")


def test_sensor_database_v127():
    """测试 v1.1.27 新增传感器"""
    from ops.database import search_components, SENSORS, get_component
    
    # 测试新传感器搜索
    new_sensors = ["AHT20", "MPU9250", "APDS-9960", "VL6180", "BME680", "RCWL-0516"]
    
    for sensor_pn in new_sensors:
        comp = get_component(sensor_pn)
        if comp:
            assert comp["category"] == "sensor"
            assert comp["part_number"] == sensor_pn
            print(f"✅ 新增传感器验证: {sensor_pn}")
    
    # 测试传感器类别搜索
    sensor_results = search_components(query="sensor", category="sensor", limit=50)
    assert len(sensor_results) >= 6  # 至少包含新增的6个
    print(f"✅ 传感器总数: {len(sensor_results)}")


# 运行测试
if __name__ == "__main__":
    print("=" * 60)
    print("🗄️ OpenPartSelector 数据库模块测试")
    print("=" * 60)
    
    test_search_components_basic()
    print()
    
    test_search_mcu()
    print()
    
    test_get_price_comparison()
    print()
    
    test_get_alternatives()
    print()
    
    test_database_functions()
    print()
    
    test_database_sync()
    print()
    
    print("=" * 60)
    print("✅ 所有数据库测试完成!")
    print("=" * 60)
