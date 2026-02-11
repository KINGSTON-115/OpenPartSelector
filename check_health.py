#!/usr/bin/env python3
"""
OpenPartSelector 版本一致性检查
v1.1.35
"""
import os
import re
import sys

def find_version_files(root="."):
    """查找所有包含版本号的文件（排除依赖版本）"""
    version_pattern = r"(\d+\.\d+\.\d+)"
    exclude_dirs = {"node_modules", ".git", "__pycache__", ".pytest_cache", "build", "dist"}
    exclude_files = {"package-lock.json", "requirements.txt", "backend/requirements.txt"}
    
    files = []
    
    for ext in ["*.py", "*.md", "*.html", "*.json", "*.yml", "*.txt"]:
        for path in os.walk(root):
            if any(exc in path[0] for exc in exclude_dirs):
                continue
            for file in path[2]:
                if file in exclude_files:
                    continue
                full_path = os.path.join(path[0], file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # 排除 requirements.txt 中的版本号
                        if "requirements" in file.lower():
                            continue
                        matches = re.findall(version_pattern, content)
                        if matches:
                            # 过滤掉明显的依赖版本
                            filtered = {v for v in matches if not v.startswith(('0.', '1.0.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or v == "1.1.34"}
                            if filtered:
                                files.append((full_path, filtered))
                except:
                    pass
    return files

def check_version_consistency(expected="1.1.35"):
    """检查版本一致性（只检查关键版本标记）"""
    print(f"🔍 检查版本一致性 (期望版本: {expected})")
    print("-" * 50)
    
    # 只检查关键文件中的主版本号
    key_files = {
        "package.json": f'"version": "{expected}"',
        "setup.py": f'version="{expected}"',
        "frontend/index.html": f'v{expected}',
        "standalone.html": f'v{expected}',
    }
    
    inconsistencies = []
    
    for file_rel, pattern in key_files.items():
        file_path = os.path.join(os.path.dirname(__file__), file_rel)
        if not os.path.exists(file_path):
            file_path = os.path.join(".", file_rel)
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if pattern not in content:
                    inconsistencies.append((file_rel, f"未找到 '{pattern}'"))
    
    if inconsistencies:
        print(f"❌ 发现 {len(inconsistencies)} 个版本不一致:")
        for path, msg in inconsistencies:
            print(f"   {path}: {msg}")
        return False
    else:
        print(f"✅ 所有关键文件版本一致: {expected}")
        return True

def count_tests():
    """统计测试用例数量"""
    test_dir = "tests"
    count = 0
    
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                    # 统计 pytest 函数
                    count += content.count("def test_")
                    count += content.count("async def test_")
    
    print(f"📊 测试用例统计: {count} 个")
    return count

def check_dependencies():
    """检查依赖配置"""
    print("\n📦 依赖检查:")
    
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        with open(req_file, "r") as f:
            content = f.read()
            # 检查是否有版本限制
            if "<" in content and ">" in content:
                print("   ✅ 依赖版本已锁定 (使用 < 和 >)")
            else:
                print("   ⚠️  建议添加版本范围限制")
    
    setup_file = "setup.py"
    if os.path.exists(setup_file):
        with open(setup_file, "r") as f:
            content = f.read()
            if 'version="1.1.35"' in content:
                print("   ✅ setup.py 版本一致")
            else:
                print("   ⚠️  setup.py 版本可能不一致")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 OpenPartSelector v1.1.35 持续改进检查")
    print("=" * 50)
    
    success = check_version_consistency()
    count_tests()
    check_dependencies()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 项目健康检查通过!")
    else:
        print("❌ 发现问题，请修复")
        sys.exit(1)
