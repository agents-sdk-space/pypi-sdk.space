from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectMeta:
    name: str
    version: str
    pyproject_path: Path


def find_pyproject(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        path = candidate / "pyproject.toml"
        if path.is_file():
            return path
    raise FileNotFoundError("pyproject.toml not found in current directory or parents")


def load_project_meta(pyproject_path: Path | None = None) -> ProjectMeta:
    path = pyproject_path or find_pyproject()
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project")
    if not isinstance(project, dict):
        raise ValueError(f"Missing [project] table in {path}")
    name = project.get("name")
    version = project.get("version")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Missing project.name in {path}")
    if not isinstance(version, str) or not version.strip():
        raise ValueError(f"Missing project.version in {path}")
    return ProjectMeta(name=name.strip(), version=version.strip(), pyproject_path=path)


_SEMVER = re.compile(
    r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?P<rest>(?:[a-zA-Z0-9.-]+)?)$"
)


def bump_version(version: str, part: str) -> str:
    match = _SEMVER.match(version)
    if not match:
        raise ValueError(f"Unsupported version format: {version!r} (expected semver like 1.2.3)")
    major, minor, patch = (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
    )
    rest = match.group("rest") or ""
    if rest and not rest.startswith(("-", ".")):
        raise ValueError(f"Cannot auto-bump version with suffix: {version!r}")

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Unknown bump part: {part!r}")

    return f"{major}.{minor}.{patch}{rest}"


def write_project_version(pyproject_path: Path, new_version: str) -> None:
    text = pyproject_path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'(?m)^(\s*version\s*=\s*")[^"]+(")',
        rf'\g<1>{new_version}\2',
        text,
        count=1,
    )
    if count != 1:
        raise ValueError(f"Could not update version in {pyproject_path}")
    pyproject_path.write_text(updated, encoding="utf-8")
