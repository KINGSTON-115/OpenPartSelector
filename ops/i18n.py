"""
🌍 多语言支持 - 中英双语界面
"""
from typing import Dict, Any
import json


# ==================== 中文界面 ====================

UI_TEXT_CN = {
    "welcome": "🎯 OpenPartSelector - AI电子元器件智能选型引擎",
    "search_placeholder": "输入需求，如：找一个 3.3V LDO 1A",
    "search_button": "🔍 开始选型",
    "results_title": "📦 推荐元器件",
    "no_results": "❌ 未找到匹配结果，请尝试其他关键词",
    "price": "价格",
    "stock": "库存",
    "compatibility": "匹配度",
    "manufacturer": "厂商",
    "datasheet": "数据手册",
    "alternatives": "替代料",
    "add_to_bom": "添加到BOM",
    "bom_title": "📋 物料清单 (BOM)",
    "total_cost": "预估总成本",
    "export_bom": "导出BOM",
    "features": {
        "chinese_alternatives": "🇨🇳 国产替代推荐",
        "jlc_integration": "🏭 嘉立创生态",
        "reference_circuits": "📚 参考电路",
        "datasheet_cn": "📖 中文解读",
        "calculators": "🧮 电路计算"
    }
}


# ==================== 英文界面 ====================

UI_TEXT_EN = {
    "welcome": "🎯 OpenPartSelector - AI Electronic Component Selection Engine",
    "search_placeholder": "Enter your request, e.g., 'Find a 3.3V LDO 1A'",
    "search_button": "🔍 Start Selection",
    "results_title": "📦 Recommended Components",
    "no_results": "❌ No matching results found, try different keywords",
    "price": "Price",
    "stock": "Stock",
    "compatibility": "Match Score",
    "manufacturer": "Manufacturer",
    "datasheet": "Datasheet",
    "alternatives": "Alternatives",
    "add_to_bom": "Add to BOM",
    "bom_title": "📋 Bill of Materials (BOM)",
    "total_cost": "Estimated Cost",
    "export_bom": "Export BOM",
    "features": {
        "chinese_alternatives": "🇨🇳 Chinese Alternatives",
        "jlc_integration": "🏭 JLC Ecosystem",
        "reference_circuits": "📚 Reference Circuits",
        "datasheet_cn": "📖 Datasheet Guide",
        "calculators": "🧮 Circuit Calculators"
    }
}


# ==================== 器件中文名称映射 ====================

COMPONENT_NAMES_CN = {
    # 品类
    "LDO": "低压差线性稳压器",
    "DC-DC": "直流-直流转换器",
    "MCU": "微控制器",
    "MOSFET": "MOS场效应管",
    "OpAmp": "运算放大器",
    "Sensor": "传感器",
    "Interface": "接口芯片",
    "Memory": "存储器",
    "Crystal": "晶振",
    "Connector": "连接器",
    "Capacitor": "电容",
    "Resistor": "电阻",
    "LED": "发光二极管",
    "Battery": "电池",
    "Module": "模块",
    
    # 常见器件
    "STM32": "STM32单片机",
    "ESP32": "ESP32无线模块",
    "ATMEGA328P": "ATMEGA328P单片机",
    "CH340": "CH340 USB转串口芯片",
    "NE555": "NE555时基芯片",
    "LM358": "LM358双运放",
    "AMS1117": "AMS1117稳压器",
    "LD1117": "LD1117稳压器",
}


# ==================== 国际平台映射 ====================

INTERNATIONAL_PLATFORMS = {
    "digikey": {
        "name": "DigiKey",
        "url": "https://www.digikey.com",
        "region": "Global",
        "currency": "USD",
        "strengths": ["正品保证", "全球发货", "技术文档全"]
    },
    "mouser": {
        "name": "Mouser",
        "url": "https://www.mouser.com",
        "region": "Global",
        "currency": "USD",
        "strengths": ["新品速度快", "技术支持好", "无最小订购量"]
    },
    "octopart": {
        "name": "Octopart",
        "url": "https://www.octopart.com",
        "region": "Global",
        "currency": "USD",
        "strengths": ["跨平台比价", "库存查询", "BOM管理"]
    },
    "arrow": {
        "name": "Arrow",
        "url": "https://www.arrow.com",
        "region": "Global",
        "currency": "USD",
        "strengths": ["工业客户", "批量采购", "技术服务"]
    },
    "rs_components": {
        "name": "RS Components",
        "url": "https://www.rs-components.com",
        "region": "Europe/Global",
        "currency": "EUR/GBP",
        "strengths": ["欧洲市场", "工业品", "快速发货"]
    },
    "ti": {
        "name": "TI Store",
        "url": "https://www.ti.com",
        "region": "Global",
        "currency": "USD",
        "strengths": ["原厂直供", "TI产品全", "样片申请"]
    },
    "st": {
        "name": "ST eStore",
        "url": "https://www.st.com",
        "region": "Global",
        "currency": "USD/EUR",
        "strengths": ["原厂直供", "STM产品全", "评估板"]
    },
}


# ==================== 封装标准对照 ====================

PACKAGE_STANDARDS = {
    "SOP-8": {
        "cn_name": "SOP-8 小外形封装",
        "alternatives": ["SOIC-8", "SO-8"],
        "jlc_footprint": "SOP-8-3.9",
        "digikey_package": "8-SOIC",
        "description": "8脚小外形集成电路封装"
    },
    "QFN-24": {
        "cn_name": "QFN-24 方形扁平无引脚封装",
        "alternatives": ["VFQFN-24"],
        "jlc_footprint": "QFN-24-4x4",
        "digikey_package": "24-VFQFN",
        "description": "24脚方形扁平无引脚封装"
    },
    "LQFP-48": {
        "cn_name": "LQFP-48 薄型四侧引脚扁平封装",
        "alternatives": ["TQFP-48"],
        "jlc_footprint": "LQFP-48-7x7",
        "digikey_package": "48-LQFP",
        "description": "48脚薄型四侧引脚封装"
    },
    "SOT-23-5": {
        "cn_name": "SOT-23-5 小外形晶体管",
        "alternatives": ["SOT-23-6"],
        "jlc_footprint": "SOT-23-5",
        "digikey_package": "5-SOT-23",
        "description": "5脚SOT-23封装"
    },
    "SOT-223": {
        "cn_name": "SOT-223 封装",
        "alternatives": ["TO-263"],
        "jlc_footprint": "SOT-223",
        "digikey_package": "SOT-223",
        "description": "4脚SOT-223功率封装"
    },
    "DIP-8": {
        "cn_name": "DIP-8 双列直插封装",
        "alternatives": ["PDIP-8"],
        "jlc_footprint": "DIP-8-300",
        "digikey_package": "8-PDIP",
        "description": "8脚双列直插封装"
    },
}


# ==================== 学习路径 ====================

LEARNING_PATHS = {
    "beginner": {
        "name": "🌱 电子入门",
        "duration": "2-4 周",
        "courses": [
            {
                "title": "电路基础",
                "topics": ["欧姆定律", "LED电路", "电阻分压", "电容充放电"],
                "projects": ["LED闪烁灯", "呼吸灯", "按键检测"],
                "recommended_components": ["LED", "Resistor 220Ω", "Capacitor 100nF", "Button"],
                "tools_needed": ["面包板", "杜邦线", "万用表", "Arduino UNO"]
            },
            {
                "title": "Arduino 入门",
                "topics": ["GPIO控制", "PWM调光", "串口通信", "传感器读取"],
                "projects": ["温湿度监测", "OLED显示", "蓝牙控制"],
                "recommended_components": ["Arduino UNO", "DHT11", "OLED 128x64", "HC-05"],
                "tools_needed": ["Arduino IDE", "USB数据线"]
            }
        ]
    },
    "intermediate": {
        "name": "🌿 单片机开发",
        "duration": "4-8 周",
        "courses": [
            {
                "title": "STM32 基础",
                "topics": ["GPIO", "UART", "I2C", "SPI", "ADC", "定时器"],
                "projects": ["串口调试助手", "I2C LCD显示", "SPI Flash读写"],
                "recommended_components": ["STM32F103C8T6", "CH340C", "LCD 16x2", "W25Q32"],
                "tools_needed": ["ST-Link", "Keil MDK/STM32CubeIDE"]
            },
            {
                "title": "ESP32 IoT 开发",
                "topics": ["WiFi配网", "MQTT通信", "蓝牙", "深度睡眠"],
                "projects": ["WiFi气象站", "远程开关", "语音控制"],
                "recommended_components": ["ESP32-WROOM", "DHT22", "Relay Module"],
                "tools_needed": ["Arduino IDE/PlatformIO"]
            }
        ]
    },
    "advanced": {
        "name": "🌳 进阶项目",
        "duration": "8-16 周",
        "courses": [
            {
                "title": "嵌入式系统设计",
                "topics": ["RTOS", "低功耗设计", "通讯协议", "Bootloader"],
                "projects": ["无人机飞控", "智能手表", "工业控制器"],
                "recommended_components": ["STM32H7", "IMU Sensor", "Flash 16MB", "Battery Charger"],
                "tools_needed": ["示波器", "逻辑分析仪", "焊接设备"]
            },
            {
                "title": "物联网全栈",
                "topics": ["云平台", "小程序", "边缘计算", "安全"],
                "projects": ["智能家居网关", "环境监测系统", "能源管理"],
                "recommended_components": ["ESP32-S3", "Various Sensors", "Cloud Module"],
                "tools_needed": ["路由器", "服务器/云主机"]
            }
        ]
    }
}


# ==================== 工具函数 ====================

def get_text(key: str, lang: str = "cn") -> str:
    """获取界面文本"""
    text_dict = UI_TEXT_CN if lang == "cn" else UI_TEXT_EN
    return text_dict.get(key, key)


def get_component_name_cn(part_type: str) -> str:
    """获取器件中文名称"""
    return COMPONENT_NAMES_CN.get(part_type, part_type)


def get_platform_info(platform: str) -> Dict:
    """获取平台信息"""
    return INTERNATIONAL_PLATFORMS.get(platform, {})


def get_package_info(package: str) -> Dict:
    """获取封装标准信息"""
    return PACKAGE_STANDARDS.get(package, {})


def get_learning_path(level: str) -> Dict:
    """获取学习路径"""
    return LEARNING_PATHS.get(level, {})
