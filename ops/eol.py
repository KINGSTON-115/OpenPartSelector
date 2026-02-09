"""
🚨 器件生命周期与停产预警模块
每年47万+器件EOL，这是选型最大的隐藏风险！
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import re

# ==================== 常见停产/濒危器件 ====================

EOL_WARNING_PARTS = {
    # STM32 停产预警
    "STM32F103C8T6": {
        "status": "NRND",  # Not Recommended for New Designs
        "lifecycle": "Mature",
        "replacement": "STM32G431CBU6",
        "replacement_reason": "更低功耗，更多外设，pin2pin兼容",
        "last_update": "2024-Q4",
        "risk_level": "medium"
    },
    "STM32F103CBT6": {
        "status": "NRND",
        "lifecycle": "Mature", 
        "replacement": "STM32G473CBT6",
        "replacement_reason": "Cortex-M4内核，更强性能",
        "last_update": "2024-Q4",
        "risk_level": "medium"
    },
    
    # 常见濒危器件
    "ATMEGA328P": {
        "status": "Active",
        "lifecycle": "Mature",
        "replacement": "AVR DD",
        "replacement_reason": "Microchip新一代AVR，更低功耗",
        "last_update": "2024-Q3",
        "risk_level": "low"
    },
    "NE555": {
        "status": "Active",
        "lifecycle": "Mature",
        "replacement": "TLC555",
        "replacement_reason": "CMOS版本，更低功耗",
        "last_update": "2024-Q2",
        "risk_level": "low"
    },
    
    # ESP32 系列
    "ESP32-WROOM-32": {
        "status": "Active",
        "lifecycle": "Mature",
        "replacement": "ESP32-C3",
        "replacement_reason": "RISC-V内核，更便宜，更省电",
        "last_update": "2024-Q3",
        "risk_level": "low"
    },
    
    # 电源器件
    "LM7805": {
        "status": "Active",
        "lifecycle": "Mature",
        "replacement": "TPS7A4700",
        "replacement_reason": "更低噪声，更高PSRR",
        "last_update": "2024-Q1",
        "risk_level": "low"
    },
    
    # CH340 系列
    "CH340G": {
        "status": "Active",
        "lifecycle": "Mature",
        "replacement": "CH340N",
        "replacement_reason": "无需外接晶振，更低成本",
        "last_update": "2024-Q2",
        "risk_level": "low"
    },
}

# ==================== 器件生命周期状态 ====================

LIFECYCLE_STATUS = {
    "Active": {
        "cn": "活跃",
        "color": "green",
        "risk": "低",
        "description": "正常供货，推荐使用"
    },
    "NRND": {
        "cn": "不推荐新设计",
        "color": "yellow", 
        "risk": "中",
        "description": "可继续使用，但不建议新设计"
    },
    "LastTimeBuy": {
        "cn": "最后购买期",
        "color": "orange",
        "risk": "高",
        "description": "即将停产，需抓紧备货"
    },
    "Obsolete": {
        "cn": "已停产",
        "color": "red",
        "risk": "极高",
        "description": "已停产，需替换"
    },
    "Pending": {
        "cn": "待定",
        "color": "gray",
        "risk": "未知",
        "description": "状态待定，需关注"
    }
}

# ==================== 供应链风险评估 ====================

SUPPLY_CHAIN_RISKS = {
    "STM32": {
        "overall_risk": "medium",
        "factors": [
            "ST晶圆厂产能稳定",
            "国产替代(GD32)成熟",
            "价格相对平稳"
        ],
        "建议": "可以考虑国产替代以降低风险"
    },
    "ESP32": {
        "overall_risk": "low",
        "factors": [
            "乐鑫产能充足",
            "价格稳定",
            "国产平替多"
        ],
        "建议": "库存管理正常即可"
    },
    "模拟器件": {
        "overall_risk": "medium-high",
        "factors": [
            "TI/ADI供应链调整",
            "部分型号交期较长",
            "国产替代逐步跟上"
        ],
        "建议": "关注交期，提前备货"
    },
    "连接器": {
        "overall_risk": "high",
        "factors": [
            "原材料涨价",
            "部分型号缺货",
            "交期延长"
        ],
        "建议": "优先选用常见型号"
    },
    "被动器件": {
        "overall_risk": "low",
        "factors": [
            "国产品牌崛起",
            "价格稳定",
            "供应充足"
        ],
        "建议": "可优先考虑国产品牌降低成本"
    }
}


@dataclass
class EOLWarning:
    """停产预警信息"""
    part_number: str
    status: str  # Active/NRND/LastTimeBuy/Obsolete
    lifecycle: str  # New/Mature/LastOrder/NotForNewDesign/Obsolete
    replacement: Optional[str]
    replacement_reason: Optional[str]
    last_update: str
    risk_level: str  # low/medium/high/critical
    warnings: List[str]


class EOLChecker:
    """器件生命周期检查器"""
    
    def __init__(self):
        self.database = EOL_WARNING_PARTS
        self.status_info = LIFECYCLE_STATUS
    
    def check_part(self, part_number: str) -> EOLWarning:
        """
        检查器件的生命周期状态
        
        Args:
            part_number: 器件型号
            
        Returns:
            EOLWarning: 包含预警信息
        """
        # 模糊匹配
        for key, data in self.database.items():
            if key.upper() in part_number.upper() or part_number.upper() in key.upper():
                return EOLWarning(
                    part_number=key,
                    status=data["status"],
                    lifecycle=data["lifecycle"],
                    replacement=data.get("replacement"),
                    replacement_reason=data.get("replacement_reason"),
                    last_update=data["last_update"],
                    risk_level=data["risk_level"],
                    warnings=self._generate_warnings(key, data)
                )
        
        # 返回未知状态
        return EOLWarning(
            part_number=part_number,
            status="Unknown",
            lifecycle="Unknown",
            replacement=None,
            replacement_reason=None,
            last_update="Unknown",
            risk_level="unknown",
            warnings=["⚠️ 未在数据库中，请手动查询原厂网站"]
        )
    
    def _generate_warnings(self, part_number: str, data: Dict) -> List[str]:
        """生成预警信息"""
        warnings = []
        
        if data["status"] == "NRND":
            warnings.append(f"⚠️ {part_number} 已不推荐新设计使用")
            if data.get("replacement"):
                warnings.append(f"💡 建议替换为: {data['replacement']}")
        
        elif data["status"] == "LastTimeBuy":
            warnings.append(f"🚨 {part_number} 处于最后购买期，请抓紧备货!")
        
        elif data["status"] == "Obsolete":
            warnings.append(f"❌ {part_number} 已停产，必须替换!")
        
        if data["risk_level"] in ["medium", "high", "critical"]:
            warnings.append(f"📊 风险等级: {data['risk_level'].upper()}")
        
        return warnings
    
    def check_bom_risk(self, bom: List[Dict]) -> Dict:
        """
        检查整个BOM的供应链风险
        
        Args:
            bom: BOM列表 [{'part_number': 'xxx'}, ...]
            
        Returns:
            风险评估报告
        """
        risk_summary = {
            "total_parts": len(bom),
            "risk_counts": {"low": 0, "medium": 0, "high": 0, "critical": 0, "unknown": 0},
            "warnings": [],
            "recommendations": []
        }
        
        for item in bom:
            part = item.get("part_number", "")
            if not part:
                continue
                
            warning = self.check_part(part)
            risk_level = warning.risk_level or "unknown"
            risk_summary["risk_counts"][risk_level] = risk_summary["risk_counts"].get(risk_level, 0) + 1
            
            # 收集高风险预警
            if risk_level in ["high", "critical"]:
                risk_summary["warnings"].append({
                    "part_number": part,
                    "status": warning.status,
                    "risk": risk_level,
                    "replacement": warning.replacement
                })
        
        # 生成建议
        if risk_summary["warnings"]:
            risk_summary["recommendations"].append(
                f"🚨 发现 {len(risk_summary['warnings'])} 个高风险器件，建议替换"
            )
        
        # 计算整体风险
        total_risks = sum(risk_summary["risk_counts"].values())
        if total_risks > 0:
            high_ratio = (risk_summary["risk_counts"]["high"] + 
                         risk_summary["risk_counts"]["critical"]) / total_risks
            if high_ratio > 0.3:
                risk_summary["overall_risk"] = "HIGH"
                risk_summary["recommendations"].append(
                    "⚠️ BOM中超过30%为高风险器件，请重新评估选型"
                )
            elif high_ratio > 0.1:
                risk_summary["overall_risk"] = "MEDIUM"
            else:
                risk_summary["overall_risk"] = "LOW"
        
        return risk_summary
    
    def get_supply_chain_advice(self, category: str) -> Dict:
        """
        获取供应链建议
        
        Args:
            category: 器件类别 (MCU/模拟/连接器/被动等)
            
        Returns:
            供应链建议
        """
        category_lower = category.lower()
        
        for key, advice in SUPPLY_CHAIN_RISKS.items():
            if key.lower() in category_lower or category_lower in key.lower():
                return advice
        
        return {
            "overall_risk": "unknown",
            "factors": ["请查阅最新供应链报告"],
            "建议": "建议咨询供应商了解最新情况"
        }


# ==================== 便捷函数 ====================

def check_component_lifecycle(part_number: str) -> Dict:
    """检查器件生命周期状态"""
    checker = EOLChecker()
    warning = checker.check_part(part_number)
    
    return {
        "part_number": warning.part_number,
        "status": warning.status,
        "status_cn": LIFECYCLE_STATUS.get(warning.status, {}).get("cn", "未知"),
        "lifecycle": warning.lifecycle,
        "replacement": warning.replacement,
        "replacement_reason": warning.replacement_reason,
        "risk_level": warning.risk_level,
        "warnings": warning.warnings
    }


def analyze_bom_risk(bom: List[Dict]) -> Dict:
    """分析BOM供应链风险"""
    checker = EOLChecker()
    return checker.check_bom_risk(bom)


def get_supply_chain_recommendation(category: str) -> Dict:
    """获取供应链建议"""
    checker = EOLChecker()
    return checker.get_supply_chain_advice(category)
