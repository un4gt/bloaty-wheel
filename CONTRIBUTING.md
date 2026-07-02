# Contributing to bloaty-wheel

感谢你对 bloaty-wheel 项目的关注！

## 项目结构

```
bloaty-wheel/
├── src/bloaty/          # Python 包装器
│   └── __init__.py      # 主入口点
├── tests/               # 测试
│   ├── conftest.py
│   └── test_executable.py
├── CMakeLists.txt       # CMake 构建脚本
├── pyproject.toml       # Python 项目配置
├── bloaty_version.txt   # Bloaty 版本号
└── .github/workflows/   # CI/CD 工作流
```

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/bloaty-wheel.git
cd bloaty-wheel
```

2. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

3. 安装开发依赖：
```bash
pip install -e ".[dev]"
```

4. 安装构建工具：
```bash
pip install scikit-build-core ninja pytest
```

## 本地测试

运行测试：
```bash
pytest tests/ -v
```

构建并测试安装：
```bash
pip install -e . -v
bloaty --help
```

## 更新 Bloaty 版本

当 Google Bloaty 发布新版本时：

1. 更新 `bloaty_version.txt`：
```bash
echo "1.2.0" > bloaty_version.txt
```

2. 更新 `pyproject.toml` 中的版本号：
```toml
version = "1.2.0.0"  # 最后的 .0 是打包版本
```

3. 测试构建：
```bash
pip install -e . -v
```

4. 提交并创建 tag：
```bash
git add bloaty_version.txt pyproject.toml
git commit -m "Update to bloaty 1.2.0"
git tag v1.2.0.0
git push origin main --tags
```

## 代码风格

- Python 代码遵循 PEP 8
- 使用 `ruff` 进行代码检查
- 使用类型注解（mypy 检查）

运行检查：
```bash
ruff check src/ tests/
mypy src/bloaty/ --ignore-missing-imports
```

## 提交 Pull Request

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建 Pull Request

## 发布流程

发布由 GitHub Actions 自动处理：

1. 更新版本号（如上所述）
2. 创建并推送 tag：`git tag v1.1.0.0 && git push --tags`
3. GitHub Actions 将自动：
   - 为多个平台构建 wheels
   - 运行测试
   - 发布到 PyPI（需要配置 secrets）

## 报告问题

发现 bug 或有功能建议？请在 [GitHub Issues](https://github.com/yourusername/bloaty-wheel/issues) 中提出。

## 许可证

通过贡献代码，你同意你的贡献将采用与本项目相同的 Apache License 2.0 许可证。
