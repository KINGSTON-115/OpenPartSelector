"""
工具函数模块
"""
import logging
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
        ts = datetime.utcnow()
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


def estimate_price(quantity: int = 1) -> float:
    """
    估算价格 (基于常见价格曲线)
    
    TODO: 接入真实价格数据
    """
    base_price = 0.50  # 基础价格
    
    # 简单线性折扣
    if quantity >= 100:
        base_price *= 0.7
    if quantity >= 1000:
        base_price *= 0.5
    if quantity >= 10000:
        base_price *= 0.3
    
    return base_price * quantity


def generate_bom_id() -> str:
    """生成 BOM ID"""
    import hashlib
    timestamp = str(datetime.utcnow().timestamp())
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


# 导入 re 用于正则表达式
import re
