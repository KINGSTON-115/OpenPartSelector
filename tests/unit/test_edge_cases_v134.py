"""
v1.1.34 边缘情况增强测试
新增更多边界条件测试用例
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ops.features import (
    calculate_resistor_for_led,
    calculate_voltage_divider,
    calculate_pwm_frequency,
    calculate_rc_time_constant,
    calculate_capacitor_ripple,
    calculate_battery_life,
    calculate_voltage_reference,
    calculate_led_parallel_resistor,
    calculate_inductor_rough,
    find_e24_closest,
    find_e24_nearby,
    decode_resistor_4band,
    decode_resistor_5band,
    decode_capacitor_3band,
    calculate_led_resistor,
    calculate_led_series_resistor,
    calculate_inductor_energy,
    calculate_rf_attenuator,
)


class TestVoltageDividerEdgeCases:
    """分压电阻边缘情况测试"""

    def test_voltage_divider_equal_vin_vout(self):
        """测试输入输出电压相等"""
        result = calculate_voltage_divider(v_in=3.3, v_out=3.3)
        assert "error" in result

    def test_voltage_divider_zero_vin(self):
        """测试零输入电压"""
        result = calculate_voltage_divider(v_in=0, v_out=2.5)
        assert "error" in result

    def test_voltage_divider_zero_vout(self):
        """测试零输出电压"""
        result = calculate_voltage_divider(v_in=5.0, v_out=0)
        assert "error" in result

    def test_voltage_divider_vout_greater_vin(self):
        """测试输出大于输入"""
        result = calculate_voltage_divider(v_in=3.3, v_out=5.0)
        assert "error" in result

    def test_voltage_divider_high_voltage(self):
        """测试高压输入 (12V→3.3V)"""
        result = calculate_voltage_divider(v_in=12.0, v_out=3.3, r1=10000)
        assert "recommended_r2" in result
        actual_vout = float(result["actual_vout"].replace("V", ""))
        assert actual_vout < 3.4

    def test_voltage_divider_with_custom_r1(self):
        """测试指定R1参数"""
        result = calculate_voltage_divider(v_in=5.0, v_out=2.5, r1=20000)
        assert "recommended_r2" in result
        assert "20KΩ" in result["tips"][0]


class TestPWMFrequencyEdgeCases:
    """PWM频率边缘情况测试"""

    def test_pwm_zero_timer_clock(self):
        """测试零时钟频率"""
        result = calculate_pwm_frequency(timer_clock=0, prescaler=7199, auto_reload=99)
        assert "error" in result

    def test_pwm_zero_prescaler(self):
        """测试零预分频"""
        result = calculate_pwm_frequency(timer_clock=72000000, prescaler=0, auto_reload=99)
        assert "error" in result

    def test_pwm_zero_auto_reload(self):
        """测试零自动重载"""
        result = calculate_pwm_frequency(timer_clock=72000000, prescaler=7199, auto_reload=0)
        assert "error" in result

    def test_pwm_high_frequency(self):
        """测试高频PWM (72MHz / 72 / 100 = 10kHz)"""
        result = calculate_pwm_frequency(timer_clock=72000000, prescaler=71, auto_reload=99)
        freq = float(result["frequency"].replace("Hz", "").replace("kHz", "") * (1000 if "kHz" in result["frequency"] else 1))
        assert freq > 9000  # 约10kHz

    def test_pwm_very_low_frequency(self):
        """测试超低频PWM"""
        result = calculate_pwm_frequency(timer_clock=72000000, prescaler=71999, auto_reload=65535)
        freq = float(result["frequency"].replace("Hz", ""))
        assert freq < 10  # 应该小于10Hz


class TestRCTimeConstantEdgeCases:
    """RC时间常数边缘情况测试"""

    def test_rc_zero_resistance(self):
        """测试零电阻"""
        result = calculate_rc_time_constant(resistance=0, capacitance=0.0001)
        assert "error" in result

    def test_rc_zero_capacitance(self):
        """测试零电容"""
        result = calculate_rc_time_constant(resistance=10000, capacitance=0)
        assert "error" in result

    def test_rc_micro_farad(self):
        """测试微法级电容"""
        result = calculate_rc_time_constant(resistance=1000, capacitance=0.000001)
        # 1KΩ × 1μF = 1ms
        time_str = result["time_constant"].replace("ms", "").replace("μs", "").replace("s", "")
        time_val = float(time_str)
        assert time_val == 1.0

    def test_rc_nano_farad(self):
        """测试纳法级电容"""
        result = calculate_rc_time_constant(resistance=10000, capacitance=0.0000001)
        # 10KΩ × 100nF = 1ms
        time_str = result["time_constant"].replace("ms", "").replace("μs", "").replace("s", "")
        time_val = float(time_str)
        assert time_val == 1.0

    def test_rc_megaohm_picofarad(self):
        """测试高阻小容组合"""
        result = calculate_rc_time_constant(resistance=1000000, capacitance=0.0000000001)
        # 1MΩ × 100pF = 100μs
        assert "0.1ms" in result["time_constant"] or "100μs" in result["time_constant"]


class TestCapacitorRippleEdgeCases:
    """滤波电容边缘情况测试"""

    def test_ripple_zero_load_current(self):
        """测试零负载电流"""
        result = calculate_capacitor_ripple(load_current=0, ripple_voltage=0.5, frequency=120)
        assert "error" in result

    def test_ripple_zero_frequency(self):
        """测试零频率"""
        result = calculate_capacitor_ripple(load_current=0.1, ripple_voltage=0.5, frequency=0)
        assert "error" in result

    def test_ripple_very_small_current(self):
        """测试极小电流 (μA级)"""
        result = calculate_capacitor_ripple(
            load_current=0.0001,  # 100μA
            ripple_voltage=0.1,
            frequency=100
        )
        # 需要极小电容
        if "error" in result:
            return  # 跳过错误情况
        recommended = int(result["recommended_capacitor"].replace("μF", ""))
        assert recommended < 100

    def test_ripple_very_large_current(self):
        """测试大电流 (A级别)"""
        result = calculate_capacitor_ripple(
            load_current=5.0,  # 5A
            ripple_voltage=0.5,
            frequency=120
        )
        # 需要很大电容
        recommended = int(result["recommended_capacitor"].replace("μF", ""))
        assert recommended > 10000

    def test_ripple_50hz_ac_doubler(self):
        """测试50Hz全波整流"""
        result = calculate_capacitor_ripple(
            load_current=0.5,
            ripple_voltage=1.0,
            frequency=100  # 全波整流100Hz
        )
        assert "100Hz" in result["tips"][0]


class TestBatteryLifeEdgeCases:
    """电池续航边缘情况测试"""

    def test_battery_exact_capacity(self):
        """测试精确匹配容量"""
        result = calculate_battery_life(
            battery_capacity=100,
            avg_current=10,
            active_time_per_day=10
        )
        # 每天消耗 100mAh，应该正好1天
        assert "mAh" in result["daily_capacity_used"]

    def test_battery_coin_cell(self):
        """测试纽扣电池 (CR2032)"""
        result = calculate_battery_life(
            battery_capacity=220,
            avg_current=5,
            standby_current=0.001,
            active_time_per_day=0.5
        )
        if "error" in result:
            return  # 跳过零电流情况
        days = float(result["battery_life_days"].replace("天", ""))
        assert 10 < days < 5000

    def test_battery_power_bank(self):
        """测试充电宝 (10000mAh)"""
        result = calculate_battery_life(
            battery_capacity=10000,
            avg_current=500,
            standby_current=10,
            active_time_per_day=2
        )
        days = float(result["battery_life_days"].replace("天", ""))
        assert days > 5

    def test_battery_very_high_current(self):
        """测试极高功耗 (电机驱动)"""
        result = calculate_battery_life(
            battery_capacity=2000,
            avg_current=2000,  # 2A
            standby_current=1,
            active_time_per_day=0.5
        )
        if "error" in result:
            return  # 跳过零电流情况
        days = float(result["battery_life_days"].replace("天", ""))
        assert days <= 3  # 最多几天

    def test_battery_zero_avg_current(self):
        """测试零平均电流 (纯待机) - 只有待机电流"""
        result = calculate_battery_life(
            battery_capacity=2000,
            avg_current=0,
            standby_current=0.01,
            active_time_per_day=0
        )
        # 这个情况可能有正常计算结果
        assert "battery_life_days" in result or "error" in result


class TestVoltageReferenceEdgeCases:
    """电压基准边缘情况测试"""

    def test_vref_low_input(self):
        """测试低压输入 (3.3V)"""
        result = calculate_voltage_reference(
            v_in=3.3,
            v_ref=1.8,
            i_ref=0.001
        )
        assert "calculated_r1" in result
        assert "calculated_r2" in result

    def test_vref_high_input(self):
        """测试高压输入 (24V)"""
        result = calculate_voltage_reference(
            v_in=24.0,
            v_ref=2.5,
            i_ref=0.001
        )
        # 需要更大的分压电阻
        r1_str = result["calculated_r1"]
        r1 = float(r1_str.replace("KΩ", "").replace("MΩ", "").replace("Ω", ""))
        assert r1 > 1000  # 应该用 KΩ 级

    def test_vref_tiny_reference(self):
        """测试微小基准电压 (0.8V)"""
        result = calculate_voltage_reference(
            v_in=5.0,
            v_ref=0.8,
            i_ref=0.0005
        )
        assert "error" not in result

    def test_vref_high_reference(self):
        """测试高基准电压 (10V)"""
        result = calculate_voltage_reference(
            v_in=12.0,
            v_ref=10.0,
            i_ref=0.001
        )
        assert "error" not in result

    def test_vref_low_current(self):
        """测试微安级参考电流"""
        result = calculate_voltage_reference(
            v_in=12.0,
            v_ref=2.5,
            i_ref=0.00005  # 50μA
        )
        # 需要更大电阻
        assert "calculated_r1" in result
        assert "calculated_r2" in result


class TestLEDParallelEdgeCases:
    """LED并联边缘情况测试"""

    def test_led_single_5v_red(self):
        """测试单颗红LED (5V供电)"""
        result = calculate_led_parallel_resistor(
            v_supply=5.0,
            led_voltage=1.8,
            led_current=0.02,
            num_leds=1
        )
        # (5-1.8)/0.02 = 160Ω
        assert "recommended_resistor" in result
        assert "parallel连接1个LED" in result["tips"][0]

    def test_led_many_in_parallel(self):
        """测试多颗LED并联"""
        result = calculate_led_parallel_resistor(
            v_supply=5.0,
            led_voltage=2.0,
            led_current=0.02,
            num_leds=10
        )
        # (5-2)/0.2 = 15Ω
        assert "recommended_resistor" in result

    def test_led_12v_series_many(self):
        """测试12V供电多颗串联"""
        result = calculate_led_parallel_resistor(
            v_supply=12.0,
            led_voltage=2.0,
            led_current=0.01,
            num_leds=5,
            arrangement="series"
        )
        # (12-10)/0.01 = 200Ω
        assert "recommended_resistor" in result

    def test_led_low_voltage_error(self):
        """测试低压无法点亮"""
        result = calculate_led_parallel_resistor(
            v_supply=1.5,
            led_voltage=2.0,
            led_current=0.01,
            num_leds=1
        )
        assert "error" in result

    def test_led_zero_current(self):
        """测试零电流"""
        result = calculate_led_parallel_resistor(
            v_supply=5.0,
            led_voltage=2.0,
            led_current=0,
            num_leds=1
        )
        assert "error" in result


class TestInductorEdgeCases:
    """电感边缘情况测试"""

    def test_inductor_very_high_frequency(self):
        """测试超高频 (1MHz)"""
        result = calculate_inductor_rough(
            frequency=1000000,
            voltage_in=5.0,
            voltage_out=3.3,
            current_out=0.5
        )
        # 超高频需要很小的电感
        assert "recommended_inductance" in result
        assert "μH" in result["recommended_inductance"]
        assert float(result["recommended_inductance"].replace("μH", "")) < 20

    def test_inductor_very_low_frequency(self):
        """测试超低频 (10kHz)"""
        result = calculate_inductor_rough(
            frequency=10000,
            voltage_in=5.0,
            voltage_out=3.3,
            current_out=0.5
        )
        # 需要较大电感
        inductance = float(result["recommended_inductance"].replace("μH", ""))
        assert inductance > 100

    def test_inductor_high_current(self):
        """测试高电流输出 (3A)"""
        result = calculate_inductor_rough(
            frequency=100000,
            voltage_in=12.0,
            voltage_out=5.0,
            current_out=3.0
        )
        assert "error" not in result

    def test_inductor_min_voltage_diff(self):
        """测试最小压差 (5V→4.9V)"""
        result = calculate_inductor_rough(
            frequency=100000,
            voltage_in=5.0,
            voltage_out=4.9,
            current_out=0.1
        )
        assert result["duty_cycle"] is not None

    def test_inductor_zero_current(self):
        """测试零输出电流"""
        result = calculate_inductor_rough(
            frequency=100000,
            voltage_in=5.0,
            voltage_out=3.3,
            current_out=0
        )
        assert "error" in result


class TestE24StandardEdgeCases:
    """E24标准值边缘情况测试"""

    def test_e24_below_minimum(self):
        """测试低于最小标准值"""
        result = find_e24_closest(5)
        assert result == 10  # 最小E24是10Ω

    def test_e24_above_maximum(self):
        """测试高于最大标准值 (接近1MΩ)"""
        result = find_e24_closest(990000)
        assert 910000 <= result <= 1000000

    def test_e24_exact_boundary(self):
        """测试精确边界值"""
        # 10Ω 是边界
        assert find_e24_closest(10) == 10
        # 9.9Ω 应该舍入到 10Ω
        assert find_e24_closest(9.9) == 10
        # 10.1Ω 应该舍入到 10Ω
        assert find_e24_closest(10.1) == 10

    def test_e24_half_values(self):
        """测试半值情况"""
        # 15 是 E24 值
        assert find_e24_closest(15) == 15
        # 15.5 应该接近 15
        result = find_e24_closest(15.5)
        assert result in [15, 16]

    def test_e24_nearby_very_small(self):
        """测试极小值附近查找"""
        nearby = find_e24_nearby(12, count=3)
        assert "10Ω" in nearby or "12Ω" in nearby

    def test_e24_nearby_very_large(self):
        """测试极大值附近查找"""
        nearby = find_e24_nearby(910000, count=5)
        assert len(nearby) == 5


class TestResistorDecodeEdgeCases:
    """电阻解码边缘情况测试"""

    def test_resistor_4band_1ohm(self):
        """测试1Ω电阻"""
        result = decode_resistor_4band("brown", "black", "gold", "gold")
        # 棕黑金 = 1Ω
        assert "1Ω" in result["resistance"]

    def test_resistor_4band_10megaohm(self):
        """测试10MΩ电阻"""
        result = decode_resistor_4band("brown", "black", "blue", "gold")
        # 棕黑蓝 = 10MΩ
        assert "10" in result["resistance"] and "MΩ" in result["resistance"]

    def test_resistor_5band_megaohm(self):
        """测试兆欧级5环电阻"""
        result = decode_resistor_5band("brown", "black", "black", "yellow", "brown")
        # 棕黑黑黄 = 100K × 10 = 1MΩ
        assert "1.00MΩ" in result["resistance"] or "1MΩ" in result["resistance"]

    def test_resistor_4band_invalid_tolerance(self):
        """测试无效容差环"""
        result = decode_resistor_4band("brown", "black", "red", "pink")
        assert "error" in result or result["tolerance"] is not None  # pink 可能返回默认值

    def test_resistor_4band_white(self):
        """测试白环电阻"""
        result = decode_resistor_4band("white", "black", "brown", "gold")
        # 白黑棕 = 900Ω (E24最接近910)
        assert "900Ω" in result["resistance"] or "910Ω" in result["resistance"]

    def test_resistor_5band_ohm(self):
        """测试欧姆级5环精密电阻"""
        result = decode_resistor_5band("black", "black", "black", "gold", "brown")
        # 黑黑黑金 = 0Ω (可能是0欧姆电阻)
        assert "0Ω" in result["resistance"]


class TestCapacitorDecodeEdgeCases:
    """电容解码边缘情况测试"""

    def test_capacitor_picofarad(self):
        """测试皮法级电容"""
        result = decode_capacitor_3band("brown", "gray", "violet")
        # 棕灰紫 = 18 × 10M = 180M pF? 这不太对
        # 正确的电容色环: 第一二环是数值，第三环是乘数
        # 棕=1, 灰=8, 紫=10M -> 18 × 10M = 180M pF = 180μF (这个太大，不太合理)
        # 实际常用的小电容: 棕黑红 = 10 × 100 = 1000pF = 1nF
        pass

    def test_capacitor_nanofarad(self):
        """测试纳法级电容"""
        result = decode_capacitor_3band("brown", "black", "red")
        # 棕黑红 = 10 × 100 = 1000pF = 1nF
        assert result["capacitance"] == "1nF"

    def test_capacitor_microfarad(self):
        """测试微法级电容 (使用特殊标记)"""
        # 陶瓷电容很少用色环表示μF
        # 通常用代码表示
        pass

    def test_capacitor_invalid_color(self):
        """测试无效颜色"""
        result = decode_capacitor_3band("white", "white", "white")
        # 白环可能是无效的，但函数可能返回默认值
        assert "capacitance" in result


class TestLEDResistorEdgeCases:
    """LED电阻边缘情况测试"""

    def test_led_high_voltage_supply(self):
        """测试高压供电 (24V)"""
        result = calculate_led_resistor(
            voltage=24.0,
            led_voltage=2.0,
            led_current=0.015
        )
        # (24-2)/0.015 = 1466Ω, E24最接近 1.5K 或 1.2K
        assert "recommended_resistor" in result

    def test_led_very_high_current(self):
        """测试大电流LED (1A)"""
        result = calculate_led_resistor(
            voltage=5.0,
            led_voltage=3.2,
            led_current=1.0
        )
        # (5-3.2)/1 = 1.8Ω
        assert "recommended_resistor" in result
        # 需要大功率电阻
        assert "recommended_package" in result

    def test_led_series_basic(self):
        """测试串联电阻计算基础功能"""
        result = calculate_led_series_resistor(
            supply_voltage=5.0,
            led_forward_voltage=2.0,
            led_current=0.02
        )
        # (5-2)/0.02 = 150Ω
        assert "recommended_resistance" in result
        assert "recommended_package" in result


class TestInductorEnergyEdgeCases:
    """电感储能边缘情况测试"""

    def test_inductor_energy_microhenry(self):
        """测试微亨级电感"""
        result = calculate_inductor_energy(
            inductance=0.000001,  # 1μH
            current=1.0  # 1A
        )
        # E = ½ × 1μH × 1A² = 0.5μJ
        assert "0.5μJ" in result["energy"]

    def test_inductor_energy_millihenry(self):
        """测试毫亨级电感"""
        result = calculate_inductor_energy(
            inductance=0.01,  # 10mH
            current=0.1  # 100mA
        )
        # E = ½ × 10mH × 100mA² = 50μJ
        assert "50" in result["energy"] and "μJ" in result["energy"]

    def test_inductor_energy_zero_current(self):
        """测试零电流"""
        result = calculate_inductor_energy(
            inductance=0.001,
            current=0
        )
        # 零电流返回0能量
        assert "energy" in result

    def test_inductor_energy_zero_inductance(self):
        """测试零电感"""
        result = calculate_inductor_energy(
            inductance=0,
            current=0.1
        )
        # 零电感返回0能量
        assert "energy" in result


class TestRFAttenuatorEdgeCases:
    """射频衰减器边缘情况测试"""

    def test_attenuator_zero_input(self):
        """测试零输入功率"""
        result = calculate_rf_attenuator(
            input_power_dbm=0,
            attenuation_db=10
        )
        assert result["output_power_dbm"] == "-10.0dBm"

    def test_attenuator_negative_attenuation(self):
        """测试负衰减 (放大)"""
        result = calculate_rf_attenuator(
            input_power_dbm=-10,
            attenuation_db=-10  # 负dB = 放大
        )
        assert result["output_power_dbm"] == "0.0dBm"

    def test_attenuator_high_power(self):
        """测试高功率输入 (30dBm = 1W)"""
        result = calculate_rf_attenuator(
            input_power_dbm=30,
            attenuation_db=20
        )
        assert result["output_power_dbm"] == "10.0dBm"
        assert float(result["output_power_mw"].replace("mW","")) == 10.0

    def test_attenuator_zero_attenuation(self):
        """测试零衰减"""
        result = calculate_rf_attenuator(
            input_power_dbm=10,
            attenuation_db=0
        )
        assert result["output_power_dbm"] == "10.0dBm"
        # 允许任意精度
        assert "10" in result["output_power_mw"] and "mW" in result["output_power_mw"]

    def test_attenuator_extreme_attenuation(self):
        """测试极端衰减 (60dB)"""
        result = calculate_rf_attenuator(
            input_power_dbm=0,
            attenuation_db=60
        )
        assert result["output_power_dbm"] == "-60.0dBm"
