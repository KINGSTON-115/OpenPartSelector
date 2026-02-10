
class TestUtilsNewFunctions:
    """测试新增工具函数"""
    
    def test_parse_resistance_ohms(self):
        """测试电阻解析 - 欧姆"""
        from ops.utils import parse_resistance
        result = parse_resistance("100R")
        assert result["value"] == 100.0
        assert result["unit"] == "Ω"
        assert result["ohms"] == 100.0
    
    def test_parse_resistance_kohms(self):
        """测试电阻解析 - 千欧"""
        from ops.utils import parse_resistance
        result = parse_resistance("10kΩ")
        assert result["value"] == 10.0
        assert result["unit"] == "kΩ"
        assert result["ohms"] == 10000.0
    
    def test_parse_resistance_mohms(self):
        """测试电阻解析 - 兆欧"""
        from ops.utils import parse_resistance
        result = parse_resistance("1M")
        assert result["value"] == 1.0
        assert result["unit"] == "MΩ"
        assert result["ohms"] == 1000000.0
    
    def test_celsius_to_fahrenheit(self):
        """测试摄氏转华氏"""
        from ops.utils import celsius_to_fahrenheit
        assert celsius_to_fahrenheit(0) == 32.0
        assert celsius_to_fahrenheit(100) == 212.0
        assert celsius_to_fahrenheit(25) == 77.0
    
    def test_fahrenheit_to_celsius(self):
        """测试华氏转摄氏"""
        from ops.utils import fahrenheit_to_celsius
        assert fahrenheit_to_celsius(32) == 0.0
        assert fahrenheit_to_celsius(212) == 100.0
        assert fahrenheit_to_celsius(77) == 25.0
