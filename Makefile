# Makefile for py_myt project

.PHONY: help install install-dev test test-cov lint format type-check clean build upload docs

# 默认目标
help:
	@echo "可用的命令:"
	@echo "  install      - 安装包"
	@echo "  install-dev  - 安装开发依赖"
	@echo "  test         - 运行测试"
	@echo "  test-cov     - 运行测试并生成覆盖率报告"
	@echo "  lint         - 代码风格检查"
	@echo "  format       - 代码格式化"
	@echo "  type-check   - 类型检查"
	@echo "  clean        - 清理构建文件"
	@echo "  build        - 构建包"
	@echo "  upload       - 上传到PyPI"
	@echo "  docs         - 生成文档"

# 安装包
install:
	pip install -e .

# 安装开发依赖
install-dev:
	pip install -e ".[dev]"

# 运行测试
test:
	pytest

# 运行测试并生成覆盖率报告
test-cov:
	pytest --cov=py_myt --cov-report=html --cov-report=term

# 代码风格检查
lint:
	flake8 py_myt/ tests/

# 代码格式化
format:
	black py_myt/ tests/

# 类型检查
type-check:
	mypy py_myt/

# 清理构建文件
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 构建包
build: clean
	python setup.py sdist bdist_wheel

# 上传到PyPI (需要先配置twine)
upload: build
	twine upload dist/*

# 生成文档 (如果使用sphinx)
docs:
	@echo "文档生成功能待实现"

# 运行所有检查
check: lint type-check test

# 开发环境设置
dev-setup: install-dev
	@echo "开发环境设置完成"
	@echo "可以运行 'make check' 来验证环境"