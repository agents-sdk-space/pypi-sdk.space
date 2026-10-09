---
description: ตั้งงานติดตาม PyPI/repo และแจ้ง Slack เมื่อมีการเปลี่ยนแปลง
---

ตั้ง monitoring สำหรับ **pypi-sdk.space**:

1. ตรวจว่า GitHub Actions workflow `monitor-and-notify.yml` อยู่ใน repo และ secret `SLACK_WEBHOOK_URL` ถูกตั้งใน GitHub (แจ้งผู้ใช้ถ้ายังไม่มี)
2. ใช้ `subscribe_timer` (cursor-subscriptions) ชื่อ `pypi-sdk-space-monitor` ด้วย cron `0 2 * * 1-5` (จ–ศ 09:00 กรุงเทพ) และ prompt:
   - รัน `/pypi-slack-update`
   - ถ้า publish gap หรือ CI publish ล้มเหลว ให้เน้นลิงก์ https://pypi.org/manage/account/publishing/#errors
3. (Optional) `subscribe_github_ci` สำหรับ branch ที่กำลังทำงาน หลัง push ที่เกี่ยวกับ publish

บอกผู้ใช้ว่าตั้ง timer แล้ว และสรุปช่องทางแจ้งเตือน: GitHub schedule + Cursor timer + `/pypi-slack-update`
