@echo off
REM ======================================================
REM OpenPartSelector Windows EXE 构建脚本
REM 使用方法:
REM   1. 安装 Python 3.10+: https://python.org/downloads
REM   2. 下载此脚本和 desktop_app.py
REM   3. 双击运行此脚本
REM ======================================================

echo.
echo ═══════════════════════════════════════════════════════
echo   OpenPartSelector EXE 构建脚本
echo ═══════════════════════════════════════════════════════
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo.
    echo 请先安装 Python 3.10 或更高版本:
    echo   访问: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python 已安装

REM 安装依赖
echo.
echo 📦 安装依赖...
pip install -q openai aiohttp httpx pyyaml pydantic loguru pyinstaller
if errorlevel 1 (
    echo ❌ 安装失败，请手动运行:
    echo   pip install openai aiohttp httpx pyyaml pydantic loguru pyinstaller
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

REM 构建 EXE
echo.
echo 🔨 正在构建 EXE...
echo    这可能需要几分钟...

python -m PyInstaller --onefile --windowed --name "OpenPartSelector" --clean desktop_app.py

if exist "dist\OpenPartSelector.exe" (
    echo.
    echo ═══════════════════════════════════════════════════════
    echo ✅ 构建成功!
    echo ═══════════════════════════════════════════════════════
    echo.
    echo 📁 EXE 文件位置:
    echo    %cd%\dist\OpenPartSelector.exe
    echo.
    echo 📦 文件大小:
    for %%I in (dist\OpenPartSelector.exe) do echo    %~zI 字节
    echo.
    echo 💡 提示: 可以将 dist\OpenPartSelector.exe 复制到任何 Windows 机器上运行!
    echo.
) else (
    echo.
    echo ❌ 构建失败，请检查错误信息
)

echo.
pause
