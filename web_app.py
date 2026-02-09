"""
🌐 多语言 Web 界面 - Streamlit 应用
"""
import streamlit as st
import asyncio
from typing import Dict, Any

# 页面配置
st.set_page_config(
    page_title="OpenPartSelector",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入模块
import sys
sys.path.insert(0, '.')

from ops.agent import Agent
from ops.jlc import search_jlc, calculate_jlc_smt, get_jlc_footprint
from ops.features import find_alternatives, get_circuit_template, get_datasheet_summary
from ops.features import calculate_resistor_for_led, calculate_voltage_divider
from ops.i18n import get_text, get_platform_info, get_package_info


# ==================== 界面文本 ====================

UI_CN = {
    "title": "🤖 OpenPartSelector - AI电子元器件智能选型引擎",
    "subtitle": "为中国电子工程师和学生打造的智能选型工具",
    "search_placeholder": "输入需求，如：找一个 3.3V LDO 1A",
    "search_button": "🔍 开始选型",
    "features": ["🔧 智能选型", "🏭 立创集成", "📖 中文解读", "🧮 电路计算"],
    "results_title": "📦 推荐元器件",
    "alternatives_title": "🇨🇳 国产替代",
    "circuits_title": "📚 参考电路",
    "calculators_title": "🧮 电路计算器",
}

UI_EN = {
    "title": "🤖 OpenPartSelector - AI Component Selection Engine",
    "subtitle": "Intelligent selection tool for electronics engineers and students worldwide",
    "search_placeholder": "Enter your request, e.g., 'Find a 3.3V LDO 1A'",
    "search_button": "🔍 Start Selection",
    "features": ["🔧 Smart Selection", "🏭 Global Sourcing", "📖 Datasheet Guide", "🧮 Circuit Tools"],
    "results_title": "📦 Recommended Components",
    "alternatives_title": "🌍 Global Alternatives",
    "circuits_title": "📚 Reference Circuits",
    "calculators_title": "🧮 Circuit Calculators",
}


# ==================== 侧边栏 ====================

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("⚙️ 设置")
        
        # 语言选择
        lang = st.selectbox("🌐 Language / 语言", ["中文", "English"])
        
        # 搜索平台选择
        st.subheader("🔌 搜索平台")
        platforms = st.multiselect(
            "选择搜索平台" if lang == "中文" else "Select platforms",
            ["立创 (LCSC)", "DigiKey", "Mouser", "Octopart"],
            default=["立创 (LCSC)"]
        )
        
        # 筛选条件
        st.subheader("📊 筛选条件")
        category = st.selectbox(
            "器件类别" if lang == "中文" else "Category",
            ["全部", "电源管理", "MCU", "传感器", "接口芯片", "模拟电路", "分立器件"]
        )
        
        # 价格范围
        price_range = st.slider(
            "价格范围 (CNY)" if lang == "中文" else "Price Range (CNY)",
            0, 100, (0, 50)
        )
        
        return {
            "lang": lang,
            "platforms": platforms,
            "category": category,
            "price_range": price_range
        }


# ==================== 主界面 ====================

def render_main(settings: Dict):
    """渲染主界面"""
    ui = UI_CN if settings["lang"] == "中文" else UI_EN
    
    # 标题
    st.title(ui["title"])
    st.markdown(f"*{ui['subtitle']}*")
    
    # 搜索框
    query = st.text_input(
        ui["search_placeholder"],
        key="search_input"
    )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button(ui["search_button"], on_click=handle_search, args=(query, settings))
    
    # 显示功能标签
    st.markdown("---")
    st.write(" | ".join(ui["features"]))
    st.markdown("---")
    
    # 如果有查询结果
    if st.session_state.get("results"):
        render_results(st.session_state["results"], ui, settings)
    
    # 其他功能区域
    render_features(settings)


def handle_search(query: str, settings: Dict):
    """处理搜索请求"""
    if not query:
        return
    
    # 创建 Agent 并搜索
    agent = Agent()
    results = asyncio.run(agent.select(query, top_k=5))
    
    st.session_state["results"] = results
    st.session_state["last_query"] = query


def render_results(results, ui: Dict, settings: Dict):
    """渲染搜索结果"""
    st.subheader(ui["results_title"])
    
    for i, r in enumerate(results.recommended_parts):
        with st.expander(f"{i+1}. 📦 {r.part_number} - {r.manufacturer}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**描述:** {r.description}")
                st.write(f"📌 **规格:** {r.specs.voltage or 'N/A'} | {r.specs.current or 'N/A'} | {r.specs.package or 'N/A'}")
                
                # 价格和库存
                if r.price:
                    st.write(f"💰 **价格:** ¥{r.price:.2f}")
                if r.stock:
                    st.write(f"📦 **库存:** {r.stock:,}件")
                
                st.write(f"🎯 **匹配度:** {r.compatibility_score:.0%}")
            
            with col2:
                # 立创链接
                if settings["lang"] == "中文":
                    jlc_results = search_jlc(r.part_number)
                    if jlc_results:
                        st.markdown(f"[📦 立创商城]({jlc_results[0]['jlc_link']})")
                
                # 国产替代
                alts = find_alternatives(r.part_number)
                if alts:
                    with st.popover(ui["alternatives_title"]):
                        for a in alts[:3]:
                            st.write(f"🇨🇳 {a['brand']} {a['model']}")
                            st.write(f"   💰 {a['price_ratio']*100:.0f}% | 🔗 {a['compatibility']}")


def render_features(settings: Dict):
    """渲染其他功能"""
    tab1, tab2, tab3, tab4 = st.tabs(["📚 参考电路", "🧮 电路计算", "🌐 国际平台", "📖 学习路径"])
    
    with tab1:
        render_circuits(settings)
    
    with tab2:
        render_calculators(settings)
    
    with tab3:
        render_platforms(settings)
    
    with tab4:
        render_learning_path(settings)


def render_circuits(settings: Dict):
    """渲染参考电路"""
    ui = UI_CN if settings["lang"] == "中文" else UI_EN
    
    circuits = ["ESP32最小系统", "STM32最小系统", "LDO稳压电源"]
    selected = st.selectbox("选择电路模板" if settings["lang"] == "中文" else "Select circuit", circuits)
    
    tmpl = get_circuit_template(selected.lower().replace(" ", "_"))
    if tmpl:
        st.write(f"**{tmpl['name']}** ({tmpl['difficulty']})")
        st.write(tmpl['description'])
        
        if 'jlc_bom_cost' in tmpl:
            st.write(f"💰 BOM成本: ¥{tmpl['jlc_bom_cost']}")
        
        with st.expander("📋 BOM清单"):
            for item in tmpl.get('器件列表', []):
                st.write(f"- {item['desc']}: {item['value']} x {item.get('part', item.get('type', ''))}")


def render_calculators(settings: Dict):
    """渲染电路计算器"""
    tool = st.selectbox(
        "选择计算器" if settings["lang"] == "中文" else "Select tool",
        ["LED限流电阻", "分压电阻"]
    )
    
    if tool == "LED限流电阻":
        v_in = st.number_input("输入电压 (V)", 3.3, 24.0, 5.0)
        v_led = st.number_input("LED压降 (V)", 1.8, 3.6, 2.0)
        i_led = st.number_input("LED电流 (mA)", 1, 50, 20) / 1000.0
        
        result = calculate_resistor_for_led(v_in, v_led, i_led)
        
        st.success(f"推荐电阻: {result['recommended_resistance']}")
        st.write(f"功率: {result['power_dissipation']}")
    
    elif tool == "分压电阻":
        v_in = st.number_input("输入电压 (V)", 3.3, 24.0, 5.0)
        v_out = st.number_input("输出电压 (V)", 1.0, 12.0, 3.3)
        
        result = calculate_voltage_divider(v_in, v_out)
        
        st.success(f"推荐: R1={result['recommended_r1']}, R2={result['recommended_r2']}")
        st.write(f"实际输出: {result['actual_output']}V")


def render_platforms(settings: Dict):
    """渲染国际采购平台"""
    platforms = ["digikey", "mouser", "octopart", "arrow"]
    
    for p in platforms:
        info = get_platform_info(p)
        if info:
            with st.expander(f"🔗 {info['name']} ({info['region']})"):
                st.write(f"**特点:** {', '.join(info['strengths'])}")
                st.write(f"[访问官网]({info['url']})")


def render_learning_path(settings: Dict):
    """渲染学习路径"""
    from ops.i18n import LEARNING_PATHS
    
    level = st.selectbox(
        "选择水平" if settings["lang"] == "中文" else "Select level",
        ["beginner", "intermediate", "advanced"]
    )
    
    path = LEARNING_PATHS.get(level, {})
    if path:
        st.write(f"## {path.get('name', '')} ({path.get('duration', '')})")
        
        for course in path.get('courses', []):
            st.subheader(course['title'])
            st.write(f"📖 {course['title']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**项目:**")
                for p in course['projects'][:2]:
                    st.write(f"- {p}")
            with col2:
                st.write("**推荐器件:**")
                for c in course['recommended_components'][:3]:
                    st.write(f"- {c}")


# ==================== 主函数 ====================

def main():
    """主函数"""
    settings = render_sidebar()
    render_main(settings)


if __name__ == "__main__":
    main()
