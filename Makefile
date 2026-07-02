.PHONY: help install test clean build lint format check-version

help:
	@echo "bloaty-wheel - Makefile 帮助"
	@echo ""
	@echo "可用命令："
	@echo "  make install        - 开发模式安装"
	@echo "  make test          - 运行测试"
	@echo "  make lint          - 代码检查"
	@echo "  make format        - 代码格式化"
	@echo "  make build         - 构建 wheel"
	@echo "  make clean         - 清理构建文件"
	@echo "  make check-version - 检查版本一致性"

install:
	pip install -e ".[dev]" -v

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/
	mypy src/bloaty/ --ignore-missing-imports

format:
	ruff format src/ tests/

build:
	python -m build

clean:
	rm -rf build/ dist/ *.egg-info _skbuild/ .pytest_cache/ __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

check-version:
	@echo "Checking version consistency..."
	@BLOATY_VER=$$(cat bloaty_version.txt); \
	PYPROJECT_VER=$$(grep '^version = ' pyproject.toml | cut -d'"' -f2 | cut -d'.' -f1-3); \
	if [ "$$BLOATY_VER" = "$$PYPROJECT_VER" ]; then \
		echo "✓ Versions match: $$BLOATY_VER"; \
	else \
		echo "✗ Version mismatch!"; \
		echo "  bloaty_version.txt: $$BLOATY_VER"; \
		echo "  pyproject.toml: $$PYPROJECT_VER"; \
		exit 1; \
	fi
