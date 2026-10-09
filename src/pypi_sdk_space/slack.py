from __future__ import annotations

import json
import os
from typing import Any

import httpx


class SlackNotifyError(RuntimeError):
    pass


def slack_webhook_configured() -> bool:
    return bool(os.environ.get("SLACK_WEBHOOK_URL", "").strip())


def post_webhook(
    *,
    text: str,
    blocks: list[dict[str, Any]] | None = None,
    timeout: float = 30.0,
) -> None:
    webhook = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if not webhook:
        raise SlackNotifyError(
            "SLACK_WEBHOOK_URL is not set. Add an incoming webhook URL in GitHub Actions secrets "
            "or export it locally before running monitor slack."
        )

    body: dict[str, Any] = {"text": text}
    if blocks:
        body["blocks"] = blocks

    with httpx.Client(timeout=timeout) as client:
        response = client.post(
            webhook,
            content=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
    if response.status_code >= 400:
        raise SlackNotifyError(
            f"Slack webhook returned HTTP {response.status_code}: {response.text[:500]}"
        )


def format_update_message(report: dict[str, Any]) -> str:
    lines = [
        f"*pypi-sdk.space monitor* — {report.get('summary', 'update')}",
        "",
    ]
    repo = report.get("repo")
    if repo:
        lines.append(f"Repo: `{repo}`")
    package = report.get("package")
    if package:
        lines.append(f"PyPI package: `{package}`")

    local = report.get("local_version")
    remote = report.get("pypi_version")
    if local is not None or remote is not None:
        lines.append(f"Version local/PyPI: `{local}` / `{remote or 'not published yet'}`")

    changes = report.get("changes") or []
    if changes:
        lines.append("")
        lines.append("*Changes detected:*")
        for item in changes:
            lines.append(f"• {item}")

    links = report.get("links") or {}
    if links:
        lines.append("")
        for label, url in links.items():
            lines.append(f"• {label}: {url}")

    return "\n".join(lines)
