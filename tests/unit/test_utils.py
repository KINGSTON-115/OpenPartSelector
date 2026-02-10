
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
    
    def test_parse_voltage_single(self):
        """测试电压解析 - 单值"""
        from ops.utils import parse_voltage
        result = parse_voltage("3.3V")
        assert result["nominal"] == 3.3
        assert result["min"] == 3.3
        assert result["max"] == 3.3
    
    def test_parse_voltage_range(self):
        """测试电压解析 - 范围"""
        from ops.utils import parse_voltage
        result = parse_voltage("3.3~12V")
        assert result["min"] == 3.3
        assert result["max"] == 12.0
    
    def test_parse_current_ma(self):
        """测试电流解析 - mA"""
        from ops.utils import parse_current
        result = parse_current("500mA")
        assert result["value"] == 0.5
        assert result["unit"] == "A"
    
    def test_parse_current_ua(self):
        """测试电流解析 - uA"""
        from ops.utils import parse_current
        result = parse_current("100uA")
        assert result["value"] == 0.0001
        assert result["unit"] == "A"
    
    def test_estimate_price_basic(self):
        """测试价格估算"""
        from ops.utils import estimate_price
        result = estimate_price("STM32F103", quantity=100)
        assert "unit_price" in result
        assert "bulk_price" in result
        assert result["quantity"] == 100
    
    def test_estimate_price_discount(self):
        """测试批量折扣"""
        from ops.utils import estimate_price
        retail = estimate_price("ESP32", quantity=1)
        bulk = estimate_price("ESP32", quantity=1000)
        assert bulk["unit_price"] < retail["unit_price"]
    
    def test_bom_builder(self):
        """测试 BOM 构建器"""
        from ops.utils import BomBuilder
        builder = BomBuilder()
        builder.add_item("STM32F103", quantity=10, manufacturer="ST", price=2.5)
        builder.add_item("CH340N", quantity=5, manufacturer="WCH", price=0.5)
        
        bom = builder.get_bom()
        assert bom["total_items"] == 2
        assert bom["total_estimated_cost"] == 27.5  # 10*2.5 + 5*0.5
    
    def test_bom_export_csv(self):
        """测试 BOM CSV 导出"""
        from ops.utils import BomBuilder
        builder = BomBuilder()
        builder.add_item("LD1117", quantity=1, price=0.3)
        
        csv = builder.export_csv()
        assert "LD1117" in csv
        assert "Reference,Part Number" in csv
    
    def test_generate_bom_id(self):
        """测试 BOM ID 生成"""
        from ops.utils import generate_bom_id
        id1 = generate_bom_id()
        id2 = generate_bom_id()
        assert len(id1) == 8
        assert id1 != id2  # 应该生成不同的 ID
