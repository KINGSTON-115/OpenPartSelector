"""
Pytest configuration for OpenPartSelector
"""
import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置 pytest-asyncio
pytest_plugins = ['pytest_asyncio']

# 异步测试配置
pytest_asyncio_mode = "auto"

