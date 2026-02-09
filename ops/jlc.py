"""
嘉立创/立创商城集成模块
🇨🇺 China: JLC (JiaLiChuang) & LCSC Integration
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re
import logging

logger = logging.getLogger(__name__)


# ==================== 嘉立创特有数据 ====================

# 立创商城热门器件 (中国学生常用)
JLC_HOT_PARTS = [
    {
        "part_number": "C10047",
        "type": "ESP-12F",
        "description": "ESP8266 WiFi Module",
        "manufacturer": "Espressif",
        "category": "wireless",
        "price_10pcs": 7.50,
        "price_100pcs": 6.80,
        "stock": 15230,
        "jlc_category": "无线模块",
        "jlc_link": "https://item.szlcsc.com/10047.html",
        "specs": {
            "voltage": "3.0-3.6V",
            "frequency": "2.4GHz",
            "protocol": "WiFi 802.11b/g/n",
        }
    },
    {
        "part_number": "C14663",
        "type": "ESP32-C3FH4",
        "description": "ESP32-C3 WiFi/BT Module",
        "manufacturer": "Espressif",
        "category": "wireless",
        "price_10pcs": 9.80,
        "price_100pcs": 8.50,
        "stock": 8500,
        "jlc_category": "无线模块",
        "jlc_link": "https://item.szlcsc.com/14663.html",
        "specs": {
            "voltage": "3.0-3.6V",
            "frequency": "2.4GHz",
            "protocol": "WiFi + BT 5.0",
        }
    },
    {
        "part_number": "C10488",
        "type": "CH340C",
        "description": "USB to UART Converter SOP-16",
        "manufacturer": "WCH",
        "category": "interface",
        "price_10pcs": 1.80,
        "price_100pcs": 1.30,
        "stock": 52000,
        "jlc_category": "USB芯片",
        "jlc_link": "https://item.szlcsc.com/10488.html",
        "specs": {
            "voltage": "5V/3.3V",
            "baudrate": "2Mbps",
        }
    },
    {
        "part_number": "C4033",
        "type": "AMS1117-3.3",
        "description": "LDO 3.3V 1A SOT-223",
        "manufacturer": "AMS",
        "category": "power",
        "price_10pcs": 0.80,
        "price_100pcs": 0.50,
        "stock": 280000,
        "jlc_category": "稳压芯片",
        "jlc_link": "https://item.szlcsc.com/4033.html",
        "specs": {
            "voltage_in": "4.7-12V",
            "voltage_out": "3.3V",
            "current": "1A",
        }
    },
    {
        "part_number": "C11449",
        "type": "GD32F103C8T6",
        "description": "ARM Cortex-M3 64KB Flash",
        "manufacturer": "GigaDevice",
        "category": "mcu",
        "price_10pcs": 8.50,
        "price_100pcs": 7.20,
        "stock": 18500,
        "jlc_category": "MCU",
        "jlc_link": "https://item.szlcsc.com/11449.html",
        "specs": {
            "core": "Cortex-M3",
            "frequency": "108MHz",
            "flash": "64KB",
            "voltage": "2.6-3.6V",
        }
    },
    {
        "part_number": "C12743",
        "type": "RP2040",
        "description": "Raspberry Pi Dual Cortex-M0+",
        "manufacturer": "Raspberry Pi",
        "category": "mcu",
        "price_10pcs": 9.80,
        "price_100pcs": 8.80,
        "stock": 6500,
        "jlc_category": "MCU",
        "jlc_link": "https://item.szlcsc.com/12743.html",
        "specs": {
            "core": "Dual Cortex-M0+",
            "frequency": "133MHz",
            "ram": "264KB",
            "voltage": "1.8-3.3V",
        }
    },
    {
        "part_number": "C8580",
        "type": "NE555P",
        "description": "Precision Timer DIP-8",
        "manufacturer": "TI",
        "category": "analog",
        "price_10pcs": 0.50,
        "price_100pcs": 0.35,
        "stock": 45000,
        "jlc_category": "时基电路",
        "jlc_link": "https://item.szlcsc.com/8580.html",
        "specs": {
            "voltage": "4.5-16V",
            "frequency": "500kHz",
        }
    },
    {
        "part_number": "C10943",
        "type": "TPS63000DSJR",
        "description": "Buck-Boost Converter 3.3V",
        "manufacturer": "TI",
        "category": "power",
        "price_10pcs": 15.00,
        "price_100pcs": 13.00,
        "stock": 3200,
        "jlc_category": "电源模块",
        "jlc_link": "https://item.szlcsc.com/10943.html",
        "specs": {
            "vin": "1.8-5.5V",
            "vout": "3.3V",
            "efficiency": "96%",
        }
    },
]


# 嘉立创EDA常用封装库
JLC_FOOTPRINTS = {
    "SOP-8": {
        "jlc_footprint": "SOP-8-3.9",
        "pitch": "1.27mm",
        "body_size": "4.9 x 3.9mm",
        "land_pattern": "Standard",
    },
    "SOT-23-5": {
        "jlc_footprint": "SOT-23-5",
        "pitch": "0.95mm",
        "body_size": "2.9 x 1.6mm",
        "land_pattern": "Standard",
    },
    "SOT-223": {
        "jlc_footprint": "SOT-223",
        "pitch": "2.3mm",
        "body_size": "6.7 x 3.7mm",
        "land_pattern": "Standard",
    },
    "LQFP-48": {
        "jlc_footprint": "LQFP-48-7x7",
        "pitch": "0.5mm",
        "body_size": "7x7mm",
        "land_pattern": "Standard",
    },
    "QFN-24": {
        "jlc_footprint": "QFN-24-4x4",
        "pitch": "0.5mm",
        "body_size": "4x4mm",
        "land_pattern": "EP",
    },
    "DIP-8": {
        "jlc_footprint": "DIP-8-300",
        "pitch": "2.54mm",
        "body_size": "9.4 x 6.4mm",
        "land_pattern": "Through-Hole",
    },
    "ESP-12F": {
        "jlc_footprint": "ESP-12F",
        "pitch": "1.5mm",
        "body_size": "24x16mm",
        "module_type": "SMD Module",
    },
    "CH340C": {
        "jlc_footprint": "SOP-16-3.9",
        "pitch": "1.27mm",
        "body_size": "9.9 x 3.9mm",
    },
}


@dataclass
class JLCSMTPrice:
    """SMT 贴片价格"""
    smt_side: str           # 单面/双面
    dot_count: int          # 焊dot_count量
    base_price: float       # 起步价
    unit_price: float       # 每个点的价格
    
    def calculate(self) -> float:
        """计算SMT费用"""
        points = max(self.dot_count, 80)  # 至少80点
        return self.base_price + points * self.unit_price


# 嘉立创SMT贴片价格 (2024参考)
JLC_SMT_PRICING = {
    "single": JLCSMTPrice("single", 0, 8.00, 0.015),
    "double": JLCSMTPrice("double", 0, 12.00, 0.025),
}


class JLCEda:
    """嘉立创EDA 集成"""
    
    def __init__(self):
        self.base_url = "https://lceda.cn"
        self.api_url = "https://api.lceda.cn"
    
    def search_component_on_jlc(self, keyword: str) -> List[Dict]:
        """
        在立创商城搜索器件
        
        返回JLC特有信息: 货号、价格、库存
        """
        results = []
        
        for part in JLC_HOT_PARTS:
            # 关键词匹配
            keyword_lower = keyword.lower()
            search_text = f"{part['type']} {part['description']} {part['manufacturer']}".lower()
            
            if keyword_lower in search_text or any(k in search_text for k in keyword_lower.split()):
                results.append({
                    "jlc_part_number": part["part_number"],
                    "type": part["type"],
                    "description": part["description"],
                    "manufacturer": part["manufacturer"],
                    "category": part["category"],
                    "price_10pcs": part["price_10pcs"],
                    "price_100pcs": part["price_100pcs"],
                    "stock": part["stock"],
                    "jlc_category": part["jlc_category"],
                    "jlc_link": part["jlc_link"],
                    "specs": part["specs"],
                })
        
        return results
    
    def get_footprint_info(self, package: str) -> Dict:
        """获取封装信息 (嘉立创EDA封装库)"""
        package_upper = package.upper()
        
        for pkg, info in JLC_FOOTPRINTS.items():
            if pkg in package_upper:
                return {
                    "package": package,
                    "jlc_footprint_id": info.get("jlc_footprint", ""),
                    "pitch": info.get("pitch", ""),
                    "body_size": info.get("body_size", ""),
                    "jlc_link": f"https://lceda.cn/footprint/{info.get('jlc_footprint', '')}"
                }
        
        return {
            "package": package,
            "jlc_footprint_id": None,
            "message": "请在嘉立创EDA中搜索对应封装"
        }
    
    def calculate_smt_cost(self, bom: List[Dict], double_side: bool = False) -> Dict:
        """
        计算SMT贴片费用
        
        Args:
            bom: BOM清单 (含数量)
            double_side: 是否双面贴片
            
        Returns:
            SMT费用明细
        """
        # 统计焊dot_count量 (粗略估算: 每个器件约4-20个焊点)
        pin_count_map = {
            "SOP-8": 8, "SOP-16": 16, "SOP-14": 14,
            "QFN-24": 24, "QFN-32": 32, "QFN-48": 48,
            "LQFP-48": 48, "LQFP-64": 64,
            "SOT-23": 3, "SOT-23-5": 5, "SOT-223": 4,
            "DIP-8": 8, "DIP-16": 16, "DIP-28": 28,
            "ESP-12F": 16,
            "CH340C": 16,
            "Resistor": 2, "Capacitor": 2,
        }
        
        total_points = 0
        for item in bom:
            pins = pin_count_map.get(item.get("package", ""), 4)
            qty = item.get("quantity", 1)
            total_points += pins * qty
        
        # 计算费用
        pricing = JLC_SMT_PRICING["double"] if double_side else JLC_SMT_PRICING["single"]
        
        # 最小点80
        actual_points = max(total_points, 80)
        smt_cost = pricing.base_price + actual_points * pricing.unit_price
        
        return {
            "smt_type": pricing.smt_side,
            "estimated_points": actual_points,
            "base_price": pricing.base_price,
            "price_per_point": pricing.unit_price,
            "total_smt_cost": round(smt_cost, 2),
            "unit": "CNY",
            "notes": [
                "以上价格为SMT加工费(不含器件费用)",
                "最小订单: 5片起",
                "包含: 贴片 + 回流焊接 + AOI检测",
            ]
        }
    
    def generate_jlc_bom(self, parts: List[Dict]) -> Dict:
        """
        生成嘉立创格式BOM
        
        用于直接导入立创商城采购
        """
        items = []
        total_cost = 0
        
        for i, part in enumerate(parts, 1):
            jlc_info = self.search_component_on_jlc(part.get("part_number", ""))
            
            if jlc_info:
                jlc = jlc_info[0]
                qty = part.get("quantity", 1)
                price = jlc.get("price_10pcs", 0) if qty <= 10 else jlc.get("price_100pcs", 0)
            else:
                price = 0
            
            items.append({
                "序号": i,
                "型号": part.get("part_number", ""),
                "位号": part.get("reference", f"U{i}"),
                "数量": part.get("quantity", 1),
                "单价": price,
                "小计": round(price * qty, 2),
                "备注": jlc_info[0].get("jlc_category", "") if jlc_info else "",
                "立创商城链接": jlc_info[0].get("jlc_link", "") if jlc_info else "",
            })
            
            total_cost += price * qty
        
        return {
            "platform": "立创商城 (LCSC)",
            "items": items,
            "total_estimated_cost": round(total_cost, 2),
            "currency": "CNY",
            "import_guide": "可将型号列复制到立创商城搜索购买"
        }


class LCSCClient:
    """立创商城API客户端"""
    
    BASE_URL = "https://api.lcsc.com"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    async def search_parts(self, keyword: str, limit: int = 20) -> List[Dict]:
        """
        搜索器件
        
        TODO: 接入立创API (需要API Key)
        """
        # 目前返回模拟数据
        from .. import database
        results = database.search_components(keyword, limit=limit)
        
        # 添加JLC特有信息
        jlc = JLCEda()
        jlc_results = jlc.search_component_on_jlc(keyword)
        
        for r in results:
            r["source"] = "builtin"
        
        return results + jlc_results
    
    async def get_price(self, part_number: str) -> Dict:
        """获取价格和库存"""
        from .. import database
        return database.get_price_comparison(part_number)


# 便捷函数
def search_jlc(keyword: str) -> List[Dict]:
    """搜索嘉立创器件"""
    jlc = JLCEda()
    return jlc.search_component_on_jlc(keyword)


def get_jlc_footprint(package: str) -> Dict:
    """获取嘉立创EDA封装信息"""
    jlc = JLCEda()
    return jlc.get_footprint_info(package)


def calculate_jlc_smt(bom: List[Dict], double_side: bool = False) -> Dict:
    """计算嘉立创SMT费用"""
    jlc = JLCEda()
    return jlc.calculate_smt_cost(bom, double_side)


def export_jlc_bom(parts: List[Dict]) -> Dict:
    """导出嘉立创格式BOM"""
    jlc = JLCEda()
    return jlc.generate_jlc_bom(parts)
