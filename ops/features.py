"""
🔥 锦上添花功能 - 最被需要的特性
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import math


# ==================== 0. 共享常量 (E24标准电阻系列) ====================
E24_RESISTORS = [
    10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30,
    33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91,
    100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300,
    330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910,
    1000, 1100, 1200, 1300, 1500, 1600, 1800, 2000, 2200, 2400, 2700, 3000,
    3300, 3600, 3900, 4300, 4700, 5100, 5600, 6200, 6800, 7500, 8200, 9100,
    10000, 11000, 12000, 13000, 15000, 16000, 18000, 20000, 22000, 24000, 27000, 30000,
    33000, 36000, 39000, 43000, 47000, 51000, 56000, 62000, 68000, 75000, 82000, 91000,
    100000, 110000, 120000, 130000, 150000, 160000, 180000, 200000, 220000, 240000, 270000, 300000,
    330000, 360000, 390000, 430000, 470000, 510000, 560000, 620000, 680000, 750000, 820000, 910000,
    1000000
]


def find_e24_closest(value: float) -> int:
    """查找最接近的 E24 标准值"""
    return min(E24_RESISTORS, key=lambda x: abs(x - value))


def find_e24_nearby(value: float, count: int = 3) -> List[str]:
    """查找最接近的 N 个 E24 标准值"""
    sorted_values = sorted(E24_RESISTORS, key=lambda x: abs(x - value))
    result = []
    for v in sorted_values[:count]:
        if v >= 1000:
            result.append(f"{v/1000:.1f}KΩ")
        else:
            result.append(f"{v}Ω")
    return result


# ==================== 1. 国产替代推荐 ====================
# 中国工程师和学生最需要的！

CHIP_ALTERNATIVES = {
    # MCU 替代
    "STM32F103C8T6": [
        {
            "brand": "兆易创新",
            "model": "GD32F103C8T6",
            "jlc_part": "C11449",
            "price_ratio": 0.9,  # 相对原价的比例
            "compatibility": "100%兼容",
            "notes": "国产替代，pin2pin兼容，性能略强"
        },
        {
            "brand": "航顺",
            "model": "HK32F103C8T6",
            "jlc_part": "C13190",
            "price_ratio": 0.85,
            "compatibility": "95%兼容",
            "notes": "需注意ADC精度略有差异"
        },
        {
            "brand": "灵动微电子",
            "model": "MM32F103C8T6",
            "jlc_part": None,
            "price_ratio": 0.9,
            "compatibility": "95%兼容",
            "notes": "国产MCU老牌厂商"
        }
    ],
    "STM32F401CCU6": [
        {
            "brand": "兆易创新",
            "model": "GD32F401CCU6",
            "jlc_part": None,
            "price_ratio": 0.88,
            "compatibility": "95%兼容",
            "notes": "Flash略大，性能相当"
        }
    ],
    "ESP32": [
        {
            "brand": "乐鑫",
            "model": "ESP32-C3",
            "jlc_part": "C14663",
            "price_ratio": 1.1,
            "compatibility": "功能兼容",
            "notes": "RISC-V内核，WiFi+BT，更新更省电"
        },
        {
            "brand": "乐鑫",
            "model": "ESP32-S3",
            "jlc_part": None,
            "price_ratio": 1.3,
            "compatibility": "功能增强",
            "notes": "带AI加速器，USB OTG"
        }
    ],
    "ATMEGA328P": [
        {
            "brand": "宏晶",
            "model": "STC15W404AS",
            "jlc_part": None,
            "price_ratio": 0.6,
            "compatibility": "功能兼容",
            "notes": "国产增强型51内核，速度快10倍"
        },
        {
            "brand": "兆易创新",
            "model": "GD32VF103",
            "jlc_part": None,
            "price_ratio": 1.2,
            "compatibility": "功能兼容",
            "notes": "RISC-V内核，性能更强"
        }
    ],
    # 接口芯片 替代
    "CH340G": [
        {
            "brand": "沁恒",
            "model": "CH340N",
            "jlc_part": None,
            "price_ratio": 1.0,
            "compatibility": "100%兼容",
            "notes": "无需外接晶振，更省成本"
        },
        {
            "brand": "沁恒",
            "model": "CH9102F",
            "jlc_part": None,
            "price_ratio": 1.2,
            "compatibility": "90%兼容",
            "notes": "内置晶振，Type-C接口"
        }
    ],
    "CP2102": [
        {
            "brand": "沁恒",
            "model": "CH340K",
            "jlc_part": None,
            "price_ratio": 0.8,
            "compatibility": "功能兼容",
            "notes": "国产替代，价格更低"
        }
    ],
    # 电源芯片 替代
    "AMS1117": [
        {
            "brand": "微盟",
            "model": "ME6211C33",
            "jlc_part": None,
            "price_ratio": 0.7,
            "compatibility": "功能兼容",
            "notes": "低压差，更省电"
        },
        {
            "brand": "深圳矽力杰",
            "model": "SY8113",
            "jlc_part": None,
            "price_ratio": 0.9,
            "compatibility": "功能兼容",
            "notes": "效率更高，发热更少"
        }
    ],
    "LM358": [
        {
            "brand": "圣邦微",
            "model": "SGM358",
            "jlc_part": None,
            "price_ratio": 0.85,
            "compatibility": "100%兼容",
            "notes": "国产高端模拟，低噪声"
        },
        {
            "brand": "润石科技",
            "model": "RS858",
            "jlc_part": None,
            "price_ratio": 0.6,
            "compatibility": "95%兼容",
            "notes": "高性价比"
        }
    ],
    "NE555": [
        {
            "brand": "华冠",
            "model": "HGT555",
            "jlc_part": None,
            "price_ratio": 0.5,
            "compatibility": "100%兼容",
            "notes": "国产替代，便宜"
        }
    ]
}


def find_alternatives(part_number: str) -> List[Dict]:
    """查找国产替代方案"""
    # 模糊匹配
    for key, alts in CHIP_ALTERNATIVES.items():
        if key.upper() in part_number.upper() or part_number.upper() in key.upper():
            return alts
    return []


# ==================== 2. 参考电路模板库 ====================
# 学生做项目最需要的！

CIRCUIT_TEMPLATES = {
    "esp32_minimal": {
        "name": "ESP32 最小系统",
        "description": "ESP32 芯片/模块工作的最简电路",
        "difficulty": "⭐",
        "器件列表": [
            {"part": "ESP32-WROOM-32", "value": "1", "desc": "WiFi模块"},
            {"part": "AMS1117-3.3", "value": "1", "desc": "LDO 3.3V"},
            {"part": "10uF", "type": "Capacitor", "value": "2", "desc": "去耦电容"},
            {"part": "100nF", "type": "Capacitor", "value": "3", "desc": "去耦电容"},
            {"part": "10K", "type": "Resistor", "value": "2", "desc": "上拉电阻"},
            {"part": "Micro USB", "type": "Connector", "value": "1", "desc": "电源接口"},
        ],
        "注意事项": [
            "模块EN脚需10K上拉",
            "3.3V电源需100nF+10uF去耦",
            "IO0接地进入下载模式",
        ],
        "jlc_bom_cost": 15.0,
        "参考链接": "https://www.espressif.com/sites/default/files/documentation/esp32_hardware_design_guidelines_en.pdf"
    },
    "esp32_downloader": {
        "name": "ESP32 下载/调试器",
        "description": "使用 CH340C 的 ESP32 烧录电路",
        "difficulty": "⭐",
        "器件列表": [
            {"part": "CH340C", "value": "1", "desc": "USB转串口"},
            {"part": "Micro USB", "type": "Connector", "value": "1", "desc": "USB接口"},
            {"part": "100nF", "type": "Capacitor", "value": "2", "desc": "CH340去耦"},
            {"part": "22pF", "type": "Capacitor", "value": "2", "desc": "晶振负载"},
            {"part": "12MHz", "type": "Crystal", "value": "1", "desc": "晶振"},
            {"part": "10K", "type": "Resistor", "value": "3", "desc": "上拉/限流"},
            {"part": "LED", "type": "LED", "value": "2", "desc": "电源/发送指示"},
            {"part": "510R", "type": "Resistor", "value": "2", "desc": "LED限流"},
        ],
        "注意事项": [
            "CH340C需外接12MHz晶振",
            "DTR/RTS连接ESP32的EN/IO0进行自动下载",
        ],
        "jlc_bom_cost": 8.0,
        "参考链接": None
    },
    "stm32_minimal": {
        "name": "STM32 最小系统",
        "description": "STM32F103 工作的最简电路",
        "difficulty": "⭐⭐",
        "器件列表": [
            {"part": "STM32F103C8T6", "value": "1", "desc": "MCU"},
            {"part": "10uF", "type": "Capacitor", "value": "2", "desc": "电源去耦"},
            {"part": "100nF", "type": "Capacitor", "value": "3", "desc": "VDD去耦"},
            {"part": "10K", "type": "Resistor", "value": "1", "desc": "BOOT0下拉"},
            {"part": "SWD", "type": "Connector", "value": "1", "desc": "调试接口"},
            {"part": "Micro USB", "type": "Connector", "value": "1", "desc": "电源"},
        ],
        "注意事项": [
            "VDD需0.1uF+10uF去耦",
            "BOOT0接地为Flash启动",
            "使用SWD调试需保留SWDIO/SWCLK",
        ],
        "jlc_bom_cost": 12.0,
        "参考链接": "https://www.st.com/resource/en/application_note/an2586-getting-started-with-stm32f1-series-hardware-development-stmicroelectronics.pdf"
    },
    "ldo_power": {
        "name": "LDO 稳压电源",
        "description": "5V转3.3V 线性稳压电路",
        "difficulty": "⭐",
        "器件列表": [
            {"part": "AMS1117-3.3", "value": "1", "desc": "LDO稳压"},
            {"part": "10uF", "type": "Capacitor", "value": "2", "desc": "输入输出电容"},
            {"part": "100nF", "type": "Capacitor", "value": "1", "desc": "高频去耦"},
            {"part": "Micro USB", "type": "Connector", "value": "1", "desc": "5V输入"},
        ],
        "注意事项": [
            "输入电容靠近Vin引脚",
            "输出电容靠近Vout引脚",
            "大电流时注意散热",
        ],
        "jlc_bom_cost": 2.0,
        "参考链接": None
    },
    "bluetooth_uart": {
        "name": "蓝牙串口模块",
        "description": "HC-05/HC-06 蓝牙串口电路",
        "difficulty": "⭐",
        "器件列表": [
            {"part": "HC-05", "type": "Module", "value": "1", "desc": "蓝牙模块"},
            {"part": "3.3V LDO", "value": "1", "desc": "5V转3.3V"},
            {"part": "10uF", "type": "Capacitor", "value": "2", "desc": "电容"},
            {"part": "LED", "type": "LED", "value": "2", "desc": "状态指示"},
            {"part": "1K", "type": "Resistor", "value": "2", "desc": "LED限流"},
        ],
        "注意事项": [
            "HC-05工作电压3.3V，需5V转3.3V",
            "KEY脚高电平进入AT模式",
            "配对码默认为1234",
        ],
        "jlc_bom_cost": 15.0,
        "参考链接": None
    },
    "mq_sensors": {
        "name": "MQ气体传感器接口",
        "description": "MQ-2/MQ-3 等气体传感器接口电路",
        "difficulty": "⭐⭐",
        "器件列表": [
            {"part": "MQ-2", "type": "Sensor", "value": "1", "desc": "烟雾/可燃气体"},
            {"part": "10K", "type": "Resistor", "value": "1", "desc": "负载电阻"},
            {"part": "100R", "type": "Resistor", "value": "1", "desc": "加热限流"},
            {"part": "100nF", "type": "Capacitor", "value": "1", "desc": "滤波"},
        ],
        "注意事项": [
            "MQ传感器需预热5分钟",
            "负载电阻调节灵敏度",
            "输出为模拟电压，需ADC读取",
        ],
        "jlc_bom_cost": 8.0,
        "参考链接": None
    },
    "power_bank": {
        "name": "充电宝电路",
        "description": "TP4056 锂电池充电电路",
        "difficulty": "⭐⭐",
        "器件列表": [
            {"part": "TP4056", "value": "1", "desc": "充电管理"},
            {"part": "18650", "type": "Battery", "value": "1", "desc": "锂电池"},
            {"part": "10uF", "type": "Capacitor", "value": "2", "desc": "电容"},
            {"part": "1K", "type": "Resistor", "value": "1", "desc": "充电电流设置"},
            {"part": "Micro USB", "type": "Connector", "value": "1", "desc": "充电口"},
            {"part": "USB Type-A", "type": "Connector", "value": "1", "desc": "输出口"},
            {"part": "3.7V升压", "type": "Module", "value": "1", "desc": "5V升压模块"},
        ],
        "注意事项": [
            "TP4056充电电流=1000/R",
            "需注意锂电池正负极",
            "可加装保护板",
        ],
        "jlc_bom_cost": 12.0,
        "参考链接": None
    }
}


def get_circuit_template(name: str) -> Optional[Dict]:
    """获取参考电路模板"""
    return CIRCUIT_TEMPLATES.get(name.lower().replace(" ", "_"))


def search_circuits(keyword: str) -> List[Dict]:
    """搜索电路模板"""
    results = []
    for key, tmpl in CIRCUIT_TEMPLATES.items():
        if keyword.lower() in tmpl["name"].lower() or keyword.lower() in tmpl["description"].lower():
            results.append({
                "key": key,
                **tmpl
            })
    return results


# ==================== 3. Datasheet 中文解读 ====================

DATASHEET_SUMMARIES = {
    "STM32F103C8T6": {
        "一句话说明": "STM32F103C8T6 是一款基于ARM Cortex-M3内核的32位微控制器",
        "主要特点": [
            "72MHz主频，64KB Flash，20KB SRAM",
            "丰富外设: GPIO/USART/SPI/I2C/ADC/DAC",
            "2.0-3.6V供电，低功耗",
            "LQFP48封装，标准SWD调试",
        ],
        "应用场景": [
            "学生入门学习单片机",
            "嵌入式项目开发",
            "工业控制小系统",
        ],
        "注意事项": [
            "首次使用需设置BOOT0接地",
            "建议使用ST-Link或DAP调试器",
            "国产替代: GD32F103 (性能更强)"
        ],
        "datasheet_link": "https://www.st.com/resource/en/datasheet/stm32f103c8.pdf"
    },
    "ESP32-WROOM-32": {
        "一句话说明": "ESP32-WROOM-32 是一款集WiFi+蓝牙于一体的低成本IoT模组",
        "主要特点": [
            "双核240MHz，支持WiFi 802.11 b/g/n + BT 4.2",
            "内置4MB Flash，集成天线",
            "支持蓝牙和WiFi同时工作",
            "超低功耗，支持深度睡眠",
        ],
        "应用场景": [
            "物联网项目 (IoT)",
            "智能家居设备",
            "WiFi/蓝牙数据传输",
        ],
        "注意事项": [
            "模组需3.3V供电，峰值电流可达500mA",
            "EN脚需10K上拉，IO0决定启动模式",
            "建议配合LDO使用，电源纹波要小",
        ],
        "datasheet_link": "https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32d_esp32-wroom-32u_datasheet_en.pdf"
    },
    "CH340G": {
        "一句话说明": "CH340G 是一款USB转串口芯片，用于USB与UART之间的转换",
        "主要特点": [
            "支持USB转UART/Printer/IrDA等",
            "最高波特率2Mbps",
            "内置晶振，需外接12MHz",
            "5V和3.3V供电版本",
        ],
        "应用场景": [
            "USB转TTL串口调试",
            "单片机程序下载",
            "USB转RS232/485",
        ],
        "注意事项": [
            "G版需外接晶振，N版内置晶振",
            "Windows需安装CH340驱动",
            "TX接对方RX，RX接对方TX",
        ],
        "datasheet_link": "http://www.wch.cn/downloads/CH340DS1_PDF.html"
    },
    "AMS1117": {
        "一句话说明": "AMS1117 是一款低压差线性稳压器(LDO)，最大输出1A",
        "主要特点": [
            "输入电压最高12V，输出3.3V/5V可调",
            "固定版和可调版",
            "内置过热保护和限流保护",
            "SOT-223封装，便于散热",
        ],
        "应用场景": [
            "5V转3.3V电路",
            "简单电源设计",
            "嵌入式系统供电",
        ],
        "注意事项": [
            "低压差1V，大电流时发热明显",
            "建议并联大电容降低纹波",
            "可考虑ME6211替代(低压差更省电)",
        ],
        "datasheet_link": "https://www.advanced-monolithic.com/pdf/ds1117.pdf"
    },
    "LM358": {
        "一句话说明": "LM358 是一款低功耗双运放，常用于信号放大和比较",
        "主要特点": [
            "单电源2-36V或双电源±1~±18V",
            "内置双运放，低功耗500uA/运放",
            "带宽700kHz，输入偏置电流低",
        ],
        "应用场景": [
            "传感器信号放大",
            "电压比较器",
            "积分/微分电路",
        ],
        "注意事项": [
            "输出摆幅受限于电源电压",
            "非轨到轨运放",
            "可考虑国产SGM358(更低噪声)",
        ],
        "datasheet_link": "https://www.ti.com/lit/ds/symlink/lm358.pdf"
    }
}


def get_datasheet_summary(part_number: str) -> Optional[Dict]:
    """获取Datasheet中文解读"""
    # 模糊匹配
    for key, summary in DATASHEET_SUMMARIES.items():
        if key.upper() in part_number.upper() or part_number.upper() in key.upper():
            return summary
    return None


# ==================== 4. 常用计算工具 ====================

def calculate_resistor_for_led(
    voltage: float = 5.0,
    led_voltage: float = 2.0,
    led_current: float = 0.02
) -> Dict:
    """
    计算LED限流电阻 (统一版 v1.1.24)
    
    合并了 calculate_led_resistor 功能，提供完整的电阻计算和封装推荐。
    
    Args:
        voltage: 输入电压 (V)
        led_voltage: LED正向压降 (V)
        led_current: LED工作电流 (A)
    
    Returns:
        推荐电阻值及参数
    """
    v_resistor = voltage - led_voltage
    
    if v_resistor <= 0:
        return {"error": "输入电压必须大于LED压降"}
    
    # 计算理想电阻值
    r_ideal = v_resistor / led_current
    
    # 使用共享E24标准值
    r_std = find_e24_closest(r_ideal)
    
    # 计算实际电流
    i_actual = v_resistor / r_std
    
    # 计算功耗
    power = v_resistor * i_actual
    
    # 推荐功率 (留50%余量)
    recommended_power = power * 2
    
    # 推荐封装
    if recommended_power < 0.125:
        package = "0603"
    elif recommended_power < 0.25:
        package = "0805"
    elif recommended_power < 0.5:
        package = "1206"
    else:
        package = "1210或更大"
    
    return {
        "input_voltage": f"{voltage}V",
        "led_voltage": f"{led_voltage}V",
        "led_current": f"{led_current*1000:.0f}mA",
        "ideal_resistor": f"{r_ideal:.1f}Ω",
        "recommended_resistor": f"{r_std}Ω",
        "actual_current": f"{i_actual*1000:.1f}mA",
        "power_dissipation": f"{power*1000:.1f}mW",
        "recommended_power": f"{recommended_power*1000:.1f}mW",
        "recommended_package": package,
        "formula": "R = (V_in - V_led) / I_led"
    }


# 为保持向后兼容性，保留这些别名函数
def calculate_led_resistor(
    voltage: float = 5.0,
    led_voltage: float = 2.0,
    led_current: float = 0.02
) -> Dict:
    """计算LED限流电阻 (别名函数)"""
    return calculate_resistor_for_led(voltage=voltage, led_voltage=led_voltage, led_current=led_current)


def calculate_led_series_resistor(
    supply_voltage: float = None,
    led_forward_voltage: float = None,
    led_current: float = None,
    voltage: float = None,
    led_voltage: float = None,
    led_current_ma: float = None
) -> Dict:
    """计算LED串联电阻 (兼容性函数)"""
    if supply_voltage is None:
        supply_voltage = voltage
    if led_forward_voltage is None:
        led_forward_voltage = led_voltage
    if led_current is None and led_current_ma is not None:
        led_current = led_current_ma / 1000
    elif led_current is None:
        led_current = 0.02
    
    result = calculate_resistor_for_led(
        voltage=supply_voltage,
        led_voltage=led_forward_voltage,
        led_current=led_current
    )
    
    if "recommended_resistor" in result:
        result["recommended_resistance"] = result["recommended_resistor"]
    if "power_dissipation" in result:
        result["power_dissipation_mw"] = result["power_dissipation"]
    
    return result


def calculate_voltage_divider(
    v_in: float = 5.0,
    v_out: float = 3.3,
    r1: float = None  # 如果为None则自动计算
) -> Dict:
    """计算分压电阻 (复用E24标准值)"""
    # 边缘情况处理
    if v_in <= 0:
        return {"error": "输入电压必须大于0"}
    if v_out <= 0:
        return {"error": "输出电压必须大于0"}
    if v_out >= v_in:
        return {"error": "输出电压必须小于输入电压"}
    
    if r1 is None:
        # 假设R2=10K，计算R1
        r2 = 10000
        r1 = r2 * (v_in / v_out - 1)
    else:
        if r1 <= 0:
            return {"error": "R1电阻值必须大于0"}
        r2 = r1 * v_out / (v_in - v_out)
        if r2 <= 0:
            return {"error": "R2电阻值必须大于0"}
    
    # 使用共享的E24标准值
    r1_std = find_e24_closest(r1)
    r2_std = find_e24_closest(r2)
    
    actual_vout = v_in * r2_std / (r1_std + r2_std)
    
    # 生成提示
    tips = []
    if r1_std >= 1000:
        tips.append(f"R1={r1_std/1000:.0f}KΩ, R2={r2_std/1000:.0f}KΩ")
    else:
        tips.append(f"R1={r1_std}Ω, R2={r2_std}Ω")
    if abs(actual_vout - v_out) / v_out > 0.05:
        tips.append("误差超过5%，建议调整电阻值")
    
    return {
        "input_voltage": f"{v_in}V",
        "desired_output": f"{v_out}V",
        "calculated_r1": f"{r1/1000:.1f}KΩ",
        "calculated_r2": f"{r2/1000:.1f}KΩ",
        "recommended_r1": f"{r1_std}Ω",
        "recommended_r2": f"{r2_std}Ω",
        "actual_output": f"{actual_vout:.2f}V",
        "error_percent": f"{abs(actual_vout - v_out) / v_out * 100:.2f}%",
        "formula": "Vout = Vin × R2 / (R1 + R2)",
        "tips": tips
    }


def calculate_pwm_frequency(
    timer_clock: float = 72000000,  # STM32默认72MHz
    prescaler: int = 7199,
    auto_reload: int = 99
) -> Dict:
    """计算PWM频率"""
    # 边缘情况处理
    if timer_clock <= 0:
        return {"error": "定时器时钟频率必须大于0"}
    if prescaler <= 0:
        return {"error": "预分频值必须大于0"}
    if auto_reload <= 0:
        return {"error": "自动重载值必须大于0"}
    
    period = prescaler + 1
    frequency = timer_clock / (prescaler + 1) / (auto_reload + 1)
    duty_resolution = (auto_reload + 1)
    duty_step = 100 / duty_resolution
    
    return {
        "timer_clock": f"{timer_clock/1000000:.0f}MHz",
        "prescaler": prescaler,
        "auto_reload": auto_reload,
        "frequency": f"{frequency:.2f}Hz",
        "period": f"{(1/frequency)*1000:.2f}ms",
        "duty_resolution": f"{duty_resolution}级 ({duty_step:.2f}%/级)",
        "formula": "Freq = TimerClock / (PSC+1) / (ARR+1)"
    }


def calculate_rc_time_constant(
    resistance: float = 10000,  # 10KΩ
    capacitance: float = 0.0001  # 100uF
) -> Dict:
    """
    计算RC时间常数
    
    Args:
        resistance: 电阻值 (Ω)
        capacitance: 电容值 (F)
    
    Returns:
        时间常数及充放电参数
    """
    # 边缘情况处理
    if resistance <= 0:
        return {"error": "电阻值必须大于0"}
    if capacitance <= 0:
        return {"error": "电容值必须大于0"}
    
    tau = resistance * capacitance
    
    # 充放电时间
    t_63 = tau  # 63.2%
    t_50 = tau * 0.693  # 50%
    t_90 = tau * 2.303  # 90%
    t_99 = tau * 4.605  # 99%
    
    # 截止频率
    f_cutoff = 1 / (2 * 3.14159 * resistance * capacitance)
    
    # 格式化电容和时间显示
    if capacitance >= 0.001:
        cap_str = f"{capacitance*1000:.1f}mF"
        tau_str = f"{tau:.4f}s"
    elif capacitance >= 0.000001:
        # μF
        if tau >= 0.001:
            tau_str = f"{tau*1000:.1f}ms"
        else:
            tau_str = f"{tau*1000000:.1f}μs"
        cap_str = f"{capacitance*1000000:.1f}μF"
    else:
        # nF 或 pF
        if tau >= 0.000001:
            tau_str = f"{tau*1000:.1f}ms"
        elif tau >= 0.000001:
            tau_str = f"{tau*1000000:.1f}μs"
        else:
            tau_str = f"{tau*1000000:.1f}μs"
        if capacitance >= 0.000000001:
            cap_str = f"{capacitance*1000000000:.1f}nF"
        else:
            cap_str = f"{capacitance*1000000000000:.1f}pF"
    
    return {
        "resistance": f"{resistance/1000:.1f}KΩ",
        "capacitance": cap_str,
        "time_constant": tau_str,
        "time_50pct": f"{t_50:.6f}s (50%充电)",
        "time_63pct": f"{t_63:.6f}s (63.2%充电)",
        "time_90pct": f"{t_90:.6f}s (90%充电)",
        "time_99pct": f"{t_99:.6f}s (99%充电)",
        "cutoff_frequency": f"{f_cutoff:.2f}Hz",
        "formula": "τ = R × C"
    }


def calculate_capacitor_ripple(
    load_current: float = 0.1,  # 100mA
    ripple_voltage: float = 0.5,  # 500mVpp
    frequency: float = 120  # 120Hz (全波整流)
) -> Dict:
    """
    计算滤波电容容量 (简化公式)
    
    Args:
        load_current: 负载电流 (A)
        ripple_voltage: 允许纹波电压 (Vpp)
        frequency: 纹波频率 (Hz)
    
    Returns:
        推荐电容值及参数
    """
    # 边缘情况处理
    if load_current <= 0:
        return {"error": "负载电流必须大于0"}
    if ripple_voltage <= 0:
        return {"error": "纹波电压必须大于0"}
    if frequency <= 0:
        return {"error": "频率必须大于0"}
    
    # 简化公式: C = I / (f × Vripple)
    c_ideal = load_current / (frequency * ripple_voltage)
    
    # 转换为常用单位 (μF)
    c_uf = c_ideal * 1000000
    
    # 推荐标准值 (扩展范围)
    standard_values = [4.7, 10, 22, 47, 100, 220, 470, 1000, 2200, 4700, 10000, 22000, 47000]
    c_std = min(standard_values, key=lambda x: abs(x - c_uf))
    
    # 实际纹波 (C 转换为法拉)
    actual_ripple = load_current / (frequency * (c_std / 1000000))
    
    # 生成提示
    tips = [f"频率{frequency}Hz对应周期{1000/frequency:.1f}ms"]
    if frequency == 100:
        tips.append("100Hz = 全波整流后的频率")
    elif frequency == 120:
        tips.append("120Hz = 全波整流50Hz市电后的频率")
    elif frequency == 60:
        tips.append("60Hz = 全波整流60Hz市电后的频率")
    
    return {
        "load_current": f"{load_current*1000:.0f}mA",
        "ripple_voltage": f"{ripple_voltage*1000:.0f}mVpp",
        "frequency": f"{frequency}Hz",
        "ideal_capacitor": f"{c_uf:.1f}μF",
        "recommended_capacitor": f"{c_std}μF",
        "actual_ripple": f"{actual_ripple*1000:.1f}mVpp",
        "formula": "C = I / (f × ΔV)",
        "tips": tips
    }


# ==================== 新增: 电阻色环解码器 (v1.1.8) ====================

RESISTOR_COLORS = {
    "black": {"value": 0, "multiplier": 1, "tolerance": None},
    "brown": {"value": 1, "multiplier": 10, "tolerance": 1},
    "red": {"value": 2, "multiplier": 100, "tolerance": 2},
    "orange": {"value": 3, "multiplier": 1000, "tolerance": None},
    "yellow": {"value": 4, "multiplier": 10000, "tolerance": 5},
    "green": {"value": 5, "multiplier": 100000, "tolerance": 0.5},
    "blue": {"value": 6, "multiplier": 1000000, "tolerance": 0.25},
    "violet": {"value": 7, "multiplier": 10000000, "tolerance": 0.1},
    "gray": {"value": 8, "multiplier": 0.1, "tolerance": 0.05},
    "white": {"value": 9, "multiplier": 0.01, "tolerance": None},
    "gold": {"value": None, "multiplier": 0.1, "tolerance": 5},
    "silver": {"value": None, "multiplier": 0.01, "tolerance": 10},
}

TOLERANCE_COLORS = {
    1: "brown",
    2: "red",
    5: "gold",
    10: "silver",
    0.5: "green",
    0.25: "blue",
    0.1: "violet",
    0.05: "gray",
}


def decode_resistor_4band(
    color1: str,
    color2: str, 
    color3: str,
    color4: str = "gold"
) -> Dict:
    """
    解码 4 色环电阻
    
    Args:
        color1: 第1环 (首位数字)
        color2: 第2环 (次位数字)
        color3: 第3环 (乘数)
        color4: 第4环 (误差)
    
    Returns:
        电阻值及参数
    """
    color1 = color1.lower()
    color2 = color2.lower()
    color3 = color3.lower()
    color4 = color4.lower()
    
    v1 = RESISTOR_COLORS.get(color1, {}).get("value")
    v2 = RESISTOR_COLORS.get(color2, {}).get("value")
    mult = RESISTOR_COLORS.get(color3, {}).get("multiplier", 1)
    tol = RESISTOR_COLORS.get(color4, {}).get("tolerance", 5)
    
    if v1 is None or v2 is None:
        return {"error": "无效的颜色代码"}
    
    # 计算阻值
    resistance = (v1 * 10 + v2) * mult
    
    # 格式化输出
    if resistance >= 1000000:
        value_str = f"{resistance / 1000000:.1f}MΩ"
    elif resistance >= 1000:
        value_str = f"{resistance / 1000:.1f}KΩ"
    else:
        value_str = f"{resistance:.0f}Ω"
    
    # 查找误差对应的颜色
    tol_color = color4
    
    return {
        "bands": 4,
        "colors": [color1, color2, color3, color4],
        "resistance": value_str,
        "tolerance": f"±{tol}%",
        "power_rating": "1/4W",
        "e24_alternative": f"{find_e24_closest(resistance)}Ω (E24)"
    }


def decode_resistor_5band(
    color1: str,
    color2: str,
    color3: str,
    color4: str,
    color5: str = "brown"
) -> Dict:
    """
    解码 5 色环精密电阻
    
    Args:
        color1: 第1环 (百位数)
        color2: 第2环 (十位数)
        color3: 第3环 (个位数)
        color4: 第4环 (乘数)
        color5: 第5环 (误差)
    
    Returns:
        电阻值及参数
    """
    color1 = color1.lower()
    color2 = color2.lower()
    color3 = color3.lower()
    color4 = color4.lower()
    color5 = color5.lower()
    
    v1 = RESISTOR_COLORS.get(color1, {}).get("value")
    v2 = RESISTOR_COLORS.get(color2, {}).get("value")
    v3 = RESISTOR_COLORS.get(color3, {}).get("value")
    mult = RESISTOR_COLORS.get(color4, {}).get("multiplier", 1)
    tol = RESISTOR_COLORS.get(color5, {}).get("tolerance", 1)
    
    if v1 is None or v2 is None or v3 is None:
        return {"error": "无效的颜色代码"}
    
    # 计算阻值
    resistance = (v1 * 100 + v2 * 10 + v3) * mult
    
    # 格式化输出
    if resistance >= 1000000:
        value_str = f"{resistance / 1000000:.2f}MΩ"
    elif resistance >= 1000:
        value_str = f"{resistance / 1000:.2f}KΩ"
    else:
        value_str = f"{resistance:.0f}Ω"
    
    return {
        "bands": 5,
        "colors": [color1, color2, color3, color4, color5],
        "resistance": value_str,
        "tolerance": f"±{tol}%",
        "power_rating": "1/8W~1/4W",
        "e24_alternative": f"{find_e24_closest(resistance)}Ω (E24)"
    }


# ==================== 新增: 电容色环解码器 (v1.1.9) ====================

CAPACITOR_CODES = {
    # 瓷片电容色环 (前两位数字) - 标准EIA色码
    "black": 0, "brown": 1, "red": 2, "orange": 3,
    "yellow": 4, "green": 5, "blue": 6, "violet": 7,
    "gray": 8, "white": 9,
}

CAPACITOR_MULTIPLIERS = {
    # 乘数 (pF单位, EIA标准)
    # 棕=×10, 红=×100, 橙=×1nF, 黄=×10nF, 绿=×100nF, 蓝=×1μF
    "black": 1, "brown": 10, "red": 100, "orange": 1000,
    "yellow": 10000, "green": 100000, "blue": 1000000,
    "violet": 10000000, "gold": 0.1, "silver": 0.01,
}

CAPACITOR_TOLERANCES = {
    "black": "±20%",
    "brown": "±1%",
    "red": "±2%",
    "green": "±5%",
    "white": "±10%",
    "gold": "±5%",
    "silver": "±10%",
}


def decode_capacitor_3band(color1: str, color2: str, color3: str) -> Dict:
    """
    解码 3 色环瓷片电容
    
    Args:
        color1: 第1环 (十位数)
        color2: 第2环 (个位数)
        color3: 第3环 (乘数)
    
    Returns:
        电容值
    """
    color1, color2, color3 = color1.lower(), color2.lower(), color3.lower()
    
    v1 = CAPACITOR_CODES.get(color1)
    v2 = CAPACITOR_CODES.get(color2, 0)
    mult = CAPACITOR_MULTIPLIERS.get(color3, 1)
    
    if v1 is None:
        return {"error": "无效的颜色代码"}
    
    capacitance = (v1 * 10 + v2) * mult
    
    # 格式化
    if capacitance >= 1000000:
        value_str = f"{capacitance / 1000000:.1f}μF"
    elif capacitance >= 1000:
        value_str = f"{capacitance / 1000:.0f}nF"
    else:
        value_str = f"{capacitance:.0f}pF"
    
    return {
        "bands": 3,
        "colors": [color1, color2, color3],
        "capacitance": value_str,
        "formula": "C = (第1环×10 + 第2环) × 乘数"
    }


# ==================== 新增: 电感计算器 (v1.1.9) ====================

def calculate_inductor_energy(
    inductance: float = 0.001,  # 1mH
    current: float = 0.1  # 100mA
) -> Dict:
    """
    计算电感储能
    
    Args:
        inductance: 电感量 (H)
        current: 电流 (A)
    
    Returns:
        储能及参数
    """
    energy = 0.5 * inductance * current ** 2
    impedance = 2 * 3.14159 * inductance * 1000  # 假设1kHz
    
    return {
        "inductance": f"{inductance*1000:.1f}mH",
        "current": f"{current*1000:.0f}mA",
        "energy": f"{energy*1000000:.1f}μJ",
        "impedance_1kHz": f"{impedance:.1f}Ω",
        "formula": "E = ½ × L × I²"
    }


def calculate_rf_attenuator(
    input_power_dbm: float = 10,  # 10dBm
    attenuation_db: float = 20  # 20dB
) -> Dict:
    """
    计算射频衰减器输出功率
    
    Args:
        input_power_dbm: 输入功率 (dBm)
        attenuation_db: 衰减量 (dB)
    
    Returns:
        输出功率及功率值
    """
    output_dbm = input_power_dbm - attenuation_db
    
    # dBm -> mW
    input_mw = 10 ** (input_power_dbm / 10)
    output_mw = 10 ** (output_dbm / 10)
    
    # 转换为W
    input_w = input_mw / 1000
    output_w = output_mw / 1000
    
    return {
        "input_power_dbm": f"{input_power_dbm:.1f}dBm",
        "input_power_mw": f"{input_mw:.4f}mW",
        "input_power_w": f"{input_w:.6f}W",
        "attenuation": f"{attenuation_db:.1f}dB",
        "output_power_dbm": f"{output_dbm:.1f}dBm",
        "output_power_mw": f"{output_mw:.4f}mW",
        "output_power_w": f"{output_w:.9f}W",
        "formula": "P_out(dBm) = P_in(dBm) - Attenuation(dB)"
    }


# ==================== 新增: 电池续航计算器 (v1.1.28) ====================

def calculate_battery_life(
    battery_capacity: float = 2000,  # 电池容量 (mAh)
    avg_current: float = 50,  # 平均工作电流 (mA)
    standby_current: float = 0.1,  # 待机电流 (mA)
    active_time_per_day: float = 2,  # 每天活跃时间 (小时)
) -> Dict:
    """
    计算电池续航时间

    Args:
        battery_capacity: 电池容量 (mAh)
        avg_current: 平均工作电流 (mA)
        standby_current: 待机电流 (mA)
        active_time_per_day: 每天活跃时间 (小时)

    Returns:
        续航时间及参数
    """
    # 边缘情况处理
    if battery_capacity <= 0:
        return {"error": "电池容量必须大于0"}
    if active_time_per_day < 0:
        return {"error": "活跃时间不能为负数"}
    if active_time_per_day > 24:
        return {"error": "每天活跃时间不能超过24小时"}

    standby_time_per_day = 24 - active_time_per_day

    # 每天消耗的容量
    daily_capacity_used = avg_current * active_time_per_day + standby_current * standby_time_per_day

    # 续航天数
    if avg_current <= 0 and standby_current <= 0:
        return {"error": "电流消耗必须大于0"}
    if daily_capacity_used <= 0:
        return {"error": "电流消耗必须大于0"}
    
    days = battery_capacity / daily_capacity_used
    
    # 预计日期
    from datetime import datetime, timedelta
    now = datetime.now()
    end_date = now + timedelta(days=days)
    
    return {
        "battery_capacity": f"{battery_capacity}mAh",
        "avg_current": f"{avg_current}mA",
        "active_time_per_day": f"{active_time_per_day}h",
        "daily_capacity_used": f"{daily_capacity_used:.1f}mAh",
        "battery_life_days": f"{days:.1f}天",
        "battery_life_hours": f"{days*24:.0f}小时",
        "expected_depletion": end_date.strftime("%Y-%m-%d"),
        "tips": [
            f"每天活跃{active_time_per_day}小时，消耗{avg_current*active_time_per_day:.0f}mAh",
            f"待机{standby_time_per_day}小时，消耗{standby_current*standby_time_per_day:.1f}mAh",
            f"总计每天约{daily_capacity_used:.1f}mAh"
        ]
    }


# ==================== 新增: 电压基准计算器 (v1.1.28) ====================

def calculate_voltage_reference(
    v_in: float = 5.0,  # 输入电压 (V)
    v_ref: float = 2.5,  # 目标基准电压 (V)
    i_ref: float = 0.001,  # 基准芯片工作电流 (A)
    tolerance: str = "1%"
) -> Dict:
    """
    计算电压基准分压电阻
    
    使用 TL431 等电压基准芯片
    
    Args:
        v_in: 输入电压 (V)
        v_ref: 目标基准电压 (V)
        i_ref: 基准芯片工作电流 (A)
        tolerance: 电阻精度
    
    Returns:
        推荐电阻值及参数
    """
    # 边缘情况处理
    if v_in <= 0:
        return {"error": "输入电压必须大于0"}
    if v_ref <= 0:
        return {"error": "基准电压必须大于0"}
    if v_ref >= v_in:
        return {"error": "基准电压必须小于输入电压"}
    if i_ref <= 0:
        return {"error": "基准电流必须大于0"}
    
    # 计算分压电流 (应大于 i_ref 的 10 倍以保证稳定性)
    min_divider_current = i_ref * 10
    divider_current = max(min_divider_current, 0.001)  # 至少 1mA
    
    # 总电阻
    r_total = (v_in - v_ref) / divider_current
    
    # 下拉电阻 (从 Vref 到 GND)
    r2 = v_ref / divider_current
    
    # 上拉电阻 (从 Vin 到 Vref)
    r1 = r_total - r2
    
    # E24 系列标准值 (扩展到更大阻值)
    e24 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 51, 68, 82, 100, 120, 
           150, 180, 220, 270, 330, 390, 470, 510, 680, 820, 1000, 1200,
           1500, 1800, 2000, 2200, 2700, 3300, 3900, 4700, 5100, 5600,
           6800, 8200, 10000, 12000, 15000, 18000, 20000, 22000, 27000,
           33000, 39000, 47000, 51000, 68000, 82000, 100000, 120000,
           150000, 180000, 200000, 220000, 270000, 330000, 390000, 470000,
           510000, 680000, 820000, 1000000]
    
    # 查找合适的标准值
    available_e24 = [x for x in e24 if x >= r1 * 0.1]  # 至少要接近计算值
    if not available_e24:
        r1_closest = max(e24)  # 使用最大值
    else:
        r1_closest = min(available_e24, key=lambda x: abs(x - r1))
    
    available_e24_r2 = [x for x in e24 if x >= r2 * 0.1]
    if not available_e24_r2:
        r2_closest = max(e24)
    else:
        r2_closest = min(available_e24_r2, key=lambda x: abs(x - r2))
    
    # 实际输出电压
    v_out_actual = v_in * r2_closest / (r1_closest + r2_closest)
    
    return {
        "v_in": f"{v_in:.1f}V",
        "target_v_ref": f"{v_ref}V",
        "calculated_r1": f"{r1:.0f}Ω",
        "calculated_r2": f"{r2:.0f}Ω",
        "recommended_r1": f"{r1_closest}Ω",
        "recommended_r2": f"{r2_closest}Ω",
        "actual_v_ref": f"{v_out_actual:.3f}V",
        "divider_current": f"{divider_current*1000:.1f}mA",
        "formula": "Vref = Vin × R2 / (R1 + R2)",
        "chip_example": "TL431, LM4040, REF3030",
        "notes": "推荐使用 1% 精度电阻"
    }


# ==================== 新增: LED 并联电阻计算器 (v1.1.33) ====================

def calculate_led_parallel_resistor(
    v_supply: float = 5.0,  # 电源电压 (V)
    led_voltage: float = 2.0,  # LED 正向电压 (V)
    led_current: float = 0.02,  # LED 工作电流 (A)
    num_leds: int = 2,  # LED 数量
    arrangement: str = "parallel"  # 连接方式: parallel/series
) -> Dict:
    """
    计算多 LED 并联/串联限流电阻
    
    Args:
        v_supply: 电源电压 (V)
        led_voltage: 单个 LED 正向电压 (V)
        led_current: 单个 LED 工作电流 (A)
        num_leds: LED 数量
        arrangement: 连接方式 (parallel/series)
    
    Returns:
        推荐电阻值及参数
    """
    # 边缘情况处理
    if v_supply <= 0:
        return {"error": "电源电压必须大于0"}
    if led_voltage <= 0:
        return {"error": "LED电压必须大于0"}
    if led_current <= 0:
        return {"error": "LED电流必须大于0"}
    if num_leds <= 0:
        return {"error": "LED数量必须大于0"}
    
    if arrangement == "parallel":
        # 并联: 总电流 = 单个电流 × 数量
        total_current = led_current * num_leds
        total_voltage_drop = led_voltage
        # 总电压降 = LED 电压
        # 限流电阻上的电压 = 电源电压 - LED 电压
        resistor_voltage = v_supply - led_voltage
        if resistor_voltage <= 0:
            return {"error": f"电源电压{v_supply}V低于LED电压{led_voltage}V，无法点亮"}
        resistor_value = resistor_voltage / total_current
        power_dissipation = resistor_voltage * total_current
    else:
        # 串联: 总电压 = 单个电压 × 数量
        total_voltage_drop = led_voltage * num_leds
        total_current = led_current  # 串联电流相同
        resistor_voltage = v_supply - total_voltage_drop
        if resistor_voltage <= 0:
            return {"error": f"电源电压{v_supply}V低于{num_leds}个LED串联电压{total_voltage_drop}V，无法点亮"}
        resistor_value = resistor_voltage / total_current
        power_dissipation = resistor_voltage * total_current
    
    # E24 系列标准值
    e24 = E24_RESISTORS
    # 过滤合理的电阻值 (1Ω - 1MΩ)
    e24_filtered = [x for x in e24 if 1 <= x <= 1000000]
    closest_resistor = min(e24_filtered, key=lambda x: abs(x - resistor_value))
    
    # 计算实际电流
    if arrangement == "parallel":
        actual_current_per_led = (v_supply - closest_resistor * total_current / closest_resistor) / closest_resistor if closest_resistor > 0 else 0
    else:
        actual_current_per_led = (v_supply - closest_resistor) / num_leds
    
    return {
        "v_supply": f"{v_supply:.1f}V",
        "led_voltage": f"{led_voltage:.1f}V",
        "led_current": f"{led_current*1000:.0f}mA",
        "num_leds": str(num_leds),
        "arrangement": arrangement,
        "calculated_resistor": f"{resistor_value:.1f}Ω",
        "recommended_resistor": f"{closest_resistor}Ω",
        "resistor_power": f"{power_dissipation*1000:.1f}mW",
        "suggested_power_rating": f"{int(power_dissipation * 2 * 1000)}mW",  # 2倍余量
        "total_power": f"{total_current * v_supply * 1000:.1f}mW",
        "tips": [
            f"{arrangement}连接{num_leds}个LED，总电流{total_current*1000:.0f}mA",
            f"推荐使用{int(power_dissipation * 2 * 1000)}mW以上功率电阻",
            f"建议并联一个{closest_resistor // 10 if closest_resistor >= 10 else 1}Ω均流电阻"
        ]
    }


# ==================== 新增: 简易电感计算器 (v1.1.33) ====================

def calculate_inductor_rough(
    frequency: float = 100000,  # 开关频率 (Hz)
    voltage_in: float = 5.0,  # 输入电压 (V)
    voltage_out: float = 3.3,  # 输出电压 (V)
    current_out: float = 0.5,  # 输出电流 (A)
    ripple_current: float = 0.1,  # 纹波电流 (A)
) -> Dict:
    """
    估算 Buck 降压电路所需电感值 (简化公式)
    
    L = (Vin - Vout) × D / (f × ΔI)
    其中 D = Vout / Vin
    
    Args:
        frequency: 开关频率 (Hz)
        voltage_in: 输入电压 (V)
        voltage_out: 输出电压 (V)
        current_out: 输出电流 (A)
        ripple_current: 纹波电流 (A)
    
    Returns:
        电感估算值及推荐型号
    """
    # 边缘情况处理
    if frequency <= 0:
        return {"error": "频率必须大于0"}
    if voltage_in <= 0:
        return {"error": "输入电压必须大于0"}
    if voltage_out <= 0:
        return {"error": "输出电压必须大于0"}
    if current_out <= 0:
        return {"error": "输出电流必须大于0"}
    if ripple_current <= 0:
        return {"error": "纹波电流必须大于0"}
    if voltage_out >= voltage_in:
        return {"error": "降压电路输出电压必须低于输入电压"}
    
    # 占空比
    duty_cycle = voltage_out / voltage_in
    
    # 电感计算公式
    inductor_value = (voltage_in - voltage_out) * duty_cycle / (frequency * ripple_current)
    
    # 推荐标准电感值 (E12 系列)
    e12_series = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2,
                  10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82,
                  100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820,
                  1000, 1200, 1500, 1800, 2200, 2700, 3300, 3900, 4700, 5600, 6800, 8200,
                  10000, 12000, 15000, 18000, 22000, 27000, 33000, 39000, 47000, 56000, 68000, 82000,
                  100000, 120000, 150000, 180000, 220000, 270000, 330000, 390000, 470000, 560000, 680000, 820000,
                  1000000]
    
    # 过滤合适的值 (单位: μH → 转换为 H 后比较)
    inductor_h = inductor_value * 1e6  # 转换为 μH
    e12_filtered = [x for x in e12_series if x >= inductor_h * 0.8 and x <= inductor_h * 1.5]
    if e12_filtered:
        recommended = min(e12_filtered, key=lambda x: abs(x - inductor_h))
    else:
        recommended = min(e12_series, key=lambda x: abs(x - inductor_h))
    
    # 计算饱和电流 (经验公式: 至少是输出电流的 1.5 倍)
    saturation_current = current_out * 1.5
    
    return {
        "frequency": f"{frequency/1000:.0f}kHz",
        "v_in": f"{voltage_in:.1f}V",
        "v_out": f"{voltage_out:.1f}V",
        "i_out": f"{current_out*1000:.0f}mA",
        "duty_cycle": f"{duty_cycle*100:.1f}%",
        "calculated_inductance": f"{inductor_value*1e6:.1f}μH",
        "recommended_inductance": f"{recommended}μH",
        "recommended_saturation_current": f"{saturation_current*1000:.0f}mA以上",
        "formula": "L = (Vin-Vout) × D / (f × ΔI)",
        "chip_example": "MP2359, LM2596, TPS63000",
        "tips": [
            f"占空比 {duty_cycle*100:.1f}% = {voltage_out:.1f}V / {voltage_in:.1f}V",
            f"推荐使用饱和电流 {saturation_current*1000:.0f}mA 以上的电感",
            f"建议使用带磁屏蔽的功率电感以减少 EMI"
        ]
    }


# ==================== 新增: 电容充电时间计算 (v1.1.33) ====================

def calculate_rc_charge_time(
    resistance: float = 1000,  # 电阻值 (Ω)
    capacitance: float = 100,  # 电容值 (μF)
    target_voltage_ratio: float = 0.632  # 充电到目标电压比例 (1-1/e ≈ 63.2%)
) -> Dict:
    """
    计算 RC 充电时间
    
    V(t) = V0 × (1 - e^(-t/RC))
    t = -RC × ln(1 - V/V0)
    
    Args:
        resistance: 电阻值 (Ω)
        capacitance: 电容值 (μF)
        target_voltage_ratio: 目标电压比例 (默认 63.2% 充满)
    
    Returns:
        充电时间及参数
    """
    # 边缘情况处理
    if resistance <= 0:
        return {"error": "电阻值必须大于0"}
    if capacitance <= 0:
        return {"error": "电容值必须大于0"}
    if target_voltage_ratio <= 0 or target_voltage_ratio >= 1:
        return {"error": "电压比例必须在 0 到 1 之间"}
    
    # 时间常数
    tau = resistance * capacitance * 1e-6  # 转换为秒
    
    # 充电时间
    time_to_target = -tau * math.log(1 - target_voltage_ratio)
    
    # 各时间点的电压
    time_1tau = tau
    time_2tau = 2 * tau
    time_3tau = 3 * tau
    time_5tau = 5 * tau
    
    return {
        "resistance": f"{resistance/1000:.1f}KΩ" if resistance >= 1000 else f"{resistance:.0f}Ω",
        "capacitance": f"{capacitance:.0f}μF",
        "time_constant": f"{tau*1000:.1f}ms",
        "time_to_63.2%": f"{time_1tau*1000:.1f}ms",
        "time_to_86.5%": f"{time_2tau*1000:.1f}ms",
        "time_to_95%": f"{time_3tau*1000:.1f}ms",
        "time_to_99.3%": f"{time_5tau*1000:.1f}ms",
        "formula": "t = -RC × ln(1 - V/V₀)",
        "applications": [
            "按键消抖: 典型 1-10ms",
            "延时启动: 典型 100ms-1s",
            "软启动电路: 典型 10-100ms"
        ]
    }


# ==================== 新增: 线性稳压器散热计算 (v1.1.33) ====================

def calculate_ldo_thermal(
    input_voltage: float = 5.0,  # 输入电压 (V)
    output_voltage: float = 3.3,  # 输出电压 (V)
    output_current: float = 0.1,  # 输出电流 (A)
    ambient_temp: float = 25,  # 环境温度 (°C)
    thermal_resistance_junction_to_case: float = 5,  # RθJC (°C/W)
    thermal_resistance_case_to_ambient: float = 50,  # RθCA (°C/W)
) -> Dict:
    """
    计算 LDO 散热需求
    
    P = (Vin - Vout) × Iout
    Tj = Ta + P × (RθJC + RθCA)
    
    Args:
        input_voltage: 输入电压 (V)
        output_voltage: 输出电压 (V)
        output_current: 输出电流 (A)
        ambient_temp: 环境温度 (°C)
        thermal_resistance_junction_to_case: 结到壳热阻 (°C/W)
        thermal_resistance_case_to_ambient: 壳到环境热阻 (°C/W)
    
    Returns:
        散热计算结果
    """
    # 边缘情况处理
    if input_voltage <= output_voltage:
        return {"error": "输入电压必须大于输出电压"}
    if output_current <= 0:
        return {"error": "输出电流必须大于0"}
    
    # 功耗计算
    power_dissipation = (input_voltage - output_voltage) * output_current
    
    # 总热阻
    total_thermal_resistance = thermal_resistance_junction_to_case + thermal_resistance_case_to_ambient
    
    # 结温计算
    junction_temp = ambient_temp + power_dissipation * total_thermal_resistance
    
    # 不同热阻下的结温
    results = []
    for rca in [20, 50, 100, 200]:
        rt = thermal_resistance_junction_to_case + rca
        tj = ambient_temp + power_dissipation * rt
        results.append({
            "rca": rca,
            "junction_temp": tj,
            "description": "无散热片" if rca < 50 else "小散热片" if rca < 100 else "中散热片" if rca < 150 else "大散热片"
        })
    
    return {
        "input_voltage": f"{input_voltage:.1f}V",
        "output_voltage": f"{output_voltage:.1f}V",
        "output_current": f"{output_current*1000:.0f}mA",
        "power_dissipation": f"{power_dissipation*1000:.1f}mW",
        "ambient_temperature": f"{ambient_temp}°C",
        "calculated_junction_temp": f"{junction_temp:.1f}°C",
        "max_junction_temp": "150°C (典型 LDO)",
        "thermal_design": {
            "no_heatsink": f"{results[0]['junction_temp']:.1f}°C",
            "small_heatsink": f"{results[1]['junction_temp']:.1f}°C",
            "medium_heatsink": f"{results[2]['junction_temp']:.1f}°C",
        },
        "tips": [
            f"LDO 功耗 {power_dissipation*1000:.1f}mW = ({input_voltage:.1f}V - {output_voltage:.1f}V) × {output_current*1000:.0f}mA",
            f"压差 {(input_voltage - output_voltage)*1000:.0f}mV，注意效率",
            "大电流应用建议使用 DC-DC 降压"
        ]
    }


# ==================== 新增: 示波器探头衰减计算 (v1.1.33) ====================

def calculate_probe_attenuation(
    probe_resistance: float = 10000000,  # 探头电阻 (Ω) 默认 10MΩ
    scope_input_resistance: float = 1000000,  # 示波器输入电阻 (Ω) 默认 1MΩ
    attenuation_ratio: float = 10,  # 衰减比 (10x, 100x)
) -> Dict:
    """
    计算示波器探头补偿参数
    
    Args:
        probe_resistance: 探头电阻 (Ω)
        scope_input_resistance: 示波器输入电阻 (Ω)
        attenuation_ratio: 衰减比
    
    Returns:
        探头补偿参数
    """
    # 边缘情况处理
    if scope_input_resistance <= 0:
        return {"error": "示波器输入电阻必须大于0"}
    
    # 补偿电容计算 (目标 20pF)
    target_compensation_capacitance = 20e-12  # 20pF
    
    # 探头内阻应该是示波器的 (衰减比 - 1) 倍
    required_probe_r = scope_input_resistance * (attenuation_ratio - 1)
    
    # 实际探头电阻
    actual_attenuation = probe_resistance / scope_input_resistance + 1
    
    return {
        "probe_resistance": f"{probe_resistance/1000000:.0f}MΩ",
        "scope_input_resistance": f"{scope_input_resistance/1000000:.0f}MΩ",
        "attenuation_ratio": f"{attenuation_ratio}x",
        "actual_attenuation": f"{actual_attenuation:.1f}x",
        "compensation_capacitance": f"{target_compensation_capacitance*1e12:.0f}pF",
        "recommended_compensation": "调节探头电容至方波边缘平直",
        "tips": [
            "使用 10x 探头时，示波器应切换到 1MΩ 输入模式",
            "使用 100x 探头时，示波器应切换到高阻抗输入模式",
            "每次测量前用校准信号检查探头补偿"
        ]
    }
