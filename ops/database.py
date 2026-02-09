"""
内置元器件数据库 - 常见器件数据
用于演示和离线测试
"""
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


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


# 合并所有内置数据
BUILTIN_DATABASE = (
    POWER_COMPONENTS + 
    MCU_COMPONENTS + 
    INTERFACE_COMPONENTS + 
    ANALOG_COMPONENTS + 
    DISCRETE_COMPONENTS
)


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
        
        # ... rest of the code
        
        # 参数约束
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
    """根据型号获取元器件详情"""
    for component in BUILTIN_DATABASE:
        if component["part_number"].upper() == part_number.upper():
            return component
    return None


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
