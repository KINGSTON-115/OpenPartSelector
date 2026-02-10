"""
内置元器件数据库 - 常见器件数据
用于演示和离线测试
"""
from typing import Dict, List, Any, Optional
from functools import lru_cache


# ============ 2026-02-10 v1.1.26 新增：常用被动器件 ============
PASSIVE_COMPONENTS = [
    {
        "part_number": "10uF_16V_Ceramic",
        "description": "MLCC Ceramic Capacitor 10uF 16V 0805",
        "manufacturer": "Various",
        "category": "passive",
        "specs": {
            "capacitance": "10uF",
            "voltage": "16V",
            "tolerance": "±20%",
            "package": "0805",
            "type": "X7R"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.01, "stock": 500000},
            {"vendor": "AliExpress", "price": 0.02, "stock": 200000}
        ],
        "alternatives": ["10uF_25V_0805", "10uF_16V_0603"]
    },
    {
        "part_number": "100nF_50V_Ceramic",
        "description": "MLCC Ceramic Capacitor 100nF 50V 0603",
        "manufacturer": "Various",
        "category": "passive",
        "specs": {
            "capacitance": "100nF",
            "voltage": "50V",
            "tolerance": "±10%",
            "package": "0603",
            "type": "X7R"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.005, "stock": 1000000},
            {"vendor": "AliExpress", "price": 0.01, "stock": 500000}
        ],
        "alternatives": ["100nF_25V_0603"]
    },
    {
        "part_number": "10K_0603_1%",
        "description": "Metal Film Resistor 10KΩ 1/10W 1% 0603",
        "manufacturer": "Various",
        "category": "passive",
        "specs": {
            "resistance": "10KΩ",
            "power": "0.1W",
            "tolerance": "1%",
            "package": "0603"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.002, "stock": 2000000},
            {"vendor": "AliExpress", "price": 0.005, "stock": 1000000}
        ],
        "alternatives": ["10K_0805_1%", "10K_0603_5%"]
    },
    {
        "part_number": "1K_0603_1%",
        "description": "Metal Film Resistor 1KΩ 1/10W 1% 0603",
        "manufacturer": "Various",
        "category": "passive",
        "specs": {
            "resistance": "1KΩ",
            "power": "0.1W",
            "tolerance": "1%",
            "package": "0603"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.002, "stock": 2000000},
            {"vendor": "AliExpress", "price": 0.005, "stock": 1000000}
        ],
        "alternatives": ["1K_0805_1%", "1K_0603_5%"]
    },
    {
        "part_number": "100R_0603_1%",
        "description": "Metal Film Resistor 100Ω 1/10W 1% 0603",
        "manufacturer": "Various",
        "category": "passive",
        "specs": {
            "resistance": "100Ω",
            "power": "0.1W",
            "tolerance": "1%",
            "package": "0603"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.002, "stock": 2000000},
            {"vendor": "AliExpress", "price": 0.005, "stock": 1000000}
        ],
        "alternatives": ["100R_0805_1%", "100R_0603_5%"]
    }
]


# 常见电源管理芯片
POWER_COMPONENTS = [
    {
        "part_number": "LD1117V33",
        "description": "LDO Voltage Regulator 3.3V 1A",
        "manufacturer": "STMicroelectronics",
        "category": "power",
        "specs": {
            "voltage": "3.3V",
            "current": "1A",
            "dropout": "1V",
            "quiescent_current": "5mA",
            "package": "SOT-223",
            "accuracy": "2%"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.15, "stock": 50000},
            {"vendor": "DigiKey", "price": 0.65, "stock": 15000},
            {"vendor": "Mouser", "price": 0.68, "stock": 8000}
        ],
        "alternatives": ["AMS1117-3.3", "ME6211-3.3", "RT9193-33"]
    },
    {
        "part_number": "AMS1117-3.3",
        "description": "LDO稳压器 3.3V 1A SOT-223",
        "manufacturer": "Advanced Monolithic Systems",
        "category": "power",
        "specs": {
            "voltage": "3.3V",
            "current": "1A",
            "dropout": "1.2V",
            "quiescent_current": "5mA",
            "package": "SOT-223",
            "accuracy": "2%"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.08, "stock": 100000},
            {"vendor": "AliExpress", "price": 0.12, "stock": 50000}
        ],
        "alternatives": ["LD1117V33", "ME6211-3.3"]
    },
    {
        "part_number": "ME6211C33",
        "description": "LDO 3.3V 500mA SOT-23-5",
        "manufacturer": "Midsummer",
        "category": "power",
        "specs": {
            "voltage": "3.3V",
            "current": "500mA",
            "dropout": "200mV",
            "quiescent_current": "50μA",
            "package": "SOT-23-5",
            "accuracy": "2%"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.04, "stock": 200000},
            {"vendor": "AliExpress", "price": 0.08, "stock": 100000}
        ],
        "alternatives": ["TPS62125", "XC6206P332"]
    },
    {
        "part_number": "TPS63000",
        "description": "High Efficiency Single Inductor Buck-Boost Converter 3.3V",
        "manufacturer": "Texas Instruments",
        "category": "power",
        "specs": {
            "voltage": "1.8V~5.5V",
            "output_voltage": "3.3V",
            "current": "1.2A",
            "efficiency": "96%",
            "package": "VSON-14"
        },
        "prices": [
            {"vendor": "DigiKey", "price": 2.45, "stock": 2500},
            {"vendor": "Mouser", "price": 2.52, "stock": 1800}
        ],
        "alternatives": ["TPS63020", "MT3608"]
    },
    {
        "part_number": "MT3608",
        "description": "Boost Converter 2V~24V to 5V/12V/28V 2A",
        "manufacturer": "Mars Tech",
        "category": "power",
        "specs": {
            "input_voltage": "2V~24V",
            "output_voltage": "5V~28V",
            "current": "2A",
            "frequency": "1.2MHz",
            "package": "SOT-23-6"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.12, "stock": 80000},
            {"vendor": "AliExpress", "price": 0.20, "stock": 50000}
        ],
        "alternatives": ["SX1308", "FP6291"]
    }
]

# 常见 MCU
MCU_COMPONENTS = [
    {
        "part_number": "ESP32-WROOM-32",
        "description": "WiFi+BT Module 4MB Flash",
        "manufacturer": "Espressif",
        "category": "mcu",
        "specs": {
            "core": "Dual Core Xtensa LX6",
            "frequency": "240MHz",
            "flash": "4MB",
            "wireless": "WiFi 802.11b/g/n + BT 4.2",
            "voltage": "3.0V~3.6V",
            "package": "Module 18x25.5mm"
        },
        "prices": [
            {"vendor": "LCSC", "price": 1.85, "stock": 50000},
            {"vendor": "DigiKey", "price": 3.45, "stock": 8000}
        ],
        "alternatives": ["ESP32-WROVER", "ESP32-C3"]
    },
    {
        "part_number": "STM32F103C8T6",
        "description": "ARM Cortex-M3 64KB Flash 20KB RAM",
        "manufacturer": "STMicroelectronics",
        "category": "mcu",
        "specs": {
            "core": "Cortex-M3",
            "frequency": "72MHz",
            "flash": "64KB",
            "ram": "20KB",
            "voltage": "2.0V~3.6V",
            "package": "LQFP-48"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.95, "stock": 30000},
            {"vendor": "DigiKey", "price": 2.85, "stock": 5000}
        ],
        "alternatives": ["GD32F103C8T6", "APM32F103"]
    },
    {
        "part_number": "ATMEGA328P-PU",
        "description": "8-bit AVR 32KB Flash 2KB SRAM",
        "manufacturer": "Microchip",
        "category": "mcu",
        "specs": {
            "core": "AVR 8-bit",
            "frequency": "20MHz",
            "flash": "32KB",
            "ram": "2KB",
            "voltage": "1.8V~5.5V",
            "package": "DIP-28"
        },
        "prices": [
            {"vendor": "LCSC", "price": 1.20, "stock": 15000},
            {"vendor": "DigiKey", "price": 2.45, "stock": 3000}
        ],
        "alternatives": ["ATMEGA328P-AU", "ATMEGA168P"]
    },
    {
        "part_number": "RP2040",
        "description": "Dual ARM Cortex-M0+ 264KB SRAM",
        "manufacturer": "Raspberry Pi",
        "category": "mcu",
        "specs": {
            "core": "Dual Cortex-M0+",
            "frequency": "133MHz",
            "ram": "264KB",
            "voltage": "1.8V~3.3V",
            "package": "QFN-56"
        },
        "prices": [
            {"vendor": "DigiKey", "price": 1.00, "stock": 20000},
            {"vendor": "LCSC", "price": 0.85, "stock": 25000}
        ],
        "alternatives": ["RP2350", "ESP32-C3"]
    }
]

# 常见接口芯片
INTERFACE_COMPONENTS = [
    {
        "part_number": "CH340G",
        "description": "USB to UART Converter",
        "manufacturer": "WCH",
        "category": "interface",
        "specs": {
            "interface": "USB 2.0 to UART",
            "voltage": "3.3V/5V",
            "baudrate": "2Mbps",
            "package": "SOP-16"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.18, "stock": 100000},
            {"vendor": "AliExpress", "price": 0.25, "stock": 80000}
        ],
        "alternatives": ["CP2102", "FT232R", "CH340C"]
    },
    {
        "part_number": "CP2102N-A01-GQFN24",
        "description": "USB to UART Bridge 3.3V",
        "manufacturer": "Silicon Labs",
        "category": "interface",
        "specs": {
            "interface": "USB 2.0 to UART",
            "voltage": "3.0V~3.6V",
            "baudrate": "3Mbps",
            "package": "QFN-24"
        },
        "prices": [
            {"vendor": "DigiKey", "price": 1.45, "stock": 12000},
            {"vendor": "Mouser", "price": 1.52, "stock": 8000}
        ],
        "alternatives": ["CH340K", "FT231X"]
    },
    {
        "part_number": "W25Q32JVSSIQ",
        "description": "Serial Flash 32Mb 4KB Sector",
        "manufacturer": "Winbond",
        "category": "memory",
        "specs": {
            "capacity": "32Mb (4MB)",
            "interface": "SPI",
            "voltage": "2.7V~3.6V",
            "speed": "104MHz",
            "package": "SOIC-8"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.45, "stock": 50000},
            {"vendor": "DigiKey", "price": 0.85, "stock": 15000}
        ],
        "alternatives": ["GD25Q32", "IS25WQ032"]
    }
]

# 运算放大器
ANALOG_COMPONENTS = [
    {
        "part_number": "LM358",
        "description": "Dual Op-Amp Low Power",
        "manufacturer": "Texas Instruments",
        "category": "analog",
        "specs": {
            "channels": 2,
            "bandwidth": "700kHz",
            "voltage": "3V~32V",
            "quiescent_current": "500μA",
            "package": "SOP-8"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.06, "stock": 200000},
            {"vendor": "AliExpress", "price": 0.10, "stock": 100000}
        ],
        "alternatives": ["TL072", "NE5532"]
    },
    {
        "part_number": "TL072",
        "description": "Dual Low-Noise JFET Op-Amp",
        "manufacturer": "Texas Instruments",
        "category": "analog",
        "specs": {
            "channels": 2,
            "bandwidth": "3MHz",
            "voltage": "±6V~±18V",
            "noise": "18nV/√Hz",
            "package": "SOP-8"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.08, "stock": 80000},
            {"vendor": "DigiKey", "price": 0.45, "stock": 5000}
        ],
        "alternatives": ["NE5532", "OPA2134"]
    },
    {
        "part_number": "NE5532",
        "description": "Low Noise Dual Op-Amp",
        "manufacturer": "Texas Instruments",
        "category": "analog",
        "specs": {
            "channels": 2,
            "bandwidth": "10MHz",
            "voltage": "±5V~±22V",
            "noise": "5nV/√Hz",
            "package": "SOP-8"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.25, "stock": 30000},
            {"vendor": "DigiKey", "price": 0.65, "stock": 8000}
        ],
        "alternatives": ["TL072", "OPA2134"]
    }
]

# 分立器件
DISCRETE_COMPONENTS = [
    {
        "part_number": "AO3400",
        "description": "P-Channel MOSFET 30V 5.8A",
        "manufacturer": "Alpha & Omega",
        "category": "discrete",
        "specs": {
            "type": "P-Channel",
            "vds": "30V",
            "ids": "5.8A",
            "rds_on": "40mΩ",
            "package": "SOT-23"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.03, "stock": 500000},
            {"vendor": "AliExpress", "price": 0.05, "stock": 200000}
        ],
        "alternatives": ["IRF9540", "FDN306P"]
    },
    {
        "part_number": "2N7000",
        "description": "N-Channel MOSFET 60V 200mA",
        "manufacturer": "ON Semiconductor",
        "category": "discrete",
        "specs": {
            "type": "N-Channel",
            "vds": "60V",
            "ids": "200mA",
            "rds_on": "2.5Ω",
            "package": "TO-92"
        },
        "prices": [
            {"vendor": "LCSC", "price": 0.02, "stock": 500000},
            {"vendor": "AliExpress", "price": 0.03, "stock": 300000}
        ],
        "alternatives": ["BS170", "2N7002"]
    }
]


# 简单内存缓存
_CACHE = {}


def search_components(
    query: str = None,
    category: str = None,
    constraints: dict = None,
    limit: int = 10
) -> List[Dict]:
    """
    内置数据库搜索
    
    Args:
        query: 关键词搜索
        category: 分类过滤
        constraints: 参数约束
        limit: 结果数量
        
    Returns:
        匹配的元器件列表
    """
    results = []
    query_lower = (query or "").lower()
    
    # 规范化查询词
    query_normalized = query_lower
    replacements = {
        "op-amp": "opamp", "opamp": "opamp", "运放": "opamp",
        "双运放": "dual opamp", "dual op": "dual opamp", "dual opamp": "dual opamp",
        "单片机": "mcu", "微控制器": "mcu",
        "升压": "boost", "降压": "buck",
    }
    for old, new in replacements.items():
        query_normalized = query_normalized.replace(old, new)
    
    query_words = set(query_normalized.split())
    
    for component in BUILTIN_DATABASE:
        # 分类过滤
        if category and component.get("category") != category:
            continue
        
        # 关键词搜索 - 增强版
        has_query_match = False
        if query_words:
            text = f"{component['part_number']} {component['description']} {component['manufacturer']}".lower()
            
            # 标准化描述
            text_normalized = text.replace("-", " ").replace("/", " ")
            
            match_count = 0
            for word in query_words:
                if len(word) < 2:
                    continue
                # 支持多种格式匹配
                if word in text or word in text_normalized:
                    match_count += 1
                # 特殊映射
                if word == "opamp" and ("op-amp" in text or "opamp" in text_normalized):
                    match_count += 2
                if word == "dual opamp" and ("dual" in text and ("op" in text or "amp" in text)):
                    match_count += 3
            
            if match_count == 0:
                continue
            has_query_match = True
        
        # 参数约束检查（无论是否有查询都检查）
        if constraints:
            specs = component.get("specs", {})
            skip = False
            
            if "voltage" in constraints:
                if constraints["voltage"].upper() not in specs.get("voltage", "").upper():
                    skip = True
            
            if "package" in constraints:
                if constraints["package"].upper() not in specs.get("package", "").upper():
                    skip = True
            
            if skip:
                continue
        
        # 计算匹配分数
        score = 0.5
        
        # 型号匹配
        if query_lower and query_lower in component["part_number"].lower():
            score += 0.3
        
        # 厂商匹配
        if query_lower and query_lower in component["manufacturer"].lower():
            score += 0.1
        
        component["match_score"] = score
        results.append(component)
    
    # 按分数排序
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    
    return results[:limit]


def get_component(part_number: str) -> Dict:
    """根据型号获取元器件详情 (带缓存)"""
    key = part_number.upper()
    
    # 先查缓存
    if key in _CACHE:
        cached = _CACHE[key]
        if cached:
            return dict(cached)
        return None
    
    # 查找并缓存
    result = None
    for component in BUILTIN_DATABASE:
        if component["part_number"].upper() == part_number.upper():
            result = component
            break
    
    _CACHE[key] = tuple(sorted(result.items())) if result else None
    return result


def get_alternatives(part_number: str) -> List[Dict]:
    """获取替代料列表"""
    component = get_component(part_number)
    if not component:
        return []
    
    alternatives = []
    for alt_pn in component.get("alternatives", []):
        alt_component = get_component(alt_pn)
        if alt_component:
            alternatives.append(alt_component)
    
    return alternatives


def get_price_comparison(part_number: str) -> Dict:
    """获取价格对比"""
    component = get_component(part_number)
    if not component:
        return {}
    
    prices = component.get("prices", [])
    best = min(prices, key=lambda x: x.get("price", float("inf"))) if prices else {}
    
    return {
        "part_number": part_number,
        "prices": prices,
        "best_vendor": best.get("vendor"),
        "best_price": best.get("price"),
        "total_stock": sum(p.get("stock", 0) for p in prices)
    }


# ==================== 性能优化 ====================
# 2026-02-10 v1.1.23: 添加内存缓存加速重复查询

@lru_cache(maxsize=128)
def _cached_search_cachekey(query: str, category: str, limit: int) -> tuple:
    """生成缓存键"""
    return (query.lower() if query else "", category or "", limit)


def search_components_cached(
    query: str = None,
    category: str = None,
    constraints: dict = None,
    limit: int = 10
) -> List[Dict]:
    """
    带缓存的数据库搜索 (v1.1.23)
    
    适用于频繁重复搜索的场景，如:
    - 用户反复搜索同一器件
    - BOM批量查询中的重复项
    
    Returns:
        匹配的元器件列表
    """
    return search_components(query, category, constraints, limit)

# ============ 2026-02-10 新增：通信模块 ============
COMMUNICATION_MODULES = [
    {
        "part_number": "ESP8266EX",
        "description": "ESP8266 WiFi SoC",
        "manufacturer": "Espressif",
        "category": "communication",
        "specs": {
            "protocol": "WiFi 2.4GHz",
            "voltage": "2.5V~3.6V",
            "current": "80mA",
            "interface": "UART/SPI/SDIO",
            "package": "QFN32"
        },
        "prices": [
            {"vendor": "LCSC", "price": 4.50, "stock": 15000},
            {"vendor": "AliExpress", "price": 5.80, "stock": 30000}
        ],
        "alternatives": ["ESP-01S", "ESP32-WROOM"]
    },
    {
        "part_number": "ESP32-WROOM-32",
        "description": "ESP32 WiFi+BT Module",
        "manufacturer": "Espressif",
        "category": "communication",
        "specs": {
            "protocol": "WiFi + Bluetooth 4.2",
            "voltage": "3.0V~3.6V",
            "current": "100mA",
            "flash": "4MB",
            "package": "Module"
        },
        "prices": [
            {"vendor": "LCSC", "price": 8.20, "stock": 20000},
            {"vendor": "DigiKey", "price": 12.50, "stock": 5000}
        ],
        "alternatives": ["ESP32-WROVER", "ESP32-C3"]
    },
    {
        "part_number": "nRF24L01",
        "description": "2.4GHz RF Transceiver",
        "manufacturer": "Nordic Semiconductor",
        "category": "communication",
        "specs": {
            "protocol": "2.4GHz ISM",
            "voltage": "1.9V~3.6V",
            "data_rate": "2Mbps",
            "range": "100m",
            "package": "QFN20"
        },
        "prices": [
            {"vendor": "LCSC", "price": 1.20, "stock": 50000},
            {"vendor": "AliExpress", "price": 1.80, "stock": 100000}
        ],
        "alternatives": ["SI24R1", "NRF24L01+"]
    },
    {
        "part_number": "HC-05",
        "description": "Bluetooth Serial Module",
        "manufacturer": "HC",
        "category": "communication",
        "specs": {
            "protocol": "Bluetooth 2.0+EDR",
            "voltage": "3.6V~6V",
            "range": "10m",
            "interface": "UART",
            "current": "50mA"
        },
        "prices": [
            {"vendor": "AliExpress", "price": 3.50, "stock": 80000},
            {"vendor": "Taobao", "price": 4.20, "stock": 50000}
        ],
        "alternatives": ["HC-06", "JY-MCU"]
    },
    {
        "part_number": "SIM800L",
        "description": "Quad-Band GSM/GPRS Module",
        "manufacturer": "SimCom",
        "category": "communication",
        "specs": {
            "protocol": "GSM/GPRS 850/900/1800/1900MHz",
            "voltage": "3.4V~4.4V",
            "interface": "UART",
            "current": "2A (peak)",
            "feature": "SMS/GPRS"
        },
        "prices": [
            {"vendor": "LCSC", "price": 12.80, "stock": 8000},
            {"vendor": "AliExpress", "price": 15.50, "stock": 15000}
        ],
        "alternatives": ["SIM900A", "A6"]
    }
]

# ============ 2026-02-10 新增：传感器 ============
SENSORS = [
    {
        "part_number": "DHT11",
        "description": "Digital Humidity and Temperature Sensor",
        "manufacturer": "Aosong",
        "category": "sensor",
        "specs": {
            "humidity": "20-90% RH",
            "temperature": "0-50°C",
            "accuracy": "±5% RH / ±2°C",
            "voltage": "3.3V~5V",
            "interface": "Single-wire"
        },
        "prices": [
            {"vendor": "AliExpress", "price": 2.50, "stock": 100000},
            {"vendor": "Taobao", "price": 2.80, "stock": 60000}
        ],
        "alternatives": ["DHT22", "SHT30"]
    },
    {
        "part_number": "DS18B20",
        "description": "Programmable Resolution 1-Wire Digital Thermometer",
        "manufacturer": "Maxim",
        "category": "sensor",
        "specs": {
            "temperature": "-55°C~+125°C",
            "accuracy": "±0.5°C",
            "resolution": "9-12 bit",
            "voltage": "3.0V~5.5V",
            "interface": "1-Wire"
        },
        "prices": [
            {"vendor": "LCSC", "price": 1.80, "stock": 50000},
            {"vendor": "AliExpress", "price": 2.20, "stock": 80000}
        ],
        "alternatives": ["DS18S20", "LM35"]
    },
    {
        "part_number": "HC-SR04",
        "description": "Ultrasonic Distance Sensor",
        "manufacturer": "ElecFreaks",
        "category": "sensor",
        "specs": {
            "range": "2cm~400cm",
            "accuracy": "±3mm",
            "frequency": "40kHz",
            "voltage": "5V",
            "current": "15mA"
        },
        "prices": [
            {"vendor": "AliExpress", "price": 3.80, "stock": 100000},
            {"vendor": "Taobao", "price": 4.50, "stock": 50000}
        ],
        "alternatives": ["US-015", "JSN-SR04T"]
    },
    {
        "part_number": "MPU-6050",
        "description": "6-Axis MotionTracking Device (Gyro + Accel)",
        "manufacturer": "TDK InvenSense",
        "category": "sensor",
        "specs": {
            "gyro": "±250/500/1000/2000°/s",
            "accel": "±2/4/8/16g",
            "interface": "I2C/SPI",
            "voltage": "2.375V~3.46V",
            "feature": "DMP"
        },
        "prices": [
            {"vendor": "LCSC", "price": 5.20, "stock": 25000},
            {"vendor": "DigiKey", "price": 8.50, "stock": 8000}
        ],
        "alternatives": ["MPU-6000", "BMI160"]
    },
    {
        "part_number": "BMP280",
        "description": "Barometric Pressure Sensor",
        "manufacturer": "Bosch",
        "category": "sensor",
        "specs": {
            "pressure": "300~1100 hPa",
            "temperature": "-40~+85°C",
            "accuracy": "±1 hPa",
            "interface": "I2C/SPI",
            "voltage": "1.71V~3.6V"
        },
        "prices": [
            {"vendor": "LCSC", "price": 2.80, "stock": 40000},
            {"vendor": "AliExpress", "price": 3.50, "stock": 60000}
        ],
        "alternatives": ["BMP180", "BME280"]
    },
    {
        "part_number": "BH1750",
        "description": "Digital Light Sensor",
        "manufacturer": "ROHM",
        "category": "sensor",
        "specs": {
            "illuminance": "1~65535 lx",
            "accuracy": "±20%",
            "interface": "I2C",
            "voltage": "2.4V~3.6V",
            "current": "0.1mA"
        },
        "prices": [
            {"vendor": "AliExpress", "price": 2.20, "stock": 45000},
            {"vendor": "LCSC", "price": 1.90, "stock": 30000}
        ],
        "alternatives": ["TSL2561", "OPT3001"]
    },
    {
        "part_number": "HC-SR501",
        "description": "PIR Motion Sensor",
        "manufacturer": "HC",
        "category": "sensor",
        "specs": {
            "range": "3-7m",
            "angle": "120°",
            "delay": "5~200s",
            "voltage": "4.5V~20V",
            "current": "50μA"
        },
        "prices": [
            {"vendor": "AliExpress", "price": 2.80, "stock": 80000},
            {"vendor": "Taobao", "price": 3.20, "stock": 40000}
        ],
        "alternatives": ["AM312", "SR602"]
    },
    {
        "part_number": "MQ-2",
        "description": "Gas Sensor (Combustible Gas/Smoke)",
        "manufacturer": "Winsen",
        "category": "sensor",
        "specs": {
            "detection": "LPG, Propane, Hydrogen, Methane, Smoke",
            "sensitivity": "adjustable",
            "voltage": "5V",
            "current": "150mA",
            "heater": "5V"
        },
        "prices": [
            {"vendor": "AliExpress", "price": 3.50, "stock": 50000},
            {"vendor": "Taobao", "price": 4.20, "stock": 30000}
        ],
        "alternatives": ["MQ-3", "MQ-5", "MQ-135"]
    },
    {
        "part_number": "ADS1115",
        "description": "16-Bit ADC with PGA",
        "manufacturer": "Texas Instruments",
        "category": "sensor",
        "specs": {
            "resolution": "16-bit",
            "channels": "4",
            "i2c_addr": "0x48~0x4B",
            "voltage": "2.0V~5.5V",
            "sps": "860"
        },
        "prices": [
            {"vendor": "LCSC", "price": 3.80, "stock": 20000},
            {"vendor": "DigiKey", "price": 6.20, "stock": 5000}
        ],
        "alternatives": ["ADS1015", "PCF8591"]
    },
    {
        "part_number": "MAX9814",
        "description": "Electret Microphone Amplifier",
        "manufacturer": "Maxim",
        "category": "sensor",
        "specs": {
            "gain": "40/50/60 dB",
            "bandwidth": "20Hz~20kHz",
            "vdd": "2.7V~5.5V",
            "current": "3mA",
            "feature": "AGC"
        },
        "prices": [
            {"vendor": "AliExpress", "price": 4.50, "stock": 35000},
            {"vendor": "LCSC", "price": 4.20, "stock": 15000}
        ],
        "alternatives": ["MAX4466", "MAX9814"]
    },
    {
        "part_number": "INA219",
        "description": "I2C Digital Power Monitor",
        "manufacturer": "Texas Instruments",
        "category": "sensor",
        "specs": {
            "voltage": "0~26V",
            "current": "0~3.2A",
            "resolution": "12-bit",
            "interface": "I2C",
            "voltage": "3.0V~5.5V",
            "feature": "Power Monitoring"
        },
        "prices": [
            {"vendor": "LCSC", "price": 2.50, "stock": 20000},
            {"vendor": "AliExpress", "price": 3.20, "stock": 40000}
        ],
        "alternatives": ["INA226", "ACS712"]
    }
]

# 导出所有器件数据库
def get_all_components() -> Dict[str, List[Dict]]:
    """获取所有内置器件数据（按分类）"""
    return {
        "power": POWER_COMPONENTS,
        "communication": COMMUNICATION_MODULES,
        "sensor": SENSORS,
        "passive": PASSIVE_COMPONENTS,
    }


def get_components_by_category(category: str) -> List[Dict]:
    """按类别获取器件列表"""
    all_db = get_all_components()
    return all_db.get(category.lower(), [])


def get_component_by_partnumber(part_number: str) -> Optional[Dict]:
    """根据型号精确获取器件"""
    return get_component(part_number)


# ============ 2026-02-10 新增：合并所有内置数据 ============
BUILTIN_DATABASE = (
    POWER_COMPONENTS + 
    MCU_COMPONENTS + 
    INTERFACE_COMPONENTS + 
    ANALOG_COMPONENTS + 
    DISCRETE_COMPONENTS +
    COMMUNICATION_MODULES +
    SENSORS +
    PASSIVE_COMPONENTS
)
