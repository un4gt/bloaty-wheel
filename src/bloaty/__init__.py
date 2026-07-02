"""
bloaty-wheel: Python distribution of Google Bloaty McBloatface

A size profiler for binaries that shows the size breakdown of your compiled
executables and libraries.
"""

import functools
import subprocess
import sys
from importlib.resources import files
from pathlib import Path

__version__ = "1.1.0.0"


@functools.cache
def _get_executable(name: str) -> Path:
    """
    查找 bloaty 可执行文件。

    支持多种可能的扩展名（Windows .exe，Unix 无扩展名）。

    Args:
        name: 可执行文件名称（不含扩展名）

    Returns:
        可执行文件的完整路径

    Raises:
        FileNotFoundError: 如果找不到可执行文件
    """
    # 检测多种可能的可执行文件扩展名
    package_root = Path(str(files("bloaty")))
    possibles = [
        package_root / "data" / "bin" / f"{name}{suffix}"
        for suffix in ("", ".exe")
    ]

    for exe_path in possibles:
        if exe_path.exists():
            return exe_path

    # 如果都找不到，提供详细的错误信息
    searched_paths = "\n  ".join(str(p) for p in possibles)
    raise FileNotFoundError(
        f"Could not find bloaty executable. Searched:\n  {searched_paths}"
    )


def bloaty():
    """
    bloaty 命令行入口点。

    直接调用 bloaty 可执行文件并传递所有命令行参数。
    退出码与 bloaty 进程的退出码相同。
    """
    try:
        executable = _get_executable("bloaty")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)

    # 构建命令并传递所有参数
    command = [str(executable)] + sys.argv[1:]

    # 直接调用并返回退出码
    raise SystemExit(subprocess.call(command))


if __name__ == "__main__":
    bloaty()
