"""pytest 配置和共享 fixtures"""

import pytest


@pytest.fixture
def sample_binary():
    """
    提供一个示例二进制文件用于测试。

    在实际测试中，这可以是一个简单的编译好的可执行文件。
    """
    # 这里可以返回 Python 解释器本身作为测试目标
    import sys
    return sys.executable
