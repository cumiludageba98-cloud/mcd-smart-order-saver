# 麦当劳中国 MCP Tool 速查表

> 数据来源：https://github.com/M-China/mcd-mcp-server （官方仓库）
> 整理时间：2026-10

接入信息：

- 地址：`https://mcp.mcd.cn`
- 协议：Streamable HTTP
- 认证：`Authorization: Bearer <MCP_TOKEN>`
- 限流：600 次/分钟

---

## 点餐相关

| Tool | 说明 |
|---|---|
| `query-meals` | 查询当前可售卖餐品列表（分类、餐品编码、标签） |
| `query-meal-detail` | 查询餐品详情（套餐组成、可替换选项） |
| `calculate-price` | 商品价格计算（含优惠券，返回金额/配送费/优惠/应付总价） |
| `create-order` | 创建订单，返回订单详情与支付链接 |
| `cancel-order` | 取消点餐订单 |
| `query-order` | 查询订单状态、内容、配送信息 |
| `order-list` | 查询近期到店/外送历史订单 |

## 门店与配送

| Tool | 说明 |
|---|---|
| `delivery-query-addresses` | 查询用户已创建的配送地址列表 |
| `delivery-create-address` | 新增配送地址 |
| `delivery-query-stores` | 外送场景下查询收货地址附近可配送门店 |
| `query-nearby-stores` | 查询用户指定地址附近的麦当劳餐厅 |
| `query-meal-assistance` | 企业团餐场景查询门店支持的助餐服务 |

## 优惠券与积分

| Tool | 说明 |
|---|---|
| `query-store-coupons` | 查询当前门店下可用优惠券列表 |
| `available-coupons` | 麦麦省券列表查询 |
| `auto-bind-coupons` | 麦麦省一键领券（自动领取全部可领券） |
| `query-my-coupons` | 查询账户下所有可用优惠券 |
| `query-my-account` | 查询积分账户（可用/累计/冻结/即将过期） |

## 营养与活动

| Tool | 说明 |
|---|---|
| `list-nutrition-foods` | 餐品营养信息（能量、蛋白质、脂肪、碳水、钠、钙） |
| `campaign-calendar` | 活动日历查询（进行中/往期/未来活动） |
| `now-time-info` | 获取当前完整时间信息 |

## 麦麦商城

| Tool | 说明 |
|---|---|
| `mall-points-products` | 查询商城商品列表（积分兑换或现金购买） |
| `mall-product-detail` | 查询商城商品详情 |
| `mall-create-order` | 积分兑换商品下单 |
| `mall-order-list` | 商城订单查询（近一年） |
| `mall-order-detail` | 商城订单详情查询 |

## 积分抽奖

| Tool | 说明 |
|---|---|
| `query-lottery-info` | 查看积分抽奖活动信息 |
| `draw-lottery` | 执行一次积分抽奖 |
| `query-my-prizes` | 查看我的奖品记录 |

## 主题活动（派对/品鉴会）

| Tool | 说明 |
|---|---|
| `query-party-city` | 主题活动城市列表 |
| `query-party-store` | 指定城市下的活动门店 |
| `query-partystore-date` | 指定门店可预约日期 |
| `query-partystore-session` | 指定日期可预约场次 |
| `party-order-create` | 主题活动订单创建 |

---

## 错误码

| code | 原因 | 处理 |
|---|---|---|
| 401 | Token 无效/过期/未提供 | 检查 Authorization 头与 Token 配置 |
| 429 | 触发限流（>600 次/分钟） | 降低请求频率 |

---

## 版本参考

| 版本 | 日期 | 新增 |
|---|---|---|
| 1.0.0 | 2025-12-09 | 麦麦日历、麦麦省领券 |
| 1.0.1 | 2026-01-23 | 餐品营养信息 |
| 1.0.2 | 2026-02-13 | 麦乐送点餐、积分兑换券 |
| 1.0.3 | 2026-04-02 | 到店取餐、团餐 |
| 1.0.4 | 2026-05-21 | 积分兑换实物、商城订单、得来速、预约 |
| 1.0.5 | 2026-06-16 | 套餐换品、餐品特制 |
| 1.0.6 | 2026-07-16 | 历史订单、优惠价展示、麦金卡/早餐卡 |
| 1.0.7 | 2026-07-29 | 派对、品鉴会主题活动 |
| 1.0.8 | 2026-08-27 | 积分抽奖 |
| 1.0.9 | 2026-09-10 | 取消订单、餐具选择、订单备注、取餐柜二维码 |
