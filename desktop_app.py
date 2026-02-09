"""
🎯 OpenPartSelector Windows 桌面应用
双击开箱即用，无需安装 Python！
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class OpenPartSelectorApp:
    """OpenPartSelector 桌面应用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 OpenPartSelector - AI电子元器件智能选型")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 初始化 Agent
        self.agent = None
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Microsoft YaHei', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Microsoft YaHei', 10))
        style.configure('Result.TLabel', font=('Microsoft YaHei', 9))
        style.configure('Action.TButton', font=('Microsoft YaHei', 10, 'bold'))
        
    def create_widgets(self):
        """创建界面组件"""
        
        # ===== 标题区 =====
        title_frame = ttk.Frame(self.root, padding=10)
        title_frame.pack(fill='x')
        
        ttk.Label(title_frame, text="🤖 OpenPartSelector", 
                 style='Title.TLabel').pack(side='left')
        
        ttk.Label(title_frame, 
                 text="AI电子元器件智能选型引擎 | 双击即用",
                 style='Subtitle.TLabel').pack(side='right')
        
        # 分隔线
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=10)
        
        # ===== 搜索区 =====
        search_frame = ttk.Frame(self.root, padding=15)
        search_frame.pack(fill='x')
        
        ttk.Label(search_frame, text="🔍 选型查询:", 
                 font=('Microsoft YaHei', 11, 'bold')).pack(anchor='w')
        
        # 搜索框
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, 
                                     textvariable=self.search_var,
                                     font=('Microsoft YaHei', 12),
                                     width=50)
        self.search_entry.pack(fill='x', pady=8)
        self.search_entry.bind('<Return>', lambda e: self.start_search())
        
        # 搜索按钮
        btn_frame = ttk.Frame(search_frame)
        btn_frame.pack(fill='x', pady=5)
        
        search_btn = ttk.Button(btn_frame, text="🚀 开始选型", 
                               command=self.start_search,
                               style='Action.TButton')
        search_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = ttk.Button(btn_frame, text="🗑️ 清空", 
                              command=self.clear_results)
        clear_btn.pack(side='left')
        
        # 示例按钮
        examples = ["找一个 3.3V LDO", "ESP32 WiFi 模块", "STM32 单片机", 
                   "CH340 USB转串口", "国产替代推荐"]
        for ex in examples:
            btn = ttk.Button(btn_frame, text=ex, 
                           command=lambda x=ex: self.search_var.set(x) or self.start_search())
            btn.pack(side='left', padx=3)
        
        # ===== 标签页 =====
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 选型结果页
        self.results_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.results_frame, text="📦 选型结果")
        self.create_results_area()
        
        # 国产替代页
        self.alternatives_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.alternatives_frame, text="🇨🇳 国产替代")
        self.create_alternatives_area()
        
        # 参考电路页
        self.circuits_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.circuits_frame, text="📚 参考电路")
        self.create_circuits_area()
        
        # 电路计算页
        self.calc_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.calc_frame, text="🧮 电路计算")
        self.create_calc_area()
        
        # ===== 状态栏 =====
        self.status_var = tk.StringVar()
        self.status_var.set("✅ 准备就绪 | 输入需求开始选型...")
        status_bar = ttk.Label(self.root, textvariable=self.status_var,
                              relief='sunken', anchor='w', padding=(5, 3))
        status_bar.pack(fill='x', side='bottom')
    
    def create_results_area(self):
        """创建选型结果区域"""
        # 结果列表
        self.results_text = scrolledtext.ScrolledText(
            self.results_frame, font=('Consolas', 10), wrap='word'
        )
        self.results_text.pack(fill='both', expand=True)
        
        # 默认提示
        self.results_text.insert('end', 
            "📋 使用说明:\n\n"
            "1. 在上方搜索框输入需求\n"
            "   例如: '找一个 3.3V LDO 1A' 或 'ESP32 WiFi 模块'\n\n"
            "2. 点击 '🚀 开始选型'\n\n"
            "3. 查看推荐结果和价格对比\n\n"
            "💡 提示: 点击下方示例按钮快速体验"
        )
    
    def create_alternatives_area(self):
        """创建国产替代区域"""
        # 输入
        input_frame = ttk.Frame(self.alternatives_frame)
        input_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(input_frame, text="输入原器件型号:").pack(side='left')
        self.alt_var = tk.StringVar()
        alt_entry = ttk.Entry(input_frame, textvariable=self.alt_var, width=30)
        alt_entry.pack(side='left', padx=10)
        alt_entry.bind('<Return>', lambda e: self.search_alternatives())
        
        ttk.Button(input_frame, text="🔍 查找替代", 
                  command=self.search_alternatives).pack(side='left')
        
        # 结果
        self.alternatives_text = scrolledtext.ScrolledText(
            self.alternatives_frame, font=('Consolas', 10), wrap='word'
        )
        self.alternatives_text.pack(fill='both', expand=True)
        
        self.alternatives_text.insert('end', 
            "🇨🇳 国产替代推荐\n\n"
            "输入原器件型号(如 STM32F103C8T6)，一键查找国产替代方案:\n\n"
            "• STM32 → GD32F103 (兆易创新)\n"
            "• ESP32 → ESP32-C3 (乐鑫)\n"
            "• CH340 → CH340N (沁恒)\n"
            "• AMS1117 → ME6211 (微盟)\n"
            "• LM358 → SGM358 (圣邦微)"
        )
    
    def create_circuits_area(self):
        """创建参考电路区域"""
        # 选择框
        sel_frame = ttk.Frame(self.circuits_frame)
        sel_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(sel_frame, text="选择电路模板:").pack(side='left')
        
        circuits = ["ESP32 最小系统", "STM32 最小系统", "LDO 稳压电源",
                   "ESP32 下载器", "蓝牙串口", "MQ气体传感器"]
        self.circuit_var = tk.StringVar()
        circuit_combo = ttk.Combobox(sel_frame, textvariable=self.circuit_var,
                                     values=circuits, state='readonly', width=20)
        circuit_combo.pack(side='left', padx=10)
        circuit_combo.current(0)
        
        ttk.Button(sel_frame, text="📖 查看详情", 
                  command=self.show_circuit).pack(side='left', padx=10)
        
        # 结果
        self.circuits_text = scrolledtext.ScrolledText(
            self.circuits_frame, font=('Consolas', 10), wrap='word'
        )
        self.circuits_text.pack(fill='both', expand=True)
        
        self.show_circuit()
    
    def create_calc_area(self):
        """创建电路计算区域"""
        # 计算器选择
        calc_sel = ttk.Frame(self.calc_frame)
        calc_sel.pack(fill='x', pady=(0, 10))
        
        ttk.Label(calc_sel, text="选择计算器:").pack(side='left')
        
        calcs = ["LED限流电阻", "分压电阻"]
        self.calc_var = tk.StringVar()
        calc_combo = ttk.Combobox(calc_sel, textvariable=self.calc_var,
                                  values=calcs, state='readonly', width=15)
        calc_combo.pack(side='left', padx=10)
        calc_combo.current(0)
        calc_combo.bind('<<ComboboxSelected>>', self.change_calc)
        
        # 计算器输入区
        self.calc_input_frame = ttk.Frame(self.calc_frame)
        self.calc_input_frame.pack(fill='x', pady=10)
        
        self.create_led_calculator()
        
        # 结果区
        self.calc_result_frame = ttk.Frame(self.calc_frame)
        self.calc_result_frame.pack(fill='x', pady=10)
        
        self.calc_result = tk.StringVar()
        self.calc_result.set("💡 输入参数后自动计算")
        ttk.Label(self.calc_result_frame, textvariable=self.calc_result,
                 font=('Microsoft YaHei', 12, 'bold'), foreground='blue').pack()
    
    def create_led_calculator(self):
        """创建 LED 电阻计算器"""
        # 清除旧组件
        for widget in self.calc_input_frame.winfo_children():
            widget.destroy()
        
        # 输入
        row1 = ttk.Frame(self.calc_input_frame)
        row1.pack(fill='x', pady=3)
        ttk.Label(row1, text="输入电压 (V):", width=12).pack(side='left')
        self.v_in = ttk.Entry(row1, width=10)
        self.v_in.insert(0, "5.0")
        self.v_in.pack(side='left')
        
        row2 = ttk.Frame(self.calc_input_frame)
        row2.pack(fill='x', pady=3)
        ttk.Label(row2, text="LED压降 (V):", width=12).pack(side='left')
        self.v_led = ttk.Entry(row2, width=10)
        self.v_led.insert(0, "2.0")
        self.v_led.pack(side='left')
        
        row3 = ttk.Frame(self.calc_input_frame)
        row3.pack(fill='x', pady=3)
        ttk.Label(row3, text="LED电流 (mA):", width=12).pack(side='left')
        self.i_led = ttk.Entry(row3, width=10)
        self.i_led.insert(0, "20")
        self.i_led.pack(side='left')
        
        ttk.Button(self.calc_input_frame, text="🧮 计算", 
                  command=self.calc_led).pack(pady=10)
    
    def create_voltage_divider(self):
        """创建分压电阻计算器"""
        for widget in self.calc_input_frame.winfo_children():
            widget.destroy()
        
        row1 = ttk.Frame(self.calc_input_frame)
        row1.pack(fill='x', pady=3)
        ttk.Label(row1, text="输入电压 (V):", width=12).pack(side='left')
        self.div_vin = ttk.Entry(row1, width=10)
        self.div_vin.insert(0, "5.0")
        self.div_vin.pack(side='left')
        
        row2 = ttk.Frame(self.calc_input_frame)
        row2.pack(fill='x', pady=3)
        ttk.Label(row2, text="输出电压 (V):", width=12).pack(side='left')
        self.div_vout = ttk.Entry(row2, width=10)
        self.div_vout.insert(0, "3.3")
        self.div_vout.pack(side='left')
        
        ttk.Button(self.calc_input_frame, text="🧮 计算", 
                  command=self.calc_divider).pack(pady=10)
    
    def change_calc(self, event=None):
        """切换计算器"""
        if self.calc_var.get() == "LED限流电阻":
            self.create_led_calculator()
        else:
            self.create_voltage_divider()
    
    def calc_led(self):
        """计算 LED 限流电阻"""
        try:
            v_in = float(self.v_in.get())
            v_led = float(self.v_led.get())
            i_led = float(self.i_led.get()) / 1000.0
            
            v_r = v_in - v_led
            if v_r <= 0:
                self.calc_result.set("❌ 输入电压必须大于LED压降!")
                return
            
            r = v_r / i_led
            # 标准电阻值
            e24 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 51, 68, 82, 100, 120, 150, 180, 220, 270, 330, 390, 470, 510, 680, 820, 1000]
            r_std = min(e24, key=lambda x: abs(x - r))
            
            power = v_r * i_led * 1000  # mW
            
            self.calc_result.set(
                f"✅ 推荐电阻: {r_std}Ω\n"
                f"功率: {power:.1f}mW (建议用1/4W电阻)"
            )
        except Exception as e:
            self.calc_result.set(f"❌ 错误: {e}")
    
    def calc_divider(self):
        """计算分压电阻"""
        try:
            v_in = float(self.div_vin.get())
            v_out = float(self.div_vout.get())
            
            if v_out >= v_in:
                self.calc_result.set("❌ 输出电压必须小于输入电压!")
                return
            
            # 假设R2=10K
            r2 = 10000
            r1 = r2 * (v_in / v_out - 1)
            
            # 标准值
            e24 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 51, 68, 82, 100, 120, 150, 180, 220, 270, 330, 390, 470, 510, 680, 820, 1000]
            r1_std = min(e24, key=lambda x: abs(x/1000 - r1))
            r2_std = min(e24, key=lambda x: abs(x - r2))
            
            actual = v_in * r2_std / (r1_std * 1000 + r2_std)
            
            self.calc_result.set(
                f"✅ 推荐: R1={r1_std}KΩ, R2={r2_std}KΩ\n"
                f"实际输出: {actual:.2f}V (目标: {v_out}V)"
            )
        except Exception as e:
            self.calc_result.set(f"❌ 错误: {e}")
    
    def show_circuit(self):
        """显示参考电路"""
        from ops.features import get_circuit_template
        
        circuit_map = {
            "ESP32 最小系统": "esp32_minimal",
            "STM32 最小系统": "stm32_minimal", 
            "LDO 稳压电源": "ldo_power",
            "ESP32 下载器": "esp32_downloader",
            "蓝牙串口": "bluetooth_uart",
            "MQ气体传感器": "mq_sensors"
        }
        
        key = circuit_map.get(self.circuit_var.get(), "esp32_minimal")
        tmpl = get_circuit_template(key)
        
        if tmpl:
            text = f"""
📚 {tmpl['name']}
{'='*40}

{tmpl['description']}

⏱️ 难度: {tmpl['difficulty']}
💰 BOM成本: ¥{tmpl.get('jlc_bom_cost', 'N/A')}

📋 BOM清单:
"""
            for item in tmpl.get('器件列表', []):
                text += f"  • {item['desc']}: {item['value']} x {item.get('part', item.get('type', ''))}\n"
            
            text += "\n⚠️ 注意事项:\n"
            for note in tmpl.get('注意事项', []):
                text += f"  • {note}\n"
            
            self.circuits_text.delete('1.0', 'end')
            self.circuits_text.insert('end', text)
    
    # ===== 功能方法 =====
    
    def start_search(self):
        """开始搜索"""
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("提示", "请输入搜索内容")
            return
        
        # 禁用按钮
        self.status_var.set("🔄 正在搜索...")
        self.root.update()
        
        # 在后台线程执行
        def do_search():
            try:
                from ops.agent import Agent
                agent = Agent()
                results = asyncio.run(agent.select(query, top_k=5))
                
                # 在主线程更新界面
                self.root.after(0, lambda: self.show_results(query, results))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(str(e)))
        
        threading.Thread(target=do_search, daemon=True).start()
    
    def show_results(self, query, results):
        """显示搜索结果"""
        self.notebook.select(0)  # 切换到结果页
        
        text = f"""
🔍 查询: {query}
{'='*60}

📦 推荐元器件 ({len(results.recommended_parts)} 个)

"""
        
        for i, r in enumerate(results.recommended_parts, 1):
            price = f"¥{r.price:.2f}" if r.price else "暂无报价"
            stock = f"{r.stock:,}" if r.stock else "未知"
            
            text += f"""
{i}. 📦 {r.part_number}
   厂商: {r.manufacturer}
   描述: {r.description}
   规格: {r.specs.voltage or 'N/A'} | {r.specs.current or 'N/A'} | {r.specs.package or 'N/A'}
   💰 价格: {price} | 📦 库存: {stock} | 🎯 匹配度: {r.compatibility_score:.0%}
"""
            
            if r.alternatives:
                text += f"   🇨🇳 替代料: {', '.join(r.alternatives[:3])}\n"
            
            text += "-"*60 + "\n"
        
        if not results.recommended_parts:
            text += "❌ 未找到匹配结果，请尝试其他关键词\n"
        
        text += f"\n⏰ 生成时间: {results.generated_at[:19]}\n"
        
        self.results_text.delete('1.0', 'end')
        self.results_text.insert('end', text)
        self.status_var.set(f"✅ 找到 {len(results.recommended_parts)} 个推荐")
    
    def show_error(self, msg):
        """显示错误"""
        self.status_var.set("❌ 搜索失败")
        messagebox.showerror("错误", f"搜索失败: {msg}")
    
    def clear_results(self):
        """清空结果"""
        self.results_text.delete('1.0', 'end')
        self.search_var.set("")
        self.status_var.set("✅ 已清空 | 准备就绪")
    
    def search_alternatives(self):
        """搜索国产替代"""
        part = self.alt_var.get().strip()
        if not part:
            messagebox.showwarning("提示", "请输入器件型号")
            return
        
        from ops.features import find_alternatives
        
        alts = find_alternatives(part)
        
        text = f"🇨🇳 {part} 的国产替代方案\n{'='*50}\n\n"
        
        if alts:
            for i, a in enumerate(alts, 1):
                text += f"{i}. 🇨🇳 {a['brand']} {a['model']}\n"
                text += f"   💰 价格比: {a['price_ratio']*100:.0f}%\n"
                text += f"   🔗 兼容性: {a['compatibility']}\n"
                text += f"   📝 {a['notes']}\n\n"
        else:
            text += "❌ 未找到国产替代方案\n"
            text += "\n💡 提示: 可尝试搜索以下关键词:\n"
            text += "   STM32, ESP32, CH340, AMS1117, LM358"
        
        self.alternatives_text.delete('1.0', 'end')
        self.alternatives_text.insert('end', text)


def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置图标 (如果有)
    try:
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    app = OpenPartSelectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
