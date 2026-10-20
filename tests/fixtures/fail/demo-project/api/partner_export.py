from pathlib import Path

import pandas as pd
from fastapi import APIRouter

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def db_connection():
    """返回 MySQL 连接（内部使用）。"""
    import pymysql

    return pymysql.connect(host="127.0.0.1", user="app", database="member")


@router.get("/partner/export")
def export_partner_members():
    """合作方需要一份会员明细，按周导出 CSV。"""
    df = pd.read_sql("SELECT * FROM member", db_connection())
    columns = ["member_id", "real_name", "phone", "id_card", "level"]
    out = DATA_DIR / "partner_members.csv"
    df[columns].to_csv(out, index=False)
    return {"file": str(out), "rows": len(df)}
