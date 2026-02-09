"""
📋 完整 BOM 分析模块 - 解决选型最大痛点！
一站式分析: 价格 / 停产风险 / CAD库 / 供应链
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class BOMItem:
    """BOM 项"""
    part_number: str
    quantity: int = 1
    reference: str = ""
    description: str = ""
    manufacturer: str = ""
    unit_price: float = 0.0
    total_price: float = 0.0
    
    # 分析结果
    lifecycle_status: str = ""
    lifecycle_risk: str = ""
    cad_availability: str = ""
    supply_chain_risk: str = ""
    replacement: str = ""
    replacement_reason: str = ""


@dataclass
class BOMAnalysis:
    """完整 BOM 分析报告"""
    items: List[BOMItem]
    
    # 汇总信息
    total_items: int = 0
    total_quantity: int = 0
    total_price: float = 0.0
    
    # 风险评估
    high_risk_count: int = 0
    cad_missing_count: int = 0
    price_warnings: List[str] = field(default_factory=list)
    
    # 建议
    replacements: List[Dict] = field(default_factory=list)
    cost_savings: float = 0.0
    risk_reductions: List[str] = field(default_factory=list)


class BOMAnalyzer:
    """BOM 完整分析器"""
    
    def __init__(self):
        from .eol import EOLChecker
        from .cad import CADLibrary集成
        
        self.eol_checker = EOLChecker()
        self.cad_engine = CADLibrary集成()
    
    def analyze_bom(self, bom: List[Dict]) -> BOMAnalysis:
        """
        完整分析 BOM
        
        分析维度:
        1. 生命周期与停产风险
        2. CAD 资源可用性
        3. 供应链风险
        4. 价格分析
        5. 替代方案推荐
        """
        items = []
        
        for i, item in enumerate(bom):
            part_number = item.get("part_number", "")
            if not part_number:
                continue
            
            quantity = item.get("quantity", 1)
            unit_price = item.get("price", 0.0)
            
            bom_item = BOMItem(
                part_number=part_number,
                quantity=quantity,
                reference=item.get("reference", f"U{i+1}"),
                unit_price=unit_price,
                total_price=unit_price * quantity
            )
            
            # 1. 检查生命周期
            from .eol import check_component_lifecycle
            lifecycle = check_component_lifecycle(part_number)
            bom_item.lifecycle_status = lifecycle.get("status", "Unknown")
            bom_item.lifecycle_risk = lifecycle.get("risk_level", "unknown")
            bom_item.replacement = lifecycle.get("replacement", "")
            bom_item.replacement_reason = lifecycle.get("replacement_reason", "")
            
            # 2. 检查 CAD 可用性
            cad = self.cad_engine.check_availability(part_number)
            if cad.get("overall_status") == "Available":
                bom_item.cad_availability = "✅ 完整"
            else:
                bom_item.cad_availability = "⚠️ 部分或缺失"
            
            # 3. 供应链风险 (简化)
            bom_item.supply_chain_risk = self._assess_supply_risk(part_number)
            
            items.append(bom_item)
        
        # 生成汇总
        analysis = BOMAnalysis(items=items)
        
        analysis.total_items = len(items)
        analysis.total_quantity = sum(item.quantity for item in items)
        analysis.total_price = sum(item.total_price for item in items)
        
        # 统计高风险
        for item in items:
            if item.lifecycle_risk in ["high", "critical"]:
                analysis.high_risk_count += 1
            if "✅" not in item.cad_availability:
                analysis.cad_missing_count += 1
        
        # 价格警告
        for item in items:
            if item.unit_price > 10:
                analysis.price_warnings.append(
                    f"⚠️ {item.part_number} 单价 ¥{item.unit_price:.2f}，可考虑替代"
                )
        
        # 替代方案
        for item in items:
            if item.replacement:
                analysis.replacements.append({
                    "original": item.part_number,
                    "replacement": item.replacement,
                    "reason": item.replacement_reason,
                    "reference": item.reference
                })
                # 估算节省 (假设替代便宜30%)
                analysis.cost_savings += item.total_price * 0.3
        
        # 风险降低建议
        if analysis.high_risk_count > 0:
            analysis.risk_reductions.append(
                f"🚨 发现 {analysis.high_risk_count} 个高风险器件，请查看替代方案"
            )
        
        if analysis.cad_missing_count > 0:
            analysis.risk_reductions.append(
                f"🔌 {analysis.cad_missing_count} 个器件缺少 CAD 资源，请下载符号/封装"
            )
        
        return analysis
    
    def _assess_supply_risk(self, part_number: str) -> str:
        """评估供应链风险"""
        part_upper = part_number.upper()
        
        risk_map = {
            "STM32": "⚡ 中等风险 - 建议国产替代",
            "ESP32": "✅ 低风险 - 供货稳定",
            "CH340": "✅ 低风险 - 国产充足",
            "LM": "⚡ 中等风险 - 关注交期",
            "NE": "✅ 低风险 - 成熟产品",
            "AMS": "⚡ 中等风险 - 关注库存",
        }
        
        for key, risk in risk_map.items():
            if key in part_upper:
                return risk
        
        return "ℹ️ 正常 - 持续关注"
    
    def generate_report(self, analysis: BOMAnalysis) -> str:
        """生成中文分析报告"""
        report = []
        
        report.append("="*70)
        report.append("📋 OpenPartSelector BOM 完整分析报告")
        report.append("="*70)
        report.append(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        # 汇总
        report.append("📊 BOM 汇总")
        report.append("-"*40)
        report.append(f"  器件种类: {analysis.total_items}")
        report.append(f"  总数量: {analysis.total_quantity}")
        report.append(f"  预估总价: ¥{analysis.total_price:.2f}")
        report.append("")
        
        # 风险汇总
        report.append("🚨 风险评估")
        report.append("-"*40)
        report.append(f"  高风险器件: {analysis.high_risk_count} 个")
        report.append(f"  CAD缺失: {analysis.cad_missing_count} 个")
        report.append(f"  预估节省: ¥{analysis.cost_savings:.2f}")
        report.append("")
        
        # 器件详情
        report.append("📦 器件详情")
        report.append("-"*40)
        
        for item in analysis.items:
            risk_emoji = "🟢" if item.lifecycle_risk == "low" else "🟡" if item.lifecycle_risk == "medium" else "🔴"
            
            report.append(f"\n{item.reference}. {item.part_number}")
            report.append(f"   数量: {item.quantity} | 单价: ¥{item.unit_price:.2f}")
            report.append(f"   {risk_emoji} 生命周期: {item.lifecycle_status} ({item.lifecycle_risk})")
            report.append(f"   🔌 CAD: {item.cad_availability}")
            report.append(f"   🚚 供应链: {item.supply_chain_risk}")
            
            if item.replacement:
                report.append(f"   💡 建议替换: {item.replacement}")
        
        # 替代方案
        if analysis.replacements:
            report.append("\n" + "="*40)
            report.append("💰 成本优化建议")
            report.append("="*40)
            
            for r in analysis.replacements:
                report.append(f"\n  🔄 {r['original']} → {r['replacement']}")
                report.append(f"     原因: {r['reason']}")
        
        # 风险降低建议
        if analysis.risk_reductions:
            report.append("\n" + "="*40)
            report.append("🎯 行动建议")
            report.append("="*40)
            
            for suggestion in analysis.risk_reductions:
                report.append(f"\n  {suggestion}")
        
        report.append("\n" + "="*70)
        report.append("✅ 分析完成")
        report.append("="*70)
        
        return "\n".join(report)
    
    def export_bom_with_analysis(self, bom: List[Dict]) -> Dict:
        """导出带分析的BOM"""
        analysis = self.analyze_bom(bom)
        
        return {
            "bom_items": [
                {
                    "reference": item.reference,
                    "part_number": item.part_number,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                    "lifecycle_status": item.lifecycle_status,
                    "lifecycle_risk": item.lifecycle_risk,
                    "cad_availability": item.cad_availability,
                    "supply_chain_risk": item.supply_chain_risk,
                    "replacement": item.replacement,
                }
                for item in analysis.items
            ],
            "summary": {
                "total_items": analysis.total_items,
                "total_quantity": analysis.total_quantity,
                "total_price": analysis.total_price,
                "high_risk_count": analysis.high_risk_count,
                "estimated_savings": analysis.cost_savings,
            },
            "recommendations": analysis.replacements,
            "report": self.generate_report(analysis)
        }


# ==================== 便捷函数 ====================

def analyze_bom_full(bom: List[Dict]) -> Dict:
    """
    一键分析BOM
    
    Args:
        bom: BOM列表 [
            {"part_number": "STM32F103C8T6", "quantity": 1, "price": 0.95},
            ...
        ]
    
    Returns:
        完整分析报告
    """
    analyzer = BOMAnalyzer()
    return analyzer.export_bom_with_analysis(bom)


def quick_bom_check(bom: List[Dict]) -> str:
    """快速BOM检查 (仅风险)"""
    analyzer = BOMAnalyzer()
    analysis = analyzer.analyze_bom(bom)
    
    if analysis.high_risk_count > 0:
        return f"⚠️ 发现 {analysis.high_risk_count} 个高风险器件!"
    
    if analysis.cad_missing_count > 0:
        return f"🔌 {analysis.cad_missing_count} 个器件缺少 CAD 资源"
    
    return "✅ BOM 状态良好"
