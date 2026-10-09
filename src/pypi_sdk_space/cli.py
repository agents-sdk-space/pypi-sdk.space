from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from pypi_sdk_space import PYPI_PUBLISHING_ERRORS_URL, __version__
from pypi_sdk_space.config import load_monitor_config
from pypi_sdk_space.monitor import run_monitor
from pypi_sdk_space.project import bump_version, load_project_meta, write_project_version
from pypi_sdk_space.pypi_client import fetch_release_info
from pypi_sdk_space.slack import format_update_message, post_webhook, slack_webhook_configured

app = typer.Typer(
    no_args_is_help=True,
    help="PyPI + repo tooling for pypi-sdk.space (build, publish, monitor, Slack).",
)
console = Console()
version_app = typer.Typer(help="Show or bump the project version in pyproject.toml.")
pypi_app = typer.Typer(help="Read package metadata from PyPI.")
monitor_app = typer.Typer(help="Detect changes and notify Slack.")
app.add_typer(version_app, name="version")
app.add_typer(pypi_app, name="pypi")
app.add_typer(monitor_app, name="monitor")


class BumpPart(StrEnum):
    patch = "patch"
    minor = "minor"
    major = "major"


@app.callback()
def main() -> None:
    """pypi-space CLI entrypoint."""


@app.command("doctor")
def doctor_cmd() -> None:
    """Check local tools and configuration for publishing and monitoring."""
    table = Table(title="pypi-space doctor")
    table.add_column("Check")
    table.add_column("Status")

    def row(name: str, ok: bool, detail: str = "") -> None:
        if ok:
            status = f"[green]OK[/green] {detail}".strip()
        else:
            status = f"[red]MISSING[/red] {detail}".strip()
        table.add_row(name, status)

    row("python", True, sys.version.split()[0])
    row("git", shutil.which("git") is not None)
    row("build", shutil.which("python") is not None, "(module: python -m build)")
    row("twine", shutil.which("twine") is not None)
    row("SLACK_WEBHOOK_URL", slack_webhook_configured())
    injected = os.environ.get("CLOUD_AGENT_INJECTED_SECRET_NAMES", "").strip()
    if injected and not slack_webhook_configured():
        table.add_row(
            "Cloud secrets (names only)",
            f"[dim]{injected}[/dim] — add SLACK_WEBHOOK_URL for webhook CLI",
        )
    row("config/monitor.yaml", Path("config/monitor.yaml").is_file())

    try:
        meta = load_project_meta()
        row("pyproject.toml", True, f"{meta.name} @ {meta.version}")
    except Exception as exc:  # noqa: BLE001
        row("pyproject.toml", False, str(exc))

    cfg = load_monitor_config()
    table.add_row("repo", cfg.repo)
    table.add_row("PyPI errors URL", cfg.pypi_publishing_errors_url)
    console.print(table)


@version_app.command("show")
def version_show() -> None:
    meta = load_project_meta()
    console.print(f"{meta.name} {meta.version}")


@version_app.command("bump")
def version_bump(
    part: Annotated[BumpPart, typer.Argument(help="Semver part to increment.")],
    write: Annotated[
        bool, typer.Option("--write/--dry-run", help="Update pyproject.toml.")
    ] = False,
) -> None:
    meta = load_project_meta()
    new_version = bump_version(meta.version, part.value)
    if write:
        write_project_version(meta.pyproject_path, new_version)
        console.print(
            f"Bumped {meta.version} → [bold]{new_version}[/bold] in {meta.pyproject_path}"
        )
    else:
        console.print(
            f"Would bump {meta.version} → [bold]{new_version}[/bold] (pass --write to apply)"
        )


@pypi_app.command("info")
def pypi_info(name: Annotated[str, typer.Argument(help="PyPI project name.")]) -> None:
    info = fetch_release_info(name)
    if not info.exists:
        console.print(f"[yellow]{name}[/yellow] is not on PyPI yet.")
        raise typer.Exit(code=1)
    console.print(f"{info.name} latest: [bold]{info.latest_version}[/bold]")
    if info.uploaded_at:
        console.print(f"Uploaded: {info.uploaded_at}")
    console.print(f"URL: {info.project_url}")


@app.command("build")
def build_cmd(
    outdir: Annotated[str, typer.Option("--outdir", "-o")] = "dist",
) -> None:
    """Build wheel and sdist via python -m build."""
    Path(outdir).mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-m", "build", "--outdir", outdir], check=True)


@app.command("check-dist")
def check_dist_cmd(dist_dir: Annotated[str, typer.Argument()] = "dist") -> None:
    """Run twine check on built artifacts."""
    subprocess.run(["twine", "check", f"{dist_dir}/*"], check=True)


@app.command("publishing")
def publishing_cmd() -> None:
    """Print trusted publishing checklist and the PyPI errors dashboard link."""
    cfg = load_monitor_config()
    meta = load_project_meta()
    console.print("[bold]Trusted publishing checklist[/bold]")
    console.print(f"1. GitHub repo: https://github.com/{cfg.repo}")
    console.print("2. Trusted publisher on PyPI: workflow file wf_spacejob.yml (see README).")
    console.print("3. GitHub secret: SLACK_WEBHOOK_URL (for monitor notifications).")
    console.print(f"4. Package name on PyPI: [cyan]{meta.name}[/cyan]")
    console.print(f"5. Publishing errors dashboard: {cfg.pypi_publishing_errors_url}")
    console.print(f"   (same as {PYPI_PUBLISHING_ERRORS_URL})")


@monitor_app.command("run")
def monitor_run_cmd(
    json_out: Annotated[bool, typer.Option("--json", help="Print JSON report.")] = False,
    force: Annotated[bool, typer.Option("--force", help="Mark report as notify-worthy.")] = False,
    no_state: Annotated[bool, typer.Option("--no-state", help="Do not write state file.")] = False,
) -> None:
    report = run_monitor(persist_state=not no_state, force_notify=force)
    if json_out:
        console.print_json(json.dumps(report))
    else:
        console.print(format_update_message(report))
    if report.get("should_notify"):
        console.print("[yellow]Material changes detected (see changes in report).[/yellow]")


@monitor_app.command("slack")
def monitor_slack_cmd(
    force: Annotated[
        bool, typer.Option("--force", help="Send even if no material change.")
    ] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Print message only.")] = False,
) -> None:
    report = run_monitor(persist_state=True, force_notify=force)
    message = format_update_message(report)
    if dry_run:
        console.print(message)
        return
    if not report.get("should_notify") and not force:
        console.print("[dim]No material changes; use --force to send anyway.[/dim]")
        raise typer.Exit(code=0)
    post_webhook(text=message)
    console.print("[green]Sent Slack webhook notification.[/green]")


@app.command("version-cli")
def version_cli_cmd() -> None:
    """Print CLI version."""
    console.print(__version__)


if __name__ == "__main__":
    app()
