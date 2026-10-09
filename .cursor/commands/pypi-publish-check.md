---
description: เช็คก่อน publish ไป PyPI (build, twine, trusted publishing checklist)
---

ก่อน release/publish ให้ทำตามลำดับ:

1. `pypi-space doctor` — ต้องมี twine และ pyproject ถูกต้อง
2. `make test` และ `make lint`
3. `make check-dist` (build + twine check)
4. `pypi-space publishing` — แสดง checklist และลิงก์ errors dashboard
5. ยืนยัน PyPI Trusted Publisher ตรงกับ `thanabartbb/pypi-sdk.space` + workflow **`wf_spacejob.yml`** + ชื่อแพ็กเกจ **`pypi-sdk.space`**
6. ถ้า publish ล้มเหลวในอดีต ให้ผู้ใช้เปิด:
   **https://pypi.org/manage/account/publishing/#errors**

สรุปผล pass/fail เป็นตารางสั้นๆ เป็นภาษาไทย
