from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from pypi_sdk_space import DEFAULT_REPO, PYPI_PUBLISHING_ERRORS_URL


@dataclass(frozen=True)
class MonitorConfig:
    repo: str
    pypi_package: str
    state_file: Path
    slack_channel_id: str | None
    pypi_publishing_errors_url: str
    github_default_branch: str


def default_config_path() -> Path:
    return Path("config/monitor.yaml")


def load_monitor_config(path: Path | None = None) -> MonitorConfig:
    cfg_path = path or default_config_path()
    if not cfg_path.is_file():
        return MonitorConfig(
            repo=DEFAULT_REPO,
            pypi_package="pypi-sdk.space",
            state_file=Path(".pypi-monitor/state.json"),
            slack_channel_id=None,
            pypi_publishing_errors_url=PYPI_PUBLISHING_ERRORS_URL,
            github_default_branch="main",
        )

    raw: dict[str, Any] = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    slack = raw.get("slack") or {}
    channel_id = slack.get("channel_id")
    return MonitorConfig(
        repo=str(raw.get("repo") or DEFAULT_REPO),
        pypi_package=str(raw.get("pypi_package") or "pypi-sdk.space"),
        state_file=Path(str(raw.get("state_file") or ".pypi-monitor/state.json")),
        slack_channel_id=str(channel_id) if channel_id else None,
        pypi_publishing_errors_url=str(
            raw.get("pypi_publishing_errors_url") or PYPI_PUBLISHING_ERRORS_URL
        ),
        github_default_branch=str(raw.get("github_default_branch") or "main"),
    )
