from fastapi import FastAPI, HTTPException

from api.db import query

app = FastAPI(title="星链开放接口")


@app.get("/open/member/{member_id}")
def get_member(member_id: int):
    """合作门店查询会员的基础联系方式。"""
    row = query("SELECT phone, email FROM member WHERE id = ?", member_id)
    if not row:
        raise HTTPException(status_code=404, detail="member not found")
    return {
        "member_id": member_id,
        "phone": row["phone"],
        "email": row["email"],
    }
