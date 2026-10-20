from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from api.db import conn
from utils.mask import mask_id_card, mask_phone

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@router.get("/partner/export")
def export_partner_members():
    """合作方需要的会员明细：导出前先做字段掩码。"""
    df = pd.read_sql("SELECT * FROM member", conn())
    df["phone"] = df["phone"].map(mask_phone)
    df["id_card"] = df["id_card"].map(mask_id_card)
    out = DATA_DIR / "partner_members.csv"
    df[["phone", "id_card", "level"]].to_csv(out, index=False)
    return {"file": str(out), "rows": len(df)}
