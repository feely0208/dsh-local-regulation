from fastapi import APIRouter, HTTPException

from api.db import conn, query

router = APIRouter()


@router.get("/open/member/{member_id}")
def get_member(member_id: int):
    """合作门店查询会员的基础联系方式（仅返回必要字段）。"""
    row = query("SELECT phone, email FROM member WHERE id = ?", member_id)
    if not row:
        raise HTTPException(status_code=404, detail="member not found")
    return {
        "member_id": member_id,
        "phone": row["phone"],
        "email": row["email"],
    }
