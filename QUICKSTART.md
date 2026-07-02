# bloaty-wheel 快速开始

## 安装

### 使用 pip

```bash
pip install bloaty-wheel
```

### 使用 uv

```bash
uv pip install bloaty-wheel
```

### 使用 uvx（无需安装，直接运行）

```bash
uvx bloaty-wheel <binary-file>
```

## 基本使用

### 分析二进制文件

```bash
bloaty /path/to/your/binary
```

### 查看帮助

```bash
bloaty --help
```

## 常见用例

### 1. 分析程序大小

```bash
# 分析编译好的程序
bloaty ./my_program

# 输出示例：
#     FILE SIZE        VM SIZE    
#  --------------  -------------- 
#   38.4%   231Ki  38.4%   231Ki    .text
#   18.1%   109Ki  18.1%   109Ki    .rodata
#   15.2%  91.5Ki   0.0%       0    .debug_info
#   ...
```

### 2. 按不同维度分析

```bash
# 按段（sections）
bloaty -d sections ./my_program

# 按符号（symbols）
bloaty -d symbols ./my_program

# 按编译单元
bloaty -d compileunits ./my_program

# 按文件（需要调试信息）
bloaty -d files ./my_program

# 多维度组合
bloaty -d sections,symbols ./my_program
```

### 3. 比较两个版本

```bash
# 比较优化前后的差异
gcc -O0 program.c -o program_O0
gcc -O3 program.c -o program_O3
bloaty program_O3 -- program_O0

# 输出会显示大小变化：
#     VM SIZE                      FILE SIZE
#  ++++++++++++++ GROWING ++++++++++++++
#   [ = ]       0  [ = ]       0    .debug_info
#   +10%    +1Ki  +10%    +1Ki    .text
#  -------------- SHRINKING --------------
#   -15%    -2Ki  -15%    -2Ki    .rodata
```

### 4. 导出数据

```bash
# CSV 格式
bloaty --csv ./my_program > sizes.csv

# TSV 格式
bloaty --tsv ./my_program > sizes.tsv
```

## 高级选项

### 显示更多/更少行

```bash
# 显示前 50 个最大项
bloaty -n 50 ./my_program

# 显示所有项
bloaty -n 0 ./my_program
```

### 设置阈值

```bash
# 只显示大于 1KB 的项
bloaty --threshold=1024 ./my_program
```

### 详细输出

```bash
# 显示详细信息
bloaty -v ./my_program
```

## 实际案例

### 案例 1：优化 C++ 程序大小

```bash
# 原始版本
g++ -g -O0 main.cpp -o main_debug
bloaty main_debug

# 优化版本
g++ -Os -ffunction-sections -fdata-sections -Wl,--gc-sections main.cpp -o main_opt
bloaty main_opt

# 比较差异
bloaty main_opt -- main_debug
```

### 案例 2：分析静态库

```bash
# 创建静态库
ar rcs libmylib.a obj1.o obj2.o obj3.o

# 分析库文件
bloaty -d symbols libmylib.a
```

### 案例 3：找出最大的函数

```bash
# 按符号大小排序
bloaty -d symbols -n 20 ./my_program | grep "FUNC"
```

## 与其他工具集成

### Make

```makefile
.PHONY: size-report
size-report: my_program
	bloaty --csv $< > build/size-report.csv
```

### CMake

```cmake
add_custom_target(size-report
    COMMAND bloaty --csv $<TARGET_FILE:my_program> > size-report.csv
    DEPENDS my_program
)
```

### CI/CD（GitHub Actions）

```yaml
- name: Install bloaty
  run: pip install bloaty-wheel

- name: Analyze binary size
  run: |
    bloaty ./build/my_program
    bloaty --csv ./build/my_program > size-report.csv

- name: Upload size report
  uses: actions/upload-artifact@v4
  with:
    name: size-report
    path: size-report.csv
```

## 疑难解答

### 问题：找不到调试信息

如果看到 "No debug info found"：

```bash
# 确保编译时包含调试信息
gcc -g program.c -o program
```

### 问题：文件格式不支持

Bloaty 支持：
- ELF（Linux）
- Mach-O（macOS）
- PE/COFF（Windows）
- WebAssembly

如果文件格式不支持，会显示错误信息。

### 问题：权限错误

确保二进制文件有读权限：
```bash
chmod +r /path/to/binary
```

## 更多资源

- [Bloaty 官方文档](https://github.com/google/bloaty/blob/master/doc/using.md)
- [GitHub Issues](https://github.com/yourusername/bloaty-wheel/issues)
