from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pypi_sdk_space.config import MonitorConfig, load_monitor_config
from pypi_sdk_space.project import load_project_meta
from pypi_sdk_space.pypi_client import fetch_release_info


@dataclass
class MonitorState:
    local_version: str | None = None
    pypi_version: str | None = None
    pypi_uploaded_at: str | None = None
    last_notified_at: str | None = None


def _now_iso() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat()


def load_state(path: Path) -> MonitorState:
    if not path.is_file():
        return MonitorState()
    data = json.loads(path.read_text(encoding="utf-8"))
    return MonitorState(
        local_version=data.get("local_version"),
        pypi_version=data.get("pypi_version"),
        pypi_uploaded_at=data.get("pypi_uploaded_at"),
        last_notified_at=data.get("last_notified_at"),
    )


def save_state(path: Path, state: MonitorState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(state), indent=2) + "\n", encoding="utf-8")


def git_head_sha() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout.strip() or None


def git_latest_tag() -> str | None:
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout.strip() or None


def run_monitor(
    *,
    config: MonitorConfig | None = None,
    persist_state: bool = True,
    force_notify: bool = False,
) -> dict[str, Any]:
    cfg = config or load_monitor_config()
    meta = load_project_meta()
    release = fetch_release_info(cfg.pypi_package)
    previous = load_state(cfg.state_file)

    changes: list[str] = []
    if previous.local_version and previous.local_version != meta.version:
        changes.append(f"Local version changed: {previous.local_version} → {meta.version}")
    if previous.pypi_version != release.latest_version:
        prev = previous.pypi_version or "(none)"
        curr = release.latest_version or "(none)"
        changes.append(f"PyPI latest version changed: {prev} → {curr}")
    if previous.pypi_uploaded_at != release.uploaded_at and release.uploaded_at:
        changes.append(f"PyPI upload timestamp updated: {release.uploaded_at}")

    publish_gap = meta.version != (release.latest_version or "")
    if publish_gap and release.exists:
        changes.append(
            f"Local {meta.version} is ahead of PyPI {release.latest_version} — publish when ready"
        )
    if not release.exists:
        changes.append("Package not found on PyPI yet — first publish pending")

    head = git_head_sha()
    tag = git_latest_tag()

    is_baseline = previous.local_version is None and previous.pypi_version is None
    material_change = (
        not is_baseline
        and (
            previous.pypi_version != release.latest_version
            or previous.local_version != meta.version
            or previous.pypi_uploaded_at != release.uploaded_at
            or (not release.exists and previous.pypi_version is not None)
        )
    )
    should_notify = force_notify or material_change

    report: dict[str, Any] = {
        "checked_at": _now_iso(),
        "repo": cfg.repo,
        "package": cfg.pypi_package,
        "local_version": meta.version,
        "pypi_version": release.latest_version,
        "pypi_uploaded_at": release.uploaded_at,
        "pypi_exists": release.exists,
        "publish_gap": publish_gap,
        "git_head": head,
        "git_latest_tag": tag,
        "changes": changes,
        "should_notify": should_notify,
        "summary": "changes detected" if changes else "no material changes",
        "links": {
            "GitHub repo": f"https://github.com/{cfg.repo}",
            "PyPI project": release.project_url,
            "PyPI publishing errors": cfg.pypi_publishing_errors_url,
            "Trusted publishing docs": "https://docs.pypi.org/trusted-publishers/",
        },
    }

    if persist_state:
        new_state = MonitorState(
            local_version=meta.version,
            pypi_version=release.latest_version,
            pypi_uploaded_at=release.uploaded_at,
            last_notified_at=_now_iso() if should_notify else previous.last_notified_at,
        )
        save_state(cfg.state_file, new_state)

    return report
