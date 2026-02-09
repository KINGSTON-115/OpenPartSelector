#!/usr/bin/env python3
"""
🚀 OpenPartSelector v0.2.0 便携版
双击运行，无需安装！

使用方法:
  1. 安装 Python 3.10+
  2. 双击此脚本 或 python run.py

或者直接在命令行运行:
  python run.py
"""
import sys
import os

# 检查 Python 版本
if sys.version_info < (3, 10):
    print("❌ 错误: 需要 Python 3.10 或更高版本")
    print(f"   当前版本: {sys.version}")
    print("\n💡 请安装新版本:")
    print("   - Windows: https://www.python.org/downloads/")
    print("   - Mac: brew install python")
    print("   - Linux: sudo apt install python3.11")
    input("\n按回车退出...")
    sys.exit(1)

# 检查依赖
def check_dependencies():
    """检查并安装依赖"""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter")
    
    try:
        import openai
    except ImportError:
        missing.append("openai")
    
    try:
        import aiohttp
    except ImportError:
        missing.append("aiohttp")
    
    if missing:
        print(f"⚠️ 缺少依赖: {', '.join(missing)}")
        print("\n🔧 自动安装...")
        
        cmd = [sys.executable, "-m", "pip", "install", "-q"] + missing
        result = os.system(" ".join(cmd))
        
        if result == 0:
            print("✅ 安装成功!")
        else:
            print("❌ 安装失败，请手动安装:")
            print(f"   pip install {' '.join(missing)}")
            input("\n按回车退出...")
            sys.exit(1)


def main():
    """主函数"""
    print("="*60)
    print("🤖 OpenPartSelector v0.2.0 便携版")
    print("="*60)
    print()
    
    # 检查依赖
    print("🔍 检查环境...")
    check_dependencies()
    
    # 导入并运行
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # 导入主应用
        from desktop_app import OpenPartSelectorApp
        
        print("✅ 环境检查通过!")
        print()
        print("📖 使用说明:")
        print("   1. 在搜索框输入需求")
        print("      例如: '找一个 3.3V LDO'")
        print("   2. 点击 '开始选型'")
        print("   3. 查看推荐结果")
        print()
        print("💡 提示: 支持中英文!")
        print()
        input("按回车启动程序...")
        
        # 启动 GUI
        root = tk.Tk()
        root.title("🤖 OpenPartSelector v0.2.0")
        root.geometry("900x700")
        
        app = OpenPartSelectorApp(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("\n💡 解决方案:")
        print("   pip install openai aiohttp")
        input("\n按回车退出...")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("\n按回车退出...")


if __name__ == "__main__":
    main()
