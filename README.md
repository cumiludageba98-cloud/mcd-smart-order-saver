# 麦麦省钱精算师（MCD Smart Order Saver）

> 基于麦当劳中国 MCP 的智能点餐省钱技能 —— 让每一次点餐都自动落到最低到手价。

[![MCP](https://img.shields.io/badge/MCP-McDonald's%20China-e4322b)](https://open.mcd.cn/mcp)
[![WorkBuddy](https://img.shields.io/badge/Built%20with-WorkBuddy-0052d9)](https://www.workbuddy.cn)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

---

## 一、项目简介

麦当劳的优惠体系是**多层的**：单品价、套餐价、门店券、麦麦省领券、积分抵扣、麦麦商城兑换、限时活动日历……人脑几乎不可能同时算清"这一单怎么搭最便宜"。

**麦麦省钱精算师**把这件事交给 AI。

你只需要说一句「我想吃巨无霸，25 块以内，别超过 700 大卡」，它会自动：

1. 领取你当前所有可领的麦麦省优惠券
2. 拉取你账户下的全部可用券、积分余额、本月活动日历
3. 查询门店在售菜单、套餐组成、可替换项
4. **穷举组合 + 逐组真实计价**，算出最低到手价方案
5. 用对比表告诉你：推荐哪个方案、省了多少钱、用了哪张券

### 它解决的核心痛点

| 痛点 | 传统做法 | 本技能 |
|---|---|---|
| 券太多不知道用哪张 | 挨个试，或干脆不用 | 自动组合遍历取最优 |
| 套餐 vs 单品哪个便宜 | 靠感觉猜 | `calculate-price` 真实比价 |
| 差几块够满减 | 想不到 | 自动检测临界点，推荐凑单 |
| 积分花在哪最值 | 随手抵了 | 对比"抵现"与"商城兑换" |
| 限时活动错过 | 不知道有 | 活动日历主动提醒 |

---

## 二、目标用户

- **价格敏感型消费者**：日常点麦当劳，希望每一单都花在刀刃上
- **减脂/健身人群**：既要控制热量，又要省钱
- **企业团餐采购**：多人点餐场景下的整体费用优化
- **开发者**：想学习如何用 MCP 工具链编排一个真实业务工作流

---

## 三、安装方法

### 3.1 前置条件

- 一个麦当劳中国 MCP Token（[申请地址](https://open.mcd.cn/mcp)，手机号验证登录后即可获取）
- 一个支持 MCP 的客户端（WorkBuddy / Cherry Studio / Cursor / Trae / Kiro / VSCode）

### 3.2 配置 MCP Server

公开配置仅使用 `${MCD_MCP_TOKEN}` 环境变量占位符。请在客户端本地配置令牌，勿将真实令牌提交至仓库；如果客户端不支持环境变量展开，请仅在本地私有配置中填入真实值：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer ${MCD_MCP_TOKEN}"
      }
    }
  }
}
```

> 完整脱敏示例见 [`mcp-config.example.json`](./mcp-config.example.json)。

### 3.3 安装本技能

**方式一：WorkBuddy 用户（推荐）**

将本仓库克隆到 WorkBuddy 的 skills 目录：

```bash
git clone https://github.com/cumiludageba98-cloud/mcd-smart-order-saver.git \
  ~/.workbuddy-ai/skills/mcd-smart-order-saver
```

**方式二：其他 MCP 客户端**

把 `SKILL.md` 作为系统提示/技能描述加载，`scripts/optimize_order.py` 用于本地离线复算。

### 3.4 本地脚本依赖

`scripts/optimize_order.py` 仅依赖 Python 3.8+ 标准库，**无需安装任何第三方包**：

```bash
python scripts/optimize_order.py examples/sample_input.json
```

---

## 四、使用示例

### 示例 1：基础省钱点餐（**真实联调实测**）

> **用户**：我在上海人民广场附近，想吃早餐，帮我看看有什么划算的。

**技能执行**（全部为真实 MCP 调用）：
1. `now-time-info` → 服务端返回 `2026-10-11 18:04:44`
2. `campaign-calendar` → 命中真实活动：**9.9 元早餐两件套**（10月8日–10月21日，周一至周五）
3. `auto-bind-coupons` → 服务端返回 `706190 系统检测您的账号环境存在异常，暂无法领券`（风控拦截，如实呈现）
4. `query-my-coupons` → 真实券：**新人专享-中杯美式 7 折**
5. `query-my-account` → 积分账户真实返回
6. `query-nearby-stores` → 真实门店：**麦当劳上海黄浦华旭国际大厦餐厅**（storeCode `1450713`，西藏中路336号，距离 144m）
7. `query-meals` → 真实菜单，15 个分类、菜品编码齐全
8. `calculate-price` ×N → 逐组真实计价（返回单位为分）

**真实计价输出**：

```
A_单品    原价 ¥27.90  折扣 ¥0.00  应付 ¥27.90
    - 枫糖风味厚松饼猪柳蛋堡三件套 x 1  ¥27.90
B_双份    原价 ¥55.80  折扣 ¥0.00  应付 ¥55.80
    - 枫糖风味厚松饼猪柳蛋堡三件套 x 2  ¥55.80
C_加购    原价 ¥67.80  折扣 ¥0.00  应付 ¥67.80
    - 枫糖风味厚松饼猪柳蛋堡三件套 x 1  ¥27.90
    - 麦当劳联名复古棒球帽 x 1          ¥39.90
```

> **真实联调的关键发现**：`521954` 实际是「麦当劳联名复古棒球帽」而非预想的甜筒 ——
> 这正是必须真实调用 MCP 的原因：菜品编码无法靠猜，价格与优惠必须以服务端返回为准。

### 示例 2：积分怎么花最值

> **用户**：我有 3000 积分，是抵现还是换个东西？

**技能执行**：`query-my-account` → `mall-points-products` → `mall-product-detail` → 对比积分抵现率与商城商品价值，给出建议。

### 示例 3：多人团餐

> **用户**：公司 8 个人团餐，人均 30 以内，帮我配。

**技能执行**：`query-meal-assistance` → `query-meals` → 组合遍历 → 输出整单方案与人均价格。

### 示例 4：本地离线复算

> ⚠️ 以下为**模拟数据**的离线算法验证，不代表真实门店价格；真实价格请以 MCP `calculate-price` 返回为准。

```bash
python scripts/optimize_order.py examples/sample_input.json --top 5
```

输出（实测）：

```
  1. 到手 ¥17.00   省 ¥13.00   [原价 ¥30.00] 750 kcal
     └ 巨无霸 ¥26.0 + 甜筒 ¥4.0（满30减8、巨无霸立减5）
  2. 到手 ¥18.00   省 ¥8.00    [原价 ¥26.00] 550 kcal
     └ 巨无霸 ¥26.0（巨无霸立减5、无门槛3元）
  ...
```

---

## 当前验证边界

- 已验证服务握手、工具发现、活动/门店/菜单查询及价格计算；没有创建真实订单、支付、兑换积分或验证完整下单链路。
- 自动领券实测返回业务错误码 `706190`，不能宣称已经成功领券；遇到平台风控应停止重试、说明原因。
- 未验证优惠券叠加与积分抵现规则。线上价格须由 `calculate-price` 核验，离线脚本的模拟叠券结果不可作为购买依据。
- 本地算法仅为有限候选集合的演示，不保证全菜单全局最优；营养缺失、重复数量、券互斥等情况需继续完善。
- 官方要求 `CONTEST_DECLARATION.md` 使用官方原文且内容不可修改；作者署名保留在 `LICENSE`（2026 启脾丸）。

## 五、项目结构

```
mcd-smart-order-saver/
├── SKILL.md                  # 技能定义与工作流（核心）
├── README.md                 # 本文件
├── CONTEST_DECLARATION.md    # 参赛声明（原创性/合规性/敏感信息）
├── MCP_INTEGRATION.md        # MCP 接入说明（Server/Tool/调用流程/业务价值）
├── mcp-config.example.json   # 脱敏 MCP 配置示例
├── workbuddy.md              # WorkBuddy 对话上下文
├── LICENSE                   # MIT
├── scripts/
│   └── optimize_order.py     # 本地组合优化器
├── examples/
│   └── sample_input.json     # 示例输入
└── references/
    └── mcp-tools.md          # MCP 工具速查表
```

---

## 六、设计原则

- **先领券再算钱** —— 任何一次点餐都先执行 `auto-bind-coupons`，领券零成本
- **用事实说话** —— 所有价格结论必须来自 `calculate-price` 真实返回，不做估算
- **不替用户下单** —— 精算到付款前一步，下单必须用户明确确认
- **隐私优先** —— 地址、手机号等敏感信息仅用于当次调用，不落盘

---

## 七、常见问题

**Q：没有 MCP Token 能用吗？**
A：可以先跑 `scripts/optimize_order.py` 做本地离线比价，但真实价格与券以服务端为准，建议申请 Token。

**Q：请求频率有限制吗？**
A：每个 Token 每分钟最多 600 次请求，超限返回 429。本技能在组合遍历时会控制调用间隔。

**Q：会泄露我的地址和手机号吗？**
A：不会。敏感信息仅传给麦当劳 MCP 服务本身，本技能不落盘、不外传。

---

## 八、License

[MIT](./LICENSE)

本项目为「麦当劳程序员创意开发大赛」参赛作品。麦当劳相关商标、服务归金拱门（中国）有限公司所有，本项目不构成任何官方背书。
