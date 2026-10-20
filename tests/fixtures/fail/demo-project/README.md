# 星链会员平台

面向连锁门店的会员管理服务：注册、积分、订单查询和门店通行。

- 前端：TypeScript + Vite，门店闸机使用 face-api.js 做人脸核验
- 后端：FastAPI + pandas，会员数据存放在自建 MySQL
- **运营地：上海、深圳**

## 快速开始

```bash
npm install
npm run dev
pip install -r requirements.txt
uvicorn api.open:app --port 8080
```

## 目录结构

```
src/face/        门店闸机的人脸核验
db/              数据库表结构
api/             对外的 HTTP 接口
rec/             会员推荐
etl/             订单数据采集
scripts/         日常运维脚本
```

## 隐私与合规

个人信息处理说明见 `PRIVACY.md`。线下门店的告知物料由运营团队维护。
