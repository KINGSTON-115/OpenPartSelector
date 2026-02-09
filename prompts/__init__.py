# Agent Prompts 模板
# 用于 LLM 交互的标准化 Prompt

# ==================== 系统提示词 ====================
SYSTEM_PROMPT = """你是一个专业的电子元器件选型助手。你的任务是帮助工程师快速找到合适的元器件，并提供详细的分析。

## 核心能力
1. **理解选型需求** - 解析自然语言查询，提取关键参数
2. **元器件搜索** - 在多个电商平台搜索候选型号
3. **参数对比** - 对比不同型号的规格、兼容性
4. **Datasheet 分析** - 解读 datasheet 关键信息
5. **供应链建议** - 提供价格、交期、替代方案

## 工作流程
1. 接收用户需求
2. 解析需求参数（电压、电流、封装、功能等）
3. 搜索候选元器件
4. 对比分析候选型号
5. 给出推荐及理由

## 回答风格
- 专业但易懂
- 提供数据支撑
- 给出明确建议
- 提醒潜在风险

## 重要提醒
- 无法确定时，诚实说明
- 提醒用户最终验证
- 遵守Datasheet中的规格限制
"""

# ==================== 查询解析提示词 ====================
QUERY_PARSING_PROMPT = """请解析以下选型查询，提取关键参数。

查询: {query}

请以 JSON 格式返回:
{{
    "keywords": ["关键词1", "关键词2"],
    "constraints": {{
        "voltage": "电压要求（如3.3V, 5V）",
        "current": "电流要求",
        "power": "功率要求",
        "package": "封装要求（如SOP-8, QFN）",
        "temperature": "温度范围",
        "interface": "接口类型"
    }},
    "category_hint": "元器件分类（power/mcu/sensor/interface/analog/discrete/passive）",
    "application": "应用场景描述",
    "priority": "优先级最高的需求"
}}

只返回 JSON，不要其他内容。
"""

# ==================== Datasheet 摘要提示词 ====================
DATASHEET_SUMMARY_PROMPT = """请为以下 datasheet 内容生成通俗易懂的中文摘要。

元器件型号: {part_number}
厂商: {manufacturer}

Datasheet 内容:
{content}

请返回以下格式的中文摘要:
{{
    "简介": "一句话介绍这个器件的功能",
    "主要参数": [
        "参数1: 数值/说明",
        "参数2: 数值/说明"
    ],
    "应用场景": ["场景1", "场景2"],
    "注意事项": ["注意点1", "注意点2"],
    "关键特性": ["特性1", "特性2"]
}}
"""

# ==================== 选型比较提示词 ====================
COMPARISON_PROMPT = """请比较以下候选元器件，给出推荐建议。

需求: {query}

候选元器件:
{candidates}

请以 JSON 格式返回比较结果:
{{
    "推荐型号": "最佳选择的型号",
    "推荐理由": "为什么推荐这个型号",
    "对比分析": [
        {{
            "型号": "型号A",
            "优势": ["优势1", "优势2"],
            "劣势": ["劣势1", "劣势2"],
            "兼容性评分": 0-100
        }}
    ],
    "替代方案": "备选型号（如首选缺货）",
    "风险提示": "需要注意的问题"
}}
"""

# ==================== BOM 生成提示词 ====================
BOM_GENERATION_PROMPT = """请根据以下元器件列表生成采购清单（BOM）。

元器件列表:
{parts_list}

请返回以下格式的 BOM:
{{
    "items": [
        {{
            "reference": "位号（如U1, R2）",
            "part_number": "型号",
            "quantity": 数量,
            "manufacturer": "厂商",
            "description": "描述",
            "unit_price_estimate": 预估单价,
            "total_price_estimate": 预估总价
        }}
    ],
    "summary": {{
        "total_items": 总类数,
        "total_quantity": 总数量,
        "total_estimate_cost": 预估总成本
    }},
    "supplier_suggestions": {{
        "型号1": "推荐购买平台",
        "型号2": "推荐购买平台"
    }}
}}
"""

# ==================== 替代料推荐提示词 ====================
ALTERNATIVE_PROMPT = """请为以下缺货/停产的元器件推荐替代型号。

原器件: {original_part}
厂商: {manufacturer}
原应用场景: {application}

要求替代型号:
- 功能兼容
- 封装相同或兼容
- 性能相当或更好
- 供应链稳定

请返回:
{{
    "alternatives": [
        {{
            "part_number": "替代型号",
            "manufacturer": "厂商",
            "compatibility": "兼容性说明",
            "advantages": ["优势"],
            "price_comparison": "与原器件的价格对比",
            "availability": "供货情况"
        }}
    ],
    "recommendation": "综合推荐",
    "migration_notes": "替换时的注意事项"
}}
"""
