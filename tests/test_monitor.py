from pathlib import Path

from pypi_sdk_space.config import MonitorConfig
from pypi_sdk_space.monitor import run_monitor


def test_run_monitor_first_run(tmp_path: Path, monkeypatch) -> None:
    state = tmp_path / "state.json"
    cfg = MonitorConfig(
        repo="thanabartbb/pypi-sdk.space",
        pypi_package="pypi-sdk-space-nonexistent-xyz",
        state_file=state,
        slack_channel_id=None,
        pypi_publishing_errors_url="https://pypi.org/manage/account/publishing/#errors",
        github_default_branch="main",
    )
    report = run_monitor(config=cfg, persist_state=True, force_notify=False)
    assert report["package"] == "pypi-sdk-space-nonexistent-xyz"
    assert report["pypi_exists"] is False
    assert state.is_file()
