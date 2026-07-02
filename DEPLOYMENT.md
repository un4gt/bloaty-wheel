# bloaty-wheel 部署指南

## 前提条件

1. GitHub 账号
2. PyPI 账号（用于发布）
3. 本地安装：Python 3.8+, Git, Ninja

## 一、本地测试

### 1. 克隆并初始化

```bash
cd bloaty-wheel
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 安装构建依赖

```bash
pip install scikit-build-core ninja pytest build
```

### 3. 本地构建测试

```bash
# 开发模式安装（会触发 CMake 构建）
pip install -e . -v

# 测试命令
bloaty --help
```

**注意**: 首次构建会下载 bloaty 源码并编译，需要 5-15 分钟，取决于你的机器性能。

### 4. 运行测试

```bash
pytest tests/ -v
```

## 二、推送到 GitHub

### 1. 创建 GitHub 仓库

在 GitHub 上创建新仓库：`bloaty-wheel`

### 2. 推送代码

```bash
git remote add origin https://github.com/你的用户名/bloaty-wheel.git
git push -u origin main
```

### 3. 配置 GitHub Secrets

需要配置以下 secrets 用于自动发布到 PyPI：

**方法 A: 使用 API Token（推荐）**

1. 访问 https://pypi.org/manage/account/token/
2. 创建新的 API token，选择 "Entire account" 作用域
3. 在 GitHub 仓库设置中添加 secret:
   - Name: `PYPI_API_TOKEN`
   - Value: 你的 PyPI token（以 `pypi-` 开头）

**方法 B: 使用 Trusted Publishers（更安全）**

1. 在 PyPI 上为项目添加 GitHub Actions 作为 trusted publisher
2. 不需要配置 secret，GitHub Actions 会自动获取临时 token

详细文档: https://docs.pypi.org/trusted-publishers/

### 4. 启用 GitHub Actions

确保 GitHub Actions 在你的仓库中启用：
- Settings → Actions → General → Allow all actions

## 三、本地测试 CI/CD 工作流（可选）

使用 `act` 工具在本地测试 GitHub Actions：

```bash
# 安装 act
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows
choco install act-cli

# 测试工作流
act -l  # 列出所有工作流
act push  # 模拟 push 事件
```

## 四、发布第一个版本

### 1. 确认版本号

检查 `pyproject.toml` 和 `bloaty_version.txt`:
```toml
version = "1.1.0.0"  # 格式：bloaty版本.打包版本
```

### 2. 创建 Release Tag

```bash
git tag v1.1.0.0
git push origin v1.1.0.0
```

### 3. 监控构建过程

1. 访问 GitHub Actions 页面
2. 查看 "Build and Release" 工作流
3. 等待所有平台构建完成（约 30-60 分钟）

### 4. 验证发布

构建成功后，检查：
- GitHub Releases 页面应该有新的 release
- PyPI 上应该能看到新版本：https://pypi.org/project/bloaty-wheel/

### 5. 测试安装

```bash
# 在新的虚拟环境中测试
python -m venv test_env
source test_env/bin/activate
pip install bloaty-wheel
bloaty --help
```

## 五、常见问题排查

### 问题 1: CMake 找不到 Ninja

**解决**:
```bash
pip install ninja
# 或
sudo apt-get install ninja-build  # Linux
brew install ninja  # macOS
```

### 问题 2: 编译失败 - 下载超时

**解决**:
```bash
# 手动下载 bloaty 源码
wget https://github.com/google/bloaty/releases/download/v1.1/bloaty-1.1.tar.bz2
# 放到 CMake 的下载缓存目录
mkdir -p _skbuild/downloads
mv bloaty-1.1.tar.bz2 _skbuild/downloads/
```

### 问题 3: GitHub Actions 构建超时

**原因**: 编译 bloaty 可能需要很长时间

**解决**: 
- 检查 `.github/workflows/release.yml` 中的 sccache 配置
- 考虑减少构建的平台数量（先只构建 Linux x86_64 测试）

### 问题 4: PyPI 发布失败

**原因**: 版本号冲突或权限问题

**解决**:
1. 确保版本号是新的，没有在 PyPI 上发布过
2. 检查 PyPI token 是否正确配置
3. 查看 GitHub Actions 日志中的详细错误信息

### 问题 5: 测试失败 - bloaty 命令找不到

**原因**: 可能是安装路径问题

**解决**:
```bash
# 检查安装
pip show bloaty-wheel
python -c "from bloaty import _get_executable; print(_get_executable('bloaty'))"
```

## 六、持续维护

### 更新 Bloaty 版本

当 Google Bloaty 发布新版本时：

1. 更新版本文件：
```bash
echo "1.2.0" > bloaty_version.txt
```

2. 更新 pyproject.toml：
```toml
version = "1.2.0.0"
```

3. 测试构建：
```bash
pip install -e . -v
bloaty --version
```

4. 提交并发布：
```bash
git add bloaty_version.txt pyproject.toml
git commit -m "Update to bloaty 1.2.0"
git tag v1.2.0.0
git push origin main --tags
```

### 监控自动化

考虑设置 GitHub Actions 定期检查 bloaty 新版本：
- 每周运行一次检查
- 发现新版本时自动创建 PR
- 参考 clangd-wheel 的 `check-llvm-version.yml`

## 七、发布检查清单

发布前检查：

- [ ] 本地构建成功
- [ ] 所有测试通过
- [ ] README.md 文档完整
- [ ] 版本号正确更新
- [ ] LICENSE 文件存在
- [ ] GitHub Actions secrets 已配置
- [ ] 创建了正确的 git tag

发布后验证：

- [ ] GitHub Actions 构建成功
- [ ] PyPI 上可以看到新版本
- [ ] 可以通过 pip install 安装
- [ ] 命令行工具正常工作
- [ ] 在不同平台上测试（Linux/macOS/Windows）

## 八、获取帮助

如果遇到问题：

1. 查看 `PROJECT_SUMMARY.md` 了解项目架构
2. 参考 `CONTRIBUTING.md` 了解开发流程
3. 查看 GitHub Actions 日志获取详细错误信息
4. 在 GitHub Issues 中提问
5. 参考 clangd-wheel 项目的类似实现

## 资源链接

- [scikit-build-core 文档](https://scikit-build-core.readthedocs.io/)
- [cibuildwheel 文档](https://cibuildwheel.readthedocs.io/)
- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [clangd-wheel 参考](https://github.com/jmpfar/clangd-wheel)
