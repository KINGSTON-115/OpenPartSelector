"""
🔥 锦上添花功能 - 最被需要的特性
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import json


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
    """计算LED限流电阻"""
    v_r = voltage - led_voltage
    if v_r <= 0:
        return {"error": "输入电压必须大于LED压降"}
    
    r = v_r / led_current
    power = v_r * led_current
    
    # 查找最近的标准电阻值
    e24_values = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91, 100]
    e12_values = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
    
    # 选择合适的系列
    if r < 100:
        standard = min(e24_values, key=lambda x: abs(x - r))
    else:
        standard = min(e12_values, key=lambda x: abs(x - r))
    
    return {
        "input_voltage": f"{voltage}V",
        "led_voltage": f"{led_voltage}V",
        "led_current": f"{led_current*1000:.0f}mA",
        "calculated_resistance": f"{r:.0f}",
        "recommended_resistance": f"{standard}",
        "power_dissipation": f"{power*1000:.1f}mW",
        "power_rating": "1/4W (建议用1W如果功率大)",
        "formula": f"R = (Vcc - Vled) / Iled"
    }


def calculate_voltage_divider(
    v_in: float = 5.0,
    v_out: float = 3.3,
    r1: float = None  # 如果为None则自动计算
) -> Dict:
    """计算分压电阻"""
    if r1 is None:
        # 假设R2=10K，计算R1
        r2 = 10000
        r1 = r2 * (v_in / v_out - 1)
    else:
        r2 = r1 * v_out / (v_in - v_out)
    
    # 标准化
    e24 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 51, 68, 100]
    
    r1_std = min(e24, key=lambda x: abs(x * 1000 - r1))
    r2_std = min(e24, key=lambda x: abs(x * 1000 - r2))
    
    actual_vout = v_in * r2_std * 1000 / (r1_std * 1000 + r2_std * 1000)
    
    return {
        "input_voltage": f"{v_in}V",
        "desired_output": f"{v_out}V",
        "calculated_r1": f"{r1/1000:.1f}KΩ",
        "calculated_r2": f"{r2/1000:.1f}KΩ",
        "recommended_r1": f"{r1_std}KΩ",
        "recommended_r2": f"{r2_std}KΩ",
        "actual_output": f"{actual_vout:.2f}V",
        "formula": "Vout = Vin × R2 / (R1 + R2)"
    }


def calculate_pwm_frequency(
    timer_clock: float = 72000000,  # STM32默认72MHz
    prescaler: int = 7199,
    auto_reload: int = 99
) -> Dict:
    """计算PWM频率"""
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
