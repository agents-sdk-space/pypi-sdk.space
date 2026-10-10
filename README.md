# pypi-sdk.space

เครื่องมือ CLI และ automation สำหรับ repo **[thanabartbb/pypi-sdk.space](https://github.com/thanabartbb/pypi-sdk.space)** — build, ตรวจสุขภาพก่อน publish ไป PyPI, ติดตามการเปลี่ยนแปลง และแจ้ง Slack

ลิงก์สำคัญสำหรับบัญชี PyPI ของคุณ (Trusted publishing / errors):

**https://pypi.org/manage/account/publishing/#errors**

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
2. ตั้งชื่อ secret ให้ตรง **`SLACK_WEBHOOK_URL`** (URL เต็มของ webhook)
   - **Cloud Agent Environment** — สำหรับรัน `pypi-space monitor slack` ใน agent (ต้องชื่อตัวแปรนี้; หลังเพิ่ม secret ให้เริ่ม agent ใหม่)
   - **GitHub repo secrets** — สำหรับ workflow `monitor-and-notify.yml` / `wf_spacejob.yml` บน GitHub
3. ใน Cursor ใช้ **`/pypi-slack-update`** ได้แม้ webhook ไม่ถูก inject ใน VM (agent โพสต์ผ่าน Slack MCP ไป `#general` ตาม `config/monitor.yaml`)
4. Workflow `monitor-and-notify.yml` รันตาม schedule และเมื่อ push ที่ `main`

Channel เริ่มต้นใน `config/monitor.yaml` ชี้ไป `#general` — แก้ `slack.channel_id` ได้

ตรวจว่า webhook พร้อมหรือยัง: `pypi-space doctor` (แถว `SLACK_WEBHOOK_URL`)

## `pyproject.toml` (ส่วนหัว)

ใช้ **setuptools** ตามเทมเพลต PyPI — ต้องตรงกับแพ็กเกจ **`pypi-sdk.space`** ก่อน publish:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "pypi-sdk.space"
version = "0.1.0"
description = "Your description here"
readme = "README.md"
requires-python = ">=3.7"

[project.urls]
"Homepage" = "https://github.com/agents-sdk-space/pypi-sdk.space"
```

Build ในเครื่อง: `pypi-space build` หรือ `python -m build` → ไฟล์ใน `dist/`

## Publish ไป PyPI

ตั้งค่า Trusted Publisher บน PyPI ให้ตรงกับ repo นี้:

| ฟิลด์ PyPI | ค่า |
|------------|-----|
| ชื่อโปรเจกต์ | **`pypi-sdk.space`** |
| GitHub repo | **`thanabartbb/pypi-sdk.space`** |
| Workflow | **`wf_spacejob.yml`** |
| Environment | ใดก็ได้ |

Publish: สร้าง [GitHub Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) → workflow [`.github/workflows/wf_spacejob.yml`](.github/workflows/wf_spacejob.yml) จะ build และอัปโหลดด้วย [Trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC)

ติดตามดาวน์โหลด: [pypistats.org/packages/pypi-sdk.space](https://pypistats.org/packages/pypi-sdk.space)

หาก publish ล้มเหลว เปิดหน้า errors ของบัญชี PyPI:

https://pypi.org/manage/account/publishing/#errors

## License

Apache-2.0 — see [LICENSE](LICENSE).
