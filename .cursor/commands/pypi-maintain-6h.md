---
description: ตรวจและบำรุง repo/pypi-sdk.space เป็นระยะ (ทุก 6 ชั่วโมง) — doctor, test, build, monitor, Slack
---

**งานบำรุงรักษา (Maintenance)** สำหรับ **pypi-sdk.space** — รันเมื่อ timer 6 ชม. หรือเมื่อผู้ใช้เรียกคำสั่งนี้

## เป้าหมาย

ตรวจสุขภาพ repo, เตรียม publish (`wf_spacejob.yml`), และแจ้ง Slack เมื่อมีการเปลี่ยนแปลง — **เว้นระยะทุก 6 ชั่วโมง**

## ขั้นตอน (ทำครบทุกครั้ง)

1. `pip install -e ".[dev]"` (ถ้ายังไม่ติดตั้ง)
2. `/pypi-publish-check` หรือเทียบเท่า:
   - `pypi-space doctor`
   - `make test` และ `make lint`
   - `make check-dist` (build + twine check — ขั้นเดียวกับ `.github/workflows/wf_spacejob.yml` ก่อน publish)
3. `pypi-space monitor run --json` — local vs PyPI **`pypi-sdk-space`** ([release 0.1.0](https://pypi.org/project/pypi-sdk-space/0.1.0/))
4. `/pypi-slack-update` — แจ้ง Slack (#general หรือ `config/monitor.yaml`) เมื่อมี diff สำคัญ
5. ถ้า publish/Trusted Publisher มีปัญหา ลิงก์ **https://pypi.org/manage/account/publishing/#errors**

## Automation ที่ผูกไว้

| ช่องทาง | รอบ |
|---------|-----|
| GitHub Actions `pypi-maintain-6h.yml` | cron `0 */6 * * *` |
| Cursor timer `pypi-sdk-space-maintain-6h` | ทุก 6 ชม. → รันคำสั่งนี้ |

สรุปผลเป็นภาษาไทย: pass/fail ต่อขั้น, เวอร์ชัน, publish gap, ลิงก์ repo **agents-sdk-space/pypi-sdk.space**
