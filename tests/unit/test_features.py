"""
单元测试 - Features 模块
测试锦上添花功能：国产替代、参考电路、计算工具
"""
import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ops.features import (
    find_alternatives,
    get_circuit_template,
    search_circuits,
    get_datasheet_summary,
    calculate_resistor_for_led,
    calculate_voltage_divider,
    calculate_pwm_frequency,
    CHIP_ALTERNATIVES,
    CIRCUIT_TEMPLATES,
    DATASHEET_SUMMARIES,
)


class TestAlternatives:
    """国产替代功能测试"""

    def test_find_alternatives_stm32(self):
        """测试 STM32F103 替代查找"""
        alts = find_alternatives("STM32F103C8T6")
        
        assert len(alts) > 0
        assert any(a["model"] == "GD32F103C8T6" for a in alts)
    
    def test_find_alternatives_esp32(self):
        """测试 ESP32 替代查找"""
        alts = find_alternatives("ESP32")
        
        assert len(alts) > 0
        assert any(a["brand"] == "乐鑫" for a in alts)
    
    def test_find_alternatives_ch340(self):
        """测试 CH340 替代查找"""
        alts = find_alternatives("CH340G")
        
        assert len(alts) > 0
        assert any(a["model"] == "CH340N" for a in alts)
    
    def test_find_alternatives_not_found(self):
        """测试未找到替代"""
        alts = find_alternatives("UNKNOWN_CHIP_12345")
        assert alts == []
    
    def test_alternatives_structure(self):
        """测试替代数据结构"""
        alts = find_alternatives("STM32F103C8T6")
        
        if alts:
            alt = alts[0]
            assert "brand" in alt
            assert "model" in alt
            assert "price_ratio" in alt
            assert "compatibility" in alt
            assert "notes" in alt


class TestCircuitTemplates:
    """参考电路模板测试"""

    def test_get_circuit_esp32(self):
        """测试获取 ESP32 最小系统"""
        tmpl = get_circuit_template("esp32_minimal")
        
        assert tmpl is not None
        assert "name" in tmpl
        assert "器件列表" in tmpl
        assert "注意事项" in tmpl
        assert tmpl["difficulty"] == "⭐"
    
    def test_get_circuit_stm32(self):
        """测试获取 STM32 最小系统"""
        tmpl = get_circuit_template("stm32_minimal")
        
        assert tmpl is not None
        assert "STM32" in tmpl["name"]
    
    def test_get_circuit_not_found(self):
        """测试获取不存在的电路"""
        tmpl = get_circuit_template("nonexistent_circuit")
        assert tmpl is None
    
    def test_get_circuit_case_insensitive(self):
        """测试大小写不敏感"""
        tmpl1 = get_circuit_template("ESP32_MINIMAL")
        tmpl2 = get_circuit_template("esp32_minimal")
        
        assert tmpl1 == tmpl2
    
    def test_search_circuits(self):
        """测试搜索电路"""
        results = search_circuits("蓝牙")
        
        assert len(results) > 0
        assert any("蓝牙" in r["name"] for r in results)
    
    def test_circuit_components_count(self):
        """测试电路元件数量"""
        tmpl = get_circuit_template("esp32_minimal")
        
        assert len(tmpl["器件列表"]) >= 4
    
    def test_all_templates_valid(self):
        """验证所有模板结构有效"""
        for key, tmpl in CIRCUIT_TEMPLATES.items():
            assert "name" in tmpl
            assert "difficulty" in tmpl
            assert "器件列表" in tmpl
            assert "注意事项" in tmpl


class TestDatasheetSummaries:
    """Datasheet 中文解读测试"""

    def test_get_summary_stm32(self):
        """测试 STM32 datasheet 摘要"""
        summary = get_datasheet_summary("STM32F103C8T6")
        
        assert summary is not None
        assert "一句话说明" in summary
        assert "主要特点" in summary
        assert "应用场景" in summary
        assert "注意事项" in summary
    
    def test_get_summary_esp32(self):
        """测试 ESP32 datasheet 摘要"""
        summary = get_datasheet_summary("ESP32-WROOM-32")
        
        assert summary is not None
        assert "一句话说明" in summary
    
    def test_get_summary_not_found(self):
        """测试获取不存在的摘要"""
        summary = get_datasheet_summary("UNKNOWN_CHIP")
        assert summary is None
    
    def test_summary_structure(self):
        """测试摘要数据结构"""
        summary = get_datasheet_summary("STM32F103C8T6")
        
        if summary:
            assert isinstance(summary["主要特点"], list)
            assert isinstance(summary["应用场景"], list)
            assert isinstance(summary["注意事项"], list)


class TestCalculators:
    """计算工具测试"""

    def test_calculate_resistor_standard_values(self):
        """测试标准电阻值计算"""
        result = calculate_resistor_for_led(
            voltage=5.0,
            led_voltage=2.0,
            led_current=0.02
        )
        
        assert "recommended_resistance" in result
        # 5V-2V=3V / 0.02A = 150Ω
        # E24系列中150附近的标准值
        e24_standard = [130, 150, 160, 180, 200]
        assert int(result["recommended_resistance"]) in e24_standard
    
    def test_calculate_resistor_error_voltage(self):
        """测试电压不足错误"""
        result = calculate_resistor_for_led(
            voltage=1.5,
            led_voltage=2.0,
            led_current=0.02
        )
        
        assert "error" in result
    
    def test_calculate_resistor_formula(self):
        """测试计算公式正确性"""
        result = calculate_resistor_for_led(
            voltage=5.0,
            led_voltage=2.0,
            led_current=0.01  # 10mA
        )
        
        # 计算值 = (5-2)/0.01 = 300Ω
        calculated = float(result["calculated_resistance"])
        assert 290 < calculated < 310
    
    def test_calculate_voltage_divider(self):
        """测试分压电阻计算"""
        result = calculate_voltage_divider(v_in=5.0, v_out=3.3)
        
        assert "recommended_r1" in result
        assert "recommended_r2" in result
    
    def test_calculate_voltage_divider_with_r1(self):
        """测试指定R1的分压计算"""
        result = calculate_voltage_divider(v_in=5.0, v_out=2.5, r1=10000)
        
        assert "recommended_r2" in result
    
    def test_pwm_frequency(self):
        """测试 PWM 频率计算"""
        result = calculate_pwm_frequency(
            timer_clock=72000000,
            prescaler=7199,
            auto_reload=99
        )
        
        assert "frequency" in result
        # 72MHz / 7200 / 100 = 100Hz
        freq = float(result["frequency"].replace("Hz", ""))
        assert 90 < freq < 110


class TestFeaturesDataIntegrity:
    """数据完整性测试"""

    def test_alternatives_has_required_chips(self):
        """测试替代库包含常用芯片"""
        required = ["STM32F103C8T6", "ESP32", "CH340G", "AMS1117", "LM358"]
        
        for chip in required:
            alts = find_alternatives(chip)
            assert len(alts) > 0, f"Missing alternatives for {chip}"
    
    def test_circuits_has_minimal_systems(self):
        """测试包含最小系统电路"""
        minimal_circuits = ["esp32_minimal", "stm32_minimal"]
        
        for key in minimal_circuits:
            tmpl = get_circuit_template(key)
            assert tmpl is not None, f"Missing circuit: {key}"
            assert tmpl["jlc_bom_cost"] > 0
    
    def test_datasheets_has_popular_chips(self):
        """测试包含常用芯片的 datasheet 解读"""
        popular = ["STM32F103C8T6", "ESP32-WROOM-32", "CH340G", "AMS1117", "LM358"]
        
        for chip in popular:
            summary = get_datasheet_summary(chip)
            assert summary is not None, f"Missing datasheet for {chip}"
            assert summary["一句话说明"] is not None
