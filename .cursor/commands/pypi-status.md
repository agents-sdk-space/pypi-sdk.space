---
description: สรุปสุขภาพ repo pypi-sdk.space, เวอร์ชัน local vs PyPI, และลิงก์ publishing errors
---

รันการตรวจสอบสำหรับ repo **agents-sdk-space/pypi-sdk.space**:

1. `make dev` หรือ `pip install -e ".[dev]"` ถ้ายังไม่ได้ติดตั้ง CLI
2. `pypi-space doctor`
3. `pypi-space monitor run --json`
4. อ่าน `config/monitor.yaml` และสรุปให้ผู้ใช้เป็นภาษาไทยสั้นๆ:
   - เวอร์ชันใน `pyproject.toml` vs PyPI
   - ว่ามี publish gap หรือไม่
   - ลิงก์ **https://pypi.org/manage/account/publishing/#errors**
   - ลิงก์ repo GitHub

ถ้ามีการเปลี่ยนแปลงสำคัญ แนะนำ `/pypi-slack-update`
