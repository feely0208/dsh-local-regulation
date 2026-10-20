from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from utils.mask import mask_id_card, mask_phone

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@router.get("/me/export")
def export_my_data(member_id: int):
    """本人查阅、复制自己的会员数据：先脱敏再导出。"""
    df = pd.read_sql("SELECT * FROM member WHERE id = ?", conn(), params=[member_id])
    df["phone"] = df["phone"].map(mask_phone)
    df["id_card"] = df["id_card"].map(mask_id_card)
    out = DATA_DIR / f"member_{member_id}.csv"
    df[["phone", "id_card", "level"]].to_csv(out, index=False)
    return {"file": str(out)}
