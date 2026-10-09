from pathlib import Path

import pytest

from pypi_sdk_space.project import bump_version, load_project_meta


def test_bump_patch() -> None:
    assert bump_version("1.2.3", "patch") == "1.2.4"
    assert bump_version("0.1.0", "minor") == "0.2.0"
    assert bump_version("0.1.0", "major") == "1.0.0"


def test_load_project_meta() -> None:
    root = Path(__file__).resolve().parents[1]
    meta = load_project_meta(root / "pyproject.toml")
    assert meta.name == "pypi-sdk-space"
    assert meta.version == "0.1.0"


def test_bump_invalid() -> None:
    with pytest.raises(ValueError):
        bump_version("not-a-version", "patch")
