"""
🚀 发布脚本 - 一键打包并发布

使用方法:
  python scripts/release.py build
  python scripts/release.py github 0.2.0
"""
import os
import sys
import subprocess
import shutil

VERSION = "0.2.0"


def run(cmd):
    """运行命令"""
    print(f"🔧 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ {result.stderr}")
        sys.exit(1)
    return result


def build():
    """构建"""
    print("="*50)
    print("🚀 构建发布包")
    print("="*50)
    
    run("pip install build twine -q")
    run("pip install -e . -q")
    run("python -m build")
    
    print("\n✅ 构建完成!")
    for f in os.listdir("dist"):
        print(f"  📦 {f}")


def github(tag):
    """创建 Release"""
    print("="*50)
    print(f"🏷️ GitHub Release v{tag}")
    print("="*50)
    
    print("\n📝 请访问:")
    print(f"https://github.com/KINGSTON-115/OpenPartSelector/releases/new?tag={tag}")
    print("\n📦 下载文件:")
    if os.path.exists("dist"):
        for f in os.listdir("dist"):
            print(f"  - {f}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if cmd == "build":
        build()
    elif cmd == "github" and len(sys.argv) > 2:
        github(sys.argv[2])
    else:
        print("用法: python scripts/release.py build | github 0.2.0")
