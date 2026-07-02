# bloaty-wheel

Python wheel distribution of [Google Bloaty McBloatface](https://github.com/google/bloaty) - a size profiler for binaries.

## 什么是 Bloaty？

Bloaty McBloatface 是一个用于分析二进制文件（可执行文件、库文件等）大小的工具。它可以帮助你了解：

- 哪些部分占用了最多的空间
- 编译选项对二进制大小的影响
- 不同符号、段、文件的大小分布

支持的格式：
- ELF (Linux)
- Mach-O (macOS)
- PE/COFF (Windows)
- WebAssembly

## 安装

使用 pip、uv 或 uvx 安装：

```bash
# 使用 pip
pip install bloaty-wheel

# 使用 uv
uv pip install bloaty-wheel

# 或者直接用 uvx 运行（无需安装）
uvx bloaty-wheel <binary-file>
```

安装后，`bloaty` 命令将自动添加到你的 PATH 中。

## 使用方法

### 基本用法

```bash
# 分析一个二进制文件
bloaty /path/to/binary

# 查看帮助
bloaty --help
```

### 常用选项

```bash
# 按段（sections）显示
bloaty -d sections /path/to/binary

# 按符号（symbols）显示
bloaty -d symbols /path/to/binary

# 按编译单元（compile units）显示
bloaty -d compileunits /path/to/binary

# 按文件显示（需要调试信息）
bloaty -d files /path/to/binary

# 多维度分析
bloaty -d sections,symbols /path/to/binary

# 比较两个二进制文件
bloaty /path/to/binary1 -- /path/to/binary2
```

### 输出格式

```bash
# CSV 格式输出
bloaty --csv /path/to/binary

# TSV 格式输出
bloaty --tsv /path/to/binary
```

## 示例

### 分析 Python 解释器

```bash
bloaty $(which python3)
```

输出示例：
```
    FILE SIZE        VM SIZE    
 --------------  -------------- 
  64.5%  3.83Mi   0.0%       0    .debug_info
  13.3%   811Ki   0.0%       0    .debug_str
   7.9%   483Ki   0.0%       0    .debug_line
   3.8%   231Ki  38.4%   231Ki    .text
   2.3%   138Ki   0.0%       0    .debug_abbrev
   1.8%   109Ki  18.1%   109Ki    .rodata
   ...
```

### 比较优化前后的差异

```bash
# 编译两个版本
gcc -O0 -g program.c -o program_O0
gcc -O3 -g program.c -o program_O3

# 比较大小差异
bloaty program_O3 -- program_O0
```

## 工作原理

bloaty-wheel 项目：

1. 在构建时从 Google Bloaty 官方仓库下载源码
2. 使用 CMake 编译成静态链接的独立可执行文件
3. 将编译好的二进制文件打包成 Python wheel
4. 通过轻量级的 Python 包装器提供命令行访问

这样你就可以像安装普通 Python 包一样安装 bloaty，无需手动编译或配置。

## 优势

相比手动编译 bloaty：

- ✅ **一键安装**：`pip install bloaty-wheel` 即可
- ✅ **无需依赖**：静态链接，无需安装 protobuf、re2、capstone 等依赖
- ✅ **跨平台**：支持 Linux (x86_64, ARM64)、macOS (Intel, Apple Silicon)、Windows
- ✅ **虚拟环境友好**：可以在项目的 venv 中独立安装
- ✅ **可重现构建**：版本锁定，CI/CD 友好

## 开发

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/yourusername/bloaty-wheel.git
cd bloaty-wheel

# 安装构建依赖
pip install scikit-build-core ninja

# 构建
pip install -e . -v

# 运行测试
pytest tests/
```

### 构建 wheel

```bash
# 本地构建
pip install build
python -m build

# 使用 cibuildwheel 构建多平台 wheel
pip install cibuildwheel
cibuildwheel --platform linux
```

## 版本说明

bloaty-wheel 的版本号格式为 `X.Y.Z.W`：
- `X.Y.Z` 对应 Google Bloaty 的版本
- `W` 是 bloaty-wheel 的打包版本

例如：`1.1.0.0` 表示 Bloaty 1.1.0 的第 0 次打包。

## 许可证

- Google Bloaty 本身采用 Apache License 2.0
- bloaty-wheel 打包项目同样采用 Apache License 2.0

## 相关链接

- [Google Bloaty 官方仓库](https://github.com/google/bloaty)
- [Bloaty 文档](https://github.com/google/bloaty/blob/main/doc/using.md)
- [clangd-wheel](https://github.com/jmpfar/clangd-wheel) - 类似项目，启发了 bloaty-wheel 的设计

## 致谢

- Google 团队开发的优秀工具 Bloaty McBloatface
- [clangd-wheel](https://github.com/jmpfar/clangd-wheel) 项目提供的打包思路
