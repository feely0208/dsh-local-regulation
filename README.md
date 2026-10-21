# @deepwhale-cn/dsh-local-regulation

[![dshfind 收录](https://dshfind.com/api/badge/feely0208/dsh-local-regulation?lang=zh)](https://dshfind.com/zh/plugins/feely0208/dsh-local-regulation)

[![Listed on dsh-plugin.org](https://dsh-plugin.org/badges/listed.svg)](https://dsh-plugin.org/zh/plugins/feely0208/dsh-local-regulation)

**国家法之外还有一层：上海、深圳两市自己的数据条例。装它，在交付前知道这一层有没有被漏掉。**

**关键词**：上海数据条例 · 深圳经济特区数据条例 · 地方数据条例 · 数据合规检查 · 人脸识别显著标识 · 去标识化 · 用户画像 · 数据销毁规程 · 数据安全责任人 · 对外数据接口安全

---

## ⚠️ 适用范围需人工确认（先读这段）

**本插件只覆盖上海、深圳两市条例；是否适用取决于实际运营地，需人工确认。**

- 插件**不判断、也不猜测**你的实际运营地 —— 这是你的法务/合规同事才能确认的事；
- 其他城市（北京、广东、浙江等）另有地方规则，不在本插件覆盖范围内；
- 报告**头部和页脚**都会重复这条提示，避免把「上海/深圳的额外要求」误当成全国通用要求。

---

## 先说清楚它是什么、不是什么

**是**：把《上海市数据条例》和《深圳经济特区数据条例》里**可以静态检测**的那几条额外要求，
落成 7 条判据，扫一遍代码库告诉你「这一层可能漏了什么」：
人脸采集场所的显著标识与替代验证、对外提供个人数据前的去标识化、用户画像的明示与拒绝途径、
敏感数据的安全管理责任人、数据来源与处理记录、共享开放与对外接口制度、数据销毁规程。

**不是**：
- ❌ **不是国家法的全覆盖** —— 个人信息保护法、数据安全法的常规项各有专门插件，这里只补「地方多出来的那层」
- ❌ **不是法律意见** —— 命中的是「值得人工确认的点」，不是「你违法了」
- ❌ **不判断运营地** —— 它不知道你的业务实际落在哪，也不该猜
- ❌ **不做动态检测** —— 只读仓库里的代码与文档；线下标识、内部制度、真实审批记录它都看不到
- ❌ **不承诺「保证通过」「绝对合规」** —— 静态检查只能降低漏项概率

**一句话分界**：**国家法管全国，它只管上海、深圳多出来的那一层。**

---

## 它查什么（7 条）

| 规则 | 查什么 | 级别 |
|---|---|---|
| `LR-SH-23` | 人脸识别 / 图像采集场所：找不到显著标识与非唯一验证方式的说明（上海第二十三条）| 🟡 |
| `LR-SZ-26` | 对外提供个人数据：找不到去标识化处理（深圳第二十六条）| 🔴 |
| `LR-SZ-29` | 用户画像 / 个性化推荐：找不到用途、规则与拒绝途径（深圳第二十九条）| 🟡 |
| `LR-SZ-73` | 处理敏感个人数据 / 重要数据：找不到安全管理机构与责任人（深圳第七十三条）| 🔴 |
| `LR-SZ-75` | 数据处理全流程记录与来源合法性（深圳第七十五条）| 🟡 |
| `LR-SZ-79` | 数据共享开放与对外接口：找不到安全管理制度（深圳第七十九条）| 🟡 |
| `LR-SZ-80` | 数据销毁规程（深圳第八十条）| 🟡 |

**每条都会给出：哪个文件、什么证据、依据是哪一条、建议怎么确认。**
其中「找不到某说明」的判据是**项目级 absence**：位置显示为 `**/*` 表示全项目都没找到，
证据里会写明实际检查了多少个文件。

### 判据的触发条件（先用 `when` 限定场景，避免误报）

| 规则 | 只在项目具备这些特征时才跑 |
|---|---|
| `LR-SH-23` | 依赖含 `face-api` / `arcsoft` / `baidu-aip` / `insightface` / `seetaface` / `facenet`，或代码含 `FaceEngine` / `detectFace` / `faceVerify` / `compareFace` |
| `LR-SZ-26` | 同一文件里同时出现导出动作（`to_csv` / `to_excel` / `dumpdata` / `SELECT * FROM` / `/export` / `/batch`）与个人字段（身份证 / 手机号等）|
| `LR-SZ-29` | 出现 `user_profile` / `用户画像` / `标签体系` / `recommend` / `协同过滤`，或依赖 `surprise` / `implicit` / `lightfm` |
| `LR-SZ-73` | schema / 模型 / 建表 SQL 含身份证、银行卡、生物特征、人脸、病历、行踪等字段 |
| `LR-SZ-75` | 出现抓取、请求接口、读库、读文件动作（`scrapy` / `requests.get` / `pd.read_` / `jdbc` / `read_csv` 等）|
| `LR-SZ-79` | 出现 REST / GraphQL / webhook / OpenAPI 接口并返回用户或业务字段 |
| `LR-SZ-80` | 出现 `DELETE FROM` / `drop table` / `purge` / `destroy` / `shred` / 硬删除 / 物理删除 |

不满足触发条件的规则会进入报告的「因不适用本项目未运行」列表，
**不会**假装检查过 —— 这是防「假绿」的硬要求。

### 出处

- 《上海市数据条例》（2021-11-25 通过，2022-01-01 施行）第二十三条
- 《深圳经济特区数据条例》（2021-06-29 通过，2022-01-01 施行）第二十六条、第二十九条、
  第七十三条、第七十五条、第七十九条、第八十条

判据逐条对照见 `docs/规则依据.md`；适用范围的人工确认流程见 `docs/适用范围.md`。

---

## 安装

```bash
dsh plugin --profile web add @deepwhale-cn/dsh-local-regulation
```

## 用法

```bash
# 检查当前项目
dsh-local-regulation

# 检查指定目录
dsh-local-regulation --root /path/to/project

# 看内置演示（一个「上海/深圳在营、各种地方要求都没落地」的样本项目）
dsh-local-regulation --demo

# 列出 7 条判据与出处
dsh-local-regulation --list-rules

# 出 HTML 报告（可截图存档）
dsh-local-regulation --root /path/to/project --html local-regulation.html

# 给 CI 用：有 high 命中时退出码 1
dsh-local-regulation --root . --quiet
```

> 在 DSH 会话里也可以直接说：「按上海、深圳的数据条例查一下这个项目」，
> 配套 skill 会调用同一个 CLI。

---

## 一个真实的例子

`--demo` 的样本项目叫「星链会员平台」，看起来很正常：TypeScript 前端、FastAPI 后端、
有隐私政策、有数据库表结构、有 ETL 脚本。它在 README 里明确写了运营地在上海、深圳。
但它把这些地方要求都漏了：

```
src/face/verify.ts        用人脸核验开门，没有标识与替代通行方式的说明
api/partner_export.py     把手机号、身份证号批量导出给合作方，没有去标识化
rec/user_profile.py       做用户画像与推荐，隐私政策里没有画像说明和关闭入口
db/schema.sql             有 id_card / face_id，没有数据安全管理责任人
etl/collect.py            抓取并读入订单数据，没有来源与处理记录
api/open.py               对外接口直接返回 phone，没有共享开放与接口制度
scripts/purge.sql         硬删除三个月前的数据，没有数据销毁规程
```

工具会把这些一条条拎出来：

```
深鲸守护 · 地方数据条例检查（仅上海 / 深圳）· 适用范围需人工确认 v0.1.0
  检查规则   7/7 条
  命中       7 条

【高】2 条
  · 对外提供个人数据：去标识化处理
  · 处理敏感个人数据 / 重要数据：数据安全管理机构与责任人的设置

【中】5 条
  · 人脸识别 / 图像采集场所：显著标识与非唯一验证方式的说明
  · 用户画像 / 个性化推荐：明示用途、主要规则与拒绝途径
  · 数据处理全流程记录与数据来源合法性
  · 数据共享开放与对外接口：安全管理制度
  · 数据销毁规程
```

反例 `clean-project` 是同结构的整改后项目：有 `docs/数据安全管理制度.md`、`docs/数据来源与处理记录.md`、
`docs/人脸识别合规说明.md`，导出前调用 `utils/mask.py`，本人导出路由用 `/me/export`，
**7 条全部不报** —— 用来防止规则把合规写法也当成问题。

---

## 边界（这些情况它管不了）

- **地域适用性** —— 只覆盖上海、深圳；运营地不在两市时，本插件的命中与你无关，需人工确认
- **线下与制度** —— 显著标识贴没贴、内部制度有没有、责任人是否真在履职，静态扫描看不到
- **「找到关键词」不等于「做到」** —— 判据是文本存在性检查，文档里写了关键词但实际没执行，它发现不了
- **反过来，「没找到关键词」也不等于「没做」** —— 说明可能在线下物料、内部知识库、工单系统里
- **不覆盖国家法常规项** —— 个人信息保护影响评估、单独同意、跨境、等保等各有专门插件
- **扫描盲区** —— `node_modules` / `dist` / `build` 等目录默认跳过；文档若只存在于这些目录会漏看
- **测试/示例字段** —— 敏感字段如果只出现在 `tests/fixtures` 或示例文档里，也可能触发对应规则，需人工判断

---

## 开发

```bash
bash tests/run.sh        # 双向验证：7 条逐条报出 + 反例 0 命中 + 溯源 + 适用范围提示
node bin/cli.mjs --demo  # 内置样本演示
```

样本目录（同时是 `--demo` 的数据源，没有第二套）：

```
tests/fixtures/fail/demo-project/     正例：上海/深圳在营、7 条地方要求全漏
tests/fixtures/pass/clean-project/    反例：同结构 + 制度文档 + 脱敏工具 + 本人导出边界
```

---

## 深鲸网安守护系列（共 39 个）

> 一个插件做一件事。**安全问题是链式的** —— 配套用才完整。

**国内合规**（12）｜ [等保对照](https://github.com/feely0208/dsh-cn-mlps) · [日志留存](https://github.com/feely0208/dsh-cn-log-retention) · [备案公示](https://github.com/feely0208/dsh-cn-filing) · [用户同意](https://github.com/feely0208/dsh-consent-guard) · [个人信息权利](https://github.com/feely0208/dsh-data-rights) · [未成年人保护](https://github.com/feely0208/dsh-minor-guard) · [影响评估](https://github.com/feely0208/dsh-pipia) · [数据分类分级](https://github.com/feely0208/dsh-data-classify) · [算法备案](https://github.com/feely0208/dsh-algorithm-filing) · [数据出境](https://github.com/feely0208/dsh-cn-data-export) · [国密合规](https://github.com/feely0208/dsh-cn-crypto) · [AI 内容标识](https://github.com/feely0208/dsh-cn-ai-labeling)

**AI 与 Agent 治理**（6）｜ [AI 输出信任](https://github.com/feely0208/dsh-ai-output-trust) · [外部内容信任](https://github.com/feely0208/dsh-content-trust) · [MCP 安全](https://github.com/feely0208/dsh-mcp-audit) · [Agent 权限](https://github.com/feely0208/dsh-agent-scope) · [策略核对](https://github.com/feely0208/dsh-agent-policy) · [可疑指令](https://github.com/feely0208/dsh-phishing-guard)

**数据与凭据**（5）｜ [敏感数据](https://github.com/feely0208/dsh-data-scan) · [密钥轮换](https://github.com/feely0208/dsh-key-rotate) · [数据留存](https://github.com/feely0208/dsh-data-lifecycle) · [配置审计](https://github.com/feely0208/dsh-env-audit) · [密钥扫描](https://github.com/feely0208/dsh-secret-scan)

**供应链与构建**（5）｜ [开源许可](https://github.com/feely0208/dsh-license-guard) · [依赖投毒](https://github.com/feely0208/dsh-dep-audit) · [CI 安全](https://github.com/feely0208/dsh-ci-guard) · [工具审查](https://github.com/feely0208/dsh-tool-vet) · [物料清单](https://github.com/feely0208/dsh-sbom)

**权限与应急**（3）｜ [最小权限](https://github.com/feely0208/dsh-least-privilege) · [告警外发](https://github.com/feely0208/dsh-alert-relay) · [应急证据包](https://github.com/feely0208/dsh-incident-package)

**行业专项**（4）｜ [医疗行业专项](https://github.com/feely0208/dsh-industry-medical) · [教育行业专项](https://github.com/feely0208/dsh-industry-education) · [金融行业专项](https://github.com/feely0208/dsh-industry-finance) · [地方数据条例](https://github.com/feely0208/dsh-local-regulation)

**编排与交付**（4）｜ [一键体检](https://github.com/feely0208/dsh-guard-suite) · [改前改后复核](https://github.com/feely0208/dsh-fix-verify) · [合规可交付文档](https://github.com/feely0208/dsh-compliance-doc) · [整改建议](https://github.com/feely0208/dsh-remediation)

都在 DSH 插件市场（dsh-plugin.org）、npm 和 deepwhale.org.cn/guard.html 上。

## License

MIT © 深鲸 DeepWhale

---

<p align="right"><a href="https://deepwhale.org.cn"><img src="https://www.deepwhale.org.cn/images/badge/deepwhale-badge.png" alt="powered by dwh" height="20"></a></p>
