"""
OpenPartSelector - AI 电子元器件智能选型引擎
AI-Driven Electronic Component Selection Engine

核心模块:
- Agent: AI 选型 Agent
- Config: 配置管理
- Search: 多平台搜索引擎
- Parser: Datasheet 解析
- Knowledge: 向量知识库
- Database: 内置器件数据库
- JLC: 嘉立创生态集成
- Features: 锦上添花功能
- EOL: 停产预警
- CAD: CAD库集成
- BOM: BOM完整分析
- i18n: 国际化支持
"""

from .config import Config
from .agent import Agent, SelectionResult, quick_select
from .database import search_components, get_price_comparison, get_alternatives
from .jlc import search_jlc, calculate_jlc_smt, get_jlc_footprint, export_jlc_bom
from .features import find_alternatives, get_circuit_template, get_datasheet_summary
from .features import (
    calculate_resistor_for_led, calculate_voltage_divider, calculate_pwm_frequency,
    calculate_led_resistor, calculate_rc_time_constant, calculate_capacitor_ripple,
    calculate_led_parallel_resistor, calculate_battery_life, calculate_voltage_reference
)
# 注意: calculate_led_series_resistor 已合并到 calculate_led_resistor()，不再导出
from .eol import check_component_lifecycle, analyze_bom_risk
from .cad import search_cad_library, check_cad_availability
from .bom import analyze_bom_full, quick_bom_check

__version__ = "1.1.28.1"
__author__ = "KINGSTON-115"

__all__ = [
    "Config",
    "Agent", 
    "SelectionResult",
    "quick_select",
    "search_components",
    "get_price_comparison", 
    "get_alternatives",
    "search_jlc",
    "calculate_jlc_smt",
    "get_jlc_footprint",
    "export_jlc_bom",
    "find_alternatives",
    "get_circuit_template",
    "get_datasheet_summary",
    "calculate_resistor_for_led",
    "calculate_voltage_divider",
    "calculate_pwm_frequency",
    "calculate_led_resistor",
    "calculate_rc_time_constant",
    "calculate_capacitor_ripple",
    "calculate_led_parallel_resistor",
    "calculate_battery_life",
    "calculate_voltage_reference",
    "check_component_lifecycle",
    "analyze_bom_risk",
    "search_cad_library",
    "check_cad_availability",
    "analyze_bom_full",
    "quick_bom_check",
]
