# pypi-sdk.space

เครื่องมือ CLI และ automation สำหรับ repo **[thanabartbb/pypi-sdk.space](https://github.com/thanabartbb/pypi-sdk.space)** — build, ตรวจสุขภาพก่อน publish ไป PyPI, ติดตามการเปลี่ยนแปลง และแจ้ง Slack

ลิงก์สำคัญสำหรับบัญชี PyPI ของคุณ (Trusted publishing /):

**https://pypi-sdk.space/**

## ติดตั้ง

```bash
make dev
pypi-space doctor
```

## คำสั่งพื้นฐาน (CLI)

| คำสั่ง | ใช้เมื่อ |
|--------|----------|
| `pypi-space doctor` | ตรวจ Python, twine, webhook, config |
| `pypi-space version show` | ดูเวอร์ชันใน `pyproject.toml` |
| `pypi-space version bump patch --write` | bump semver แล้วเขียนไฟล์ |
| `pypi-space build` | สร้าง wheel + sdist ใน `dist/` |
| `pypi-space check-dist` | `twine check` บน artifact |
| `pypi-space pypi info <name>` | อ่านเวอร์ชันล่าสุดจาก PyPI |
| `pypi-space publishing` | checklist + ลิงก์ publishing errors |
| `pypi-space monitor run --json` | สแกนการเปลี่ยนแปลง (local vs PyPI) |
| `pypi-space monitor slack` | ส่งสรุปไป Slack ผ่าน `SLACK_WEBHOOK_URL` |

Makefile shortcuts: `make test`, `make monitor`, `make monitor-slack`

## Cursor commands (ใน IDE)

พิมพ์ `/` แล้วเลือก:

- `/pypi-status` — สรุปสุขภาพ repo + PyPI
- `/pypi-publish-check` — เช็คก่อน release / publish
- `/pypi-slack-update` — รัน monitor แล้วโพสต์ Slack (MCP)
- `/pypi-watch` — ตั้ง timer ให้ agent ติดตามและแจ้งเป็นระยะ

## Slack & GitHub Actions

1. สร้าง **Incoming Webhook** ใน Slack workspace
2. ใส่ secret ใน GitHub repo: `SLACK_WEBHOOK_URL`
3. Workflow `monitor-and-notify.yml` จะรันตาม schedule และเมื่อ push ที่ `main`

Channel เริ่มต้นใน `config/monitor.yaml` ชี้ไป `#general` — แก้ `slack.channel_id` ได้

## Publish ไป PyPI

ใช้ [Trusted publishing](https://docs.pypi.org/trusted-publishers/) จาก GitHub Actions (`publish.yml`) หลัง tag release

หาก publish ล้มเหลว เปิดหน้า errors ของบัญชี PyPI:

https://pypi.org/manage/account/publishing/#errors

## License

Apache-2.0 — see [LICENSE](LICENSE).
