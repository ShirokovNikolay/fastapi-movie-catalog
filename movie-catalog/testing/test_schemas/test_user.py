import os
import sys
from pathlib import Path, WindowsPath

import pytest


@pytest.mark.skip(
    reason="user schema not implemented yet",
)
def test_user() -> None:
    user_data = {"username": "Nikolay"}
    assert user_data["username"] == "Ivan"


@pytest.mark.skipif(
    sys.version_info < (3, 13),
    reason="feature requires Python version >=3.13",
)
def test_feature() -> None:
    assert sys.version_info >= (3, 13)


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="skip test on Windows due to some reason",
)
def test_platform() -> None:
    assert sys.platform != "win32"


@pytest.mark.skipif(
    os.name != "nt",
    reason="run only on Windows",
)
def test_only_for_windows() -> None:
    path = Path(__file__)
    assert isinstance(path, WindowsPath)
