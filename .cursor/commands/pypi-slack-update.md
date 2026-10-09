---
description: รัน PyPI monitor แล้วแจ้ง Slack เกี่ยวกับการเปลี่ยนแปลง (webhook หรือ Slack MCP)
---

อัปเดต Slack สำหรับ repo **agents-sdk-space/pypi-sdk.space**:

1. `pip install -e .` แล้ว `pypi-space monitor run --json` เพื่อได้รายงานล่าสุด
2. ถ้ามี `SLACK_WEBHOOK_URL` ใน environment: รัน `pypi-space monitor slack` (ใช้ `--force` ถ้าผู้ใช้ขอให้ส่งแม้ไม่มี diff)
3. ถ้าไม่มี webhook ให้ใช้ Slack MCP:
   - อ่าน `channel_id` จาก `config/monitor.yaml` (ค่าเริ่ม `#general`)
   - ส่งข้อความ markdown สรุป: เวอร์ชัน, changes, ลิงก์ repo, PyPI project, และ
     **https://pypi.org/manage/account/publishing/#errors**
   - ใช้ `slack_send_message` (หรือ draft ถ้าผู้ใช้ยังไม่ review)

ข้อความต้อง lead with the point และมี bullet ของ changes ชัดเจน
