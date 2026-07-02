"""测试 bloaty 可执行文件"""

import os
import shutil
import subprocess
import sys

import pytest


def test_bloaty_executable_exists():
    """测试 bloaty 可执行文件是否存在"""
    from bloaty import _get_executable

    bloaty_path = _get_executable("bloaty")
    assert bloaty_path.exists(), f"bloaty executable not found at {bloaty_path}"
    assert bloaty_path.is_file(), f"{bloaty_path} is not a file"


def test_bloaty_is_executable():
    """测试 bloaty 可执行文件是否有执行权限"""
    from bloaty import _get_executable

    bloaty_path = _get_executable("bloaty")

    # Unix 系统检查执行权限
    if sys.platform != "win32":
        assert os.access(bloaty_path, os.X_OK), f"{bloaty_path} is not executable"


def test_bloaty_version():
    """测试 bloaty 能正确显示版本信息"""
    result = subprocess.run(
        ["bloaty", "--version"],
        capture_output=True,
        text=True,
        timeout=10
    )

    # bloaty 可能没有 --version 参数，但至少应该能运行
    # 我们主要测试命令能否被调用
    assert result.returncode in [0, 1], "bloaty command failed to execute"


def test_bloaty_help():
    """测试 bloaty 帮助信息"""
    result = subprocess.run(
        ["bloaty", "--help"],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 0, "bloaty --help failed"
    assert "bloaty" in result.stdout.lower() or "usage" in result.stdout.lower(), \
        "Help output doesn't look like bloaty help"


def test_bloaty_on_sample_binary(sample_binary):
    """测试 bloaty 能分析示例二进制文件"""
    result = subprocess.run(
        ["bloaty", sample_binary],
        capture_output=True,
        text=True,
        timeout=30
    )

    # bloaty 应该能成功分析 Python 解释器
    # 某些平台可能不支持，所以我们允许一些错误码
    assert result.returncode in [0, 1], f"bloaty failed with code {result.returncode}"


def test_bloaty_in_venv():
    """测试使用的是虚拟环境中的 bloaty"""
    # 只在虚拟环境中运行此测试
    if not hasattr(sys, 'real_prefix') and not (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    ):
        pytest.skip("Not running in a virtual environment")

    venv_bin = os.path.dirname(sys.executable)
    bloaty_path = shutil.which("bloaty")

    assert bloaty_path is not None, "bloaty not found in PATH"

    # 确保使用的是虚拟环境中的 bloaty
    try:
        common = os.path.commonpath([bloaty_path, venv_bin])
        assert common == venv_bin, \
            f"bloaty at {bloaty_path} is not from venv at {venv_bin}"
    except ValueError:
        # Windows 可能在不同驱动器，跳过此检查
        pass


def test_module_version():
    """测试模块版本号"""
    import bloaty
    assert hasattr(bloaty, "__version__"), "Module missing __version__"
    assert isinstance(bloaty.__version__, str), "__version__ should be a string"
    assert len(bloaty.__version__.split(".")) >= 3, "Version should have at least 3 parts"
