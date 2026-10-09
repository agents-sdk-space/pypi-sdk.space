from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

PYPI_JSON = "https://pypi.org/pypi/{name}/json"
PYPI_PROJECT = "https://pypi.org/project/{name}/"


@dataclass(frozen=True)
class ReleaseInfo:
    name: str
    latest_version: str | None
    uploaded_at: str | None
    project_url: str
    exists: bool


def fetch_release_info(package_name: str, *, timeout: float = 30.0) -> ReleaseInfo:
    url = PYPI_JSON.format(name=package_name)
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(url)
        if response.status_code == 404:
            return ReleaseInfo(
                name=package_name,
                latest_version=None,
                uploaded_at=None,
                project_url=PYPI_PROJECT.format(name=package_name),
                exists=False,
            )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()

    info = payload.get("info") or {}
    latest = info.get("version")
    releases = payload.get("releases") or {}
    uploaded_at: str | None = None
    if isinstance(latest, str) and latest in releases and releases[latest]:
        files = releases[latest]
        if isinstance(files, list) and files:
            first = files[0]
            if isinstance(first, dict):
                uploaded_at = first.get("upload_time") or first.get("upload_time_iso8601")

    return ReleaseInfo(
        name=package_name,
        latest_version=latest if isinstance(latest, str) else None,
        uploaded_at=uploaded_at if isinstance(uploaded_at, str) else None,
        project_url=PYPI_PROJECT.format(name=package_name),
        exists=True,
    )
