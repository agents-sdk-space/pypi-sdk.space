---
description: เช็คก่อน publish ไป PyPI (build, twine, trusted publishing checklist)
---

**งานระยะ (ทุก 6 ชม.):** ใช้ `/pypi-maintain-6h` — ตรวจและบำรุง repo อัตโนมัติ (doctor → test/lint → build → monitor → Slack) ตาม `pypi-maintain-6h.yml` และ timer ในแชท

ก่อน release/publish ให้ทำตามลำดับ:

1. `pypi-space doctor` — ต้องมี twine และ pyproject ถูกต้อง
2. `make test` และ `make lint`
3. `make check-dist` (build + twine check)
4. `pypi-space publishing` — แสดง checklist และลิงก์ errors dashboard
5. ยืนยัน PyPI Trusted Publisher ตรงกับ:
   - Repo **`agents-sdk-space/pypi-sdk.space`**
   - Workflow **`publish.yml`**
   - แพ็กเกจ **`pypi-sdk-space`** — [0.1.0 บน PyPI](https://pypi.org/project/pypi-sdk-space/0.1.0/)
   - Actions: [publish.yml runs](https://github.com/agents-sdk-space/pypi-sdk.space/actions/workflows/publish.yml)
6. ถ้า publish ล้มเหลว เปิด **https://pypi.org/manage/account/publishing/#errors**

สรุปผล pass/fail เป็นตารางสั้นๆ เป็นภาษาไทย
