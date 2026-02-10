# OpenPartSelector Makefile
# =========================

.PHONY: help install test lint clean build run dev check

# 默认目标
help:
	@echo "OpenPartSelector 开发命令"
	@echo ""
	@echo "可用命令:"
	@echo "  install     - 安装依赖 (pip install -e .)"
	@echo "  test        - 运行测试 (pytest)"
	@echo "  test:cov    - 运行测试并生成覆盖率报告"
	@echo "  lint        - 代码检查 (flake8, black, isort)"
	@echo "  lint:fix    - 自动修复代码格式"
	@echo "  clean       - 清理临时文件"
	@echo "  build       - 构建可执行文件"
	@echo "  run         - 运行桌面应用"
	@echo "  run:web     - 运行 Web 应用"
	@echo "  run:api     - 运行 API 服务器"
	@echo "  dev         - 开发模式运行"
	@echo "  check       - 运行所有检查"

# 安装依赖
install:
	pip install -e .

# 运行测试
test:
	python -m pytest tests/ -v

# 测试覆盖率
test:cov:
	python -m pytest tests/ --cov=ops --cov-report=html
	@echo "覆盖率报告: htmlcov/index.html"

# 代码检查
lint:
	@echo "Running flake8..."
	flake8 ops/ --max-line-length=100 --ignore=E501,W503
	@echo "Running black check..."
	black --check ops/
	@echo "Running isort check..."
	isort --check-only ops/

# 自动修复代码格式
lint:fix:
	black ops/
	isort ops/

# 清理
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".pytest_cache" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info .eggs/ 2>/dev/null || true
	@echo "清理完成"

# 构建可执行文件
build:
	python build_exe.py

# 运行桌面应用
run:
	python desktop_app.py

# 运行 Web 应用
run:web:
	python web_app.py

# 运行 API 服务器
run:api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 开发模式
dev:
	@echo "启动开发服务器..."
	@echo "1. 运行桌面应用: make run"
	@echo "2. 运行 API: make run:api"
	@echo "3. 运行测试: make test"

# 完整检查
check: lint test
	@echo "所有检查通过"

# 数据库相关
db:init:
	python -c "from ops.database import init_database; init_database()"

db:search:
	python -c "from ops.database import search_components; print(search_components('STM32'))"

# 发布到 PyPI
pypi: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*
