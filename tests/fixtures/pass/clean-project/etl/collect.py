import pandas as pd
import requests

FEED_URL = "https://feeds.example.com/orders.csv"
LOCAL_FILE = "data/orders.csv"


def pull_orders():
    """从合作方订单接口下载明细；来源与授权见 docs/数据来源与处理记录.md。"""
    resp = requests.get(FEED_URL, timeout=10)
    resp.raise_for_status()
    with open(LOCAL_FILE, "wb") as fh:
        fh.write(resp.content)
    return pd.read_csv(LOCAL_FILE)


def summarise():
    df = pull_orders()
    return df.groupby("store_id")["amount"].sum().reset_index()
