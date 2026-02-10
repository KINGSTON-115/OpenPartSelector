"""
工具函数模块
"""
import logging
import re
from datetime import datetime
from typing import Any, Dict
import json

# 日志配置
def setup_logging(
    level: int = logging.INFO,
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> logging.Logger:
    """配置日志"""
    logging.basicConfig(level=level, format=format)
    return logging.getLogger(__name__)


def format_timestamp(ts: str = None, format: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
    """格式化时间戳"""
    if ts is None:
        from datetime import timezone
        ts = datetime.now(timezone.utc)
    elif isinstance(ts, str):
        ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    
    return ts.strftime(format)


def parse_voltage(voltage_str: str) -> Dict[str, float]:
    """
    解析电压字符串
    
    Args:
        voltage_str: 如 "3.3V", "5V", "3.3~12V"
        
    Returns:
        {"min": float, "max": float, "nominal": float}
    """
    result = {"min": 0.0, "max": 0.0, "nominal": 0.0}
    
    if not voltage_str:
        return result
    
    # 清理字符串
    voltage_str = voltage_str.upper().replace("V", "").replace(" ", "")
    
    # 范围格式 (3.3~12)
    if "~" in voltage_str or "-" in voltage_str:
        parts = re.split(r"[~-]", voltage_str)
        if len(parts) == 2:
            try:
                result["min"] = float(parts[0])
                result["max"] = float(parts[1])
                result["nominal"] = (result["min"] + result["max"]) / 2
            except ValueError:
                pass
    else:
        # 单值格式
        try:
            value = float(voltage_str)
            result["nominal"] = value
            result["min"] = value
            result["max"] = value
        except ValueError:
            pass
    
    return result


def parse_current(current_str: str) -> Dict[str, float]:
    """
    解析电流字符串
    
    Returns:
        {"value": float, "unit": str}
    """
    if not current_str:
        return {"value": 0.0, "unit": "A"}
    
    # 提取数值和单位
    match = re.match(r"([0-9.]+)\s*([mMuU]?A)", current_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        
        # 标准化为 A
        if unit == "mA":
            value = value / 1000
        elif unit == "uA":
            value = value / 1000000
        
        return {"value": value, "unit": "A"}
    
    return {"value": 0.0, "unit": "A"}


def parse_resistance(resistance_str: str) -> Dict[str, Any]:
    """
    解析电阻值字符串
    
    Args:
        resistance_str: 如 "10kΩ", "1M", "4.7K", "100R"
        
    Returns:
        {"value": float, "unit": str, "ohms": float}
    """
    if not resistance_str:
        return {"value": 0.0, "unit": "Ω", "ohms": 0.0}
    
    # 清理字符串，提取数值和单位
    match = re.match(r"([0-9.]+)\s*([kKmMµuU]?)Ω?", resistance_str)
    if not match:
        # 尝试无单位格式
        match = re.match(r"([0-9.]+)([kKmMµuU]?)", resistance_str.replace("R", "", 1))
    
    if match:
        value = float(match.group(1))
        unit = match.group(2).upper()
        
        # 标准化为欧姆
        ohms = value
        if unit == "K":
            ohms = value * 1000
            unit = "kΩ"
        elif unit == "M":
            ohms = value * 1000000
            unit = "MΩ"
        elif unit == "U" or unit == "µ":
            ohms = value / 1000000
            unit = "MΩ"
        elif not unit or unit == "R":
            unit = "Ω"
        
        return {"value": value, "unit": unit, "ohms": ohms}
    
    return {"value": 0.0, "unit": "Ω", "ohms": 0.0}


def celsius_to_fahrenheit(celsius: float) -> float:
    """摄氏转华氏"""
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """华氏转摄氏"""
    return (fahrenheit - 32) * 5/9


def estimate_price(part_number: str = "", quantity: int = 1) -> Dict[str, Any]:
    """
    估算器件价格 (基于器件类型和数量)
    
    Args:
        part_number: 器件型号，用于识别器件类型
        quantity: 采购数量
        
    Returns:
        {
            "unit_price": float,      # 单价
            "bulk_price": float,     # 批量价
            "tier_discount": str,     # 折扣等级
            "price_tier": str         # 价格区间
        }
    """
    # 器件类型基础价格映射
    BASE_PRICES = {
        # MCU/Processor
        "esp32": 3.50, "esp8266": 2.00, "stm32": 4.00, "rp2040": 2.50,
        "atmega": 2.00, "attiny": 1.00, "avr": 1.50, "pic": 2.50,
        # 电源芯片
        "lm7805": 0.30, "lm1117": 0.25, " AMS1117": 0.20, "tp4056": 0.50,
        "lm2596": 0.40, "mp2359": 0.45, "xl6009": 0.55,
        # 接口芯片
        "ch340": 0.35, "ch341": 0.50, "cp2102": 0.60, "ft232": 1.20,
        "pl2303": 0.30, "usb3300": 0.80,
        # 传感器
        "dht11": 0.80, "dht22": 1.20, "ds18b20": 0.90, "bmp280": 0.70,
        "bme280": 1.50, "mpu6050": 1.00, "bh1750": 0.60, "hc-sr04": 0.75,
        # 通信模块
        "nrf24": 1.00, "hc-05": 1.20, "hc-06": 1.00, "esp8266": 2.00,
        "sim800": 3.50, "a6": 2.80,
        # 显示
        "oled": 2.00, "lcd1602": 1.50, "tft": 5.00, "ws2812": 0.15,
        # 被动器件
        "resistor": 0.01, "capacitor": 0.02, "inductor": 0.05, "led": 0.03,
    }
    
    # 识别器件类型
    part_lower = (part_number or "").lower()
    base_price = 0.50  # 默认基础价格
    
    for key, price in BASE_PRICES.items():
        if key in part_lower:
            base_price = price
            break
    
    # 数量折扣
    if quantity >= 10000:
        discount = 0.50  # 50% off
        tier = "大批量"
    elif quantity >= 1000:
        discount = 0.65  # 35% off
        tier = "批量"
    elif quantity >= 100:
        discount = 0.80  # 20% off
        tier = "中量"
    elif quantity >= 10:
        discount = 0.90  # 10% off
        tier = "小量"
    else:
        discount = 1.0
        tier = "零售"
    
    unit_price = round(base_price * discount, 3)
    bulk_price = round(unit_price * quantity, 2)
    
    # 价格区间
    if unit_price < 0.1:
        price_range = "低价 (< ¥1)"
    elif unit_price < 1:
        price_range = "经济 (¥1-10)"
    elif unit_price < 5:
        price_range = "中端 (¥10-50)"
    else:
        price_range = "高端 (> ¥50)"
    
    return {
        "unit_price": unit_price,
        "bulk_price": bulk_price,
        "tier_discount": f"{int((1-discount)*100)}%",
        "price_tier": price_range,
        "quantity": quantity,
        "part_type_detected": part_lower[:20] if part_lower else "unknown"
    }


def generate_bom_id() -> str:
    """生成 BOM ID"""
    import hashlib
    from datetime import timezone
    timestamp = str(datetime.now(timezone.utc).timestamp())
    return hashlib.md5(timestamp.encode()).hexdigest()[:8].upper()


class BomBuilder:
    """BOM 构建器"""
    
    def __init__(self):
        self.items = []
    
    def add_item(
        self,
        part_number: str,
        quantity: int = 1,
        reference: str = "",
        manufacturer: str = "",
        description: str = "",
        price: float = 0.0
    ):
        """添加 BOM 项目"""
        self.items.append({
            "part_number": part_number,
            "quantity": quantity,
            "reference": reference or f"U{len(self.items) + 1}",
            "manufacturer": manufacturer,
            "description": description,
            "unit_price": price,
            "total_price": price * quantity
        })
    
    def get_bom(self) -> Dict:
        """获取完整 BOM"""
        total = sum(item["total_price"] for item in self.items)
        
        return {
            "items": self.items,
            "total_items": len(self.items),
            "total_estimated_cost": round(total, 2),
            "generated_at": format_timestamp()
        }
    
    def export_csv(self) -> str:
        """导出 CSV 格式"""
        lines = ["Reference,Part Number,Quantity,Manufacturer,Description,Unit Price,Total Price"]
        
        for item in self.items:
            lines.append(
                f"{item['reference']},{item['part_number']},{item['quantity']},"
                f"{item['manufacturer']},{item['description']},"
                f"{item['unit_price']:.4f},{item['total_price']:.4f}"
            )
        
        return "\n".join(lines)
