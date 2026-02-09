"""
📦 Windows EXE 打包脚本
双击即用，无需安装 Python！
"""
import os
import sys
import subprocess

# PyInstaller 打包命令
BUILD_CMD = """
pyinstaller ^
    --name "OpenPartSelector" ^
    --onefile ^
    --windowed ^
    --icon "resources/icon.ico" ^
    --add-data "ops;ops" ^
    --add-data "data;data" ^
    --hidden-import "asyncio" ^
    --hidden-import "tkinter" ^
    --hidden-import "ttkthemes" ^
    --collect-all "ops" ^
    desktop_app.py
"""

def build_exe():
    """打包 EXE"""
    print("="*60)
    print("🎯 OpenPartSelector Windows EXE 打包")
    print("="*60)
    
    # 检查 PyInstaller
    try:
        subprocess.run(["pyinstaller", "--version"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 正在安装 PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"])
    
    # 创建资源目录
    os.makedirs("resources", exist_ok=True)
    
    # 下载图标 (可选)
    icon_url = "https://raw.githubusercontent.com/KINGSTON-115/OpenPartSelector/main/resources/icon.ico"
    
    # 执行打包
    print("\n🔨 开始打包...")
    result = subprocess.run(BUILD_CMD, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ 打包成功!")
        print(f"\n📦 EXE 文件位置: dist/OpenPartSelector.exe")
        print(f"📁 文件大小: {get_size('dist/OpenPartSelector.exe')}")
    else:
        print("\n❌ 打包失败!")
        print(result.stderr)
    
    return result.returncode == 0

def get_size(path):
    """获取文件大小"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        if size > 1024 * 1024:
            return f"{size / 1024 / 1024:.1f} MB"
        elif size > 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size} B"
    return "N/A"

def create_installer():
    """创建安装脚本"""
    install_script = r'''
@echo off
echo ============================================
echo   OpenPartSelector 安装程序
echo ============================================
echo.
echo 正在安装...
xcopy /E /I "dist\OpenPartSelector" "C:\Program Files\OpenPartSelector"
echo.
echo 创建快捷方式...
set "SOURCE=C:\Program Files\OpenPartSelector\OpenPartSelector.exe"
set "LINK=%USERPROFILE%\Desktop\OpenPartSelector.lnk"
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%LINK%');$s.TargetPath='%SOURCE%';$s.WorkingDirectory='C:\Program Files\OpenPartSelector';$s.Save()"
echo.
echo ✅ 安装完成!
echo.
echo 双击桌面图标开始使用!
pause
'''
    
    with open("install.bat", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    print("\n📝 安装脚本已创建: install.bat")

def create_readme():
    """创建用户说明"""
    readme = r'''
# OpenPartSelector Windows 版使用说明

## 🎯 快速开始

1. 双击 `OpenPartSelector.exe` 打开应用
2. 输入选型需求，如："找一个 3.3V LDO"
3. 点击 "🚀 开始选型"

## 📦 功能特性

- 🤖 AI 智能选型
- 🏭 嘉立创集成
- 🇨🇳 国产替代推荐
- 📚 参考电路模板
- 🧮 电路计算器
- 💰 多平台比价

## 📁 文件结构

```
OpenPartSelector/
├── OpenPartSelector.exe    # 主程序 (双击打开)
├── README.txt             # 本说明
└── docs/                  # 文档目录
    ├── i18n.md           # 多语言文档
    └── examples.md       # 使用示例
```

## 🆘 常见问题

Q: 提示缺少 DLL?
A: 请安装 Visual C++ Redistributable:
   https://aka.ms/vs/17/release/vc_redist.x64.exe

Q: 杀毒软件报警?
A: PyInstaller 打包可能被误报，请添加信任或从源码运行

## 📞 反馈

GitHub: https://github.com/KINGSTON-115/OpenPartSelector
邮件: zhenweisi@openclaw.ai

---
MIT License - 免费使用
'''
    
    with open("README_Windows.txt", "w", encoding="utf-8") as f:
        f.write(readme)
    
    print("\n📄 使用说明已创建: README_Windows.txt")

if __name__ == "__main__":
    # 创建资源文件
    os.makedirs("resources", exist_ok=True)
    
    # 打包 EXE
    if build_exe():
        # 创建辅助文件
        create_installer()
        create_readme()
        
        print("\n" + "="*60)
        print("✅ 打包完成!")
        print("="*60)
        print("\n📦 生成的文件:")
        print("  • dist/OpenPartSelector.exe  - 主程序")
        print("  • install.bat               - 安装脚本")
        print("  • README_Windows.txt        - 使用说明")
        print("\n🚀 双击 OpenPartSelector.exe 即可使用!")
    else:
        print("\n❌ 请检查错误信息")
