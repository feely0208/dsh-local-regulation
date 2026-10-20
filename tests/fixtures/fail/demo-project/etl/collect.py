import pandas as pd
import requests

FEED_URL = "https://feeds.example.com/orders.csv"
LOCAL_FILE = "data/orders.csv"


def pull_orders():
    """从合作方数据接口下载订单明细。"""
    resp = requests.get(FEED_URL, timeout=10)
    resp.raise_for_status()
    with open(LOCAL_FILE, "wb") as fh:
        fh.write(resp.content)
    return pd.read_csv(LOCAL_FILE)


def summarise():
    df = pull_orders()
    return df.groupby("store_id")["amount"].sum().reset_index()
