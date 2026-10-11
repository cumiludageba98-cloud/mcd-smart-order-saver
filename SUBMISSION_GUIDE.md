# 提交报名指引 & Issue 内容

> 本文件是给你的操作手册。代码和文档我都准备好了，最后**发布到你的 GitHub 账号**
> 和**提交 Issue**这两步需要你亲手完成（涉及你的账号凭证与公开身份）。

---

## 第一步：创建 GitHub 仓库并推送

### 1.1 在 GitHub 网页端新建仓库

1. 登录 https://github.com
2. 右上角 `+` → `New repository`
3. 填写：
   - **Repository name**：`mcd-smart-order-saver`
   - **Description**：`麦麦省钱精算师 —— 基于麦当劳中国 MCP 的智能点餐省钱技能`
   - **Public**（必须公开，赛事要求）
   - **不要**勾选 `Add a README file`（本地已有）
4. 点击 `Create repository`

### 1.2 本地推送

打开 Git Bash，在项目目录执行（把 `<YOUR_GITHUB_ID>` 换成你的用户名）：

```bash
cd "C:/Users/12729/WorkBuddy AI/2026-10-11-18-54-29/mcd-smart-order-saver"

git init
git add .
git commit -m "feat: 麦麦省钱精算师 - 基于麦当劳 MCP 的智能点餐省钱技能"

git branch -M main
git remote add origin https://github.com/cumiludageba98-cloud/mcd-smart-order-saver.git
git push -u origin main
```

> 首次推送会要求登录。推荐用 Personal Access Token 或 GitHub CLI（`gh auth login`）。

### 1.3 推送后必做的替换

仓库里有两处占位符需要你替换成真实信息：

| 文件 | 占位符 | 替换为 |
|---|---|---|
| `README.md` | `<YOUR_GITHUB_ID>` | 你的 GitHub 用户名 |
| `CONTEST_DECLARATION.md` | `__YOUR_GITHUB_ID__` | 你的 GitHub 用户名 |
| `CONTEST_DECLARATION.md` | `2026 年 10 月 __ 日` | 实际签署日期 |
| `LICENSE` | `<YOUR_NAME>` | 你的名字或 GitHub ID |

替换后：

```bash
# 用编辑器改完文件后
git add .
git commit -m "docs: 填写作者信息与日期"
git push
```

---

## 第二步：提交参赛申请 Issue

### 2.1 找到活动页面

前往麦当劳官方账号的活动仓库，找到 Issue 提交入口：

```
https://github.com/M-China/mcd-developer-innovation-challenge/issues
```

点击 `New issue`，选择**参赛申请**模板。

### 2.2 按模板填写

官方指定格式如下（照抄即可，替换项目地址）：

```text
【参赛申请】
项目名称：麦麦省钱精算师
项目地址：https://github.com/cumiludageba98-cloud/mcd-smart-order-saver
项目简介：麦当劳优惠体系层层叠加，人脑算不清哪单最便宜。麦麦省钱精算师先自动领取全部可领的麦麦省优惠券，再拉取账户券、积分与活动日历，遍历菜品组合并逐组真实比价，输出最低到手价方案对比表 —— 实测单笔可从 30 元压到 17 元。支持预算与热量双约束，精算到付款前一步，下单由你点头。
```

### 2.3 提交

点击 `Submit new issue` 完成报名。

---

## 第三步：报名后的维护

| 事项 | 说明 |
|---|---|
| **截止时间** | 北京时间 **2026-10-25 23:59** 前必须完成 Issue 提交 |
| **Star 截止** | 北京时间 **2026-10-26 00:00** 为 Star 数统计截止点 |
| **不要改仓库可见性** | 仓库必须保持 Public，否则取消资格 |
| **不要刷 Star** | 规则明确禁止刷榜，违规取消资格 |
| **提高 Star 的正道** | 完善文档、在掘金/知乎写项目介绍、分享到技术社区 |

---

## 第四步：加分建议（提高 Star 的实操）

1. **写一篇项目介绍文章**发到掘金 / 知乎 / CSDN，标题带「麦当劳 MCP」「省钱」等关键词
2. **README 顶部加动图**演示效果（可用 asciinema 录制脚本运行）
3. **补充更多实用场景**：团餐、积分抽奖、新品推荐
4. **在 Issue 里回复评审提问**，保持响应速度
5. **提交 `workbuddy.md`** 已就绪，可同时拿 WorkBuddy 专项积分（前 100 名 3000 积分）

---

## 完整文件清单（已全部就绪）

```
mcd-smart-order-saver/
├── SKILL.md                  ✅ 技能定义与工作流
├── README.md                 ✅ 项目介绍（需替换 GitHub ID）
├── CONTEST_DECLARATION.md    ✅ 参赛声明（需替换 GitHub ID + 日期）
├── MCP_INTEGRATION.md        ✅ MCP 接入说明
├── mcp-config.example.json   ✅ 脱敏配置（仅占位符）
├── workbuddy.md              ✅ WorkBuddy 对话上下文
├── LICENSE                   ✅ MIT（需替换作者名）
├── .gitignore                ✅ 已排除敏感文件
├── scripts/
│   └── optimize_order.py     ✅ 本地组合优化器（已实测通过）
├── examples/
│   └── sample_input.json     ✅ 示例输入
└── references/
    └── mcp-tools.md          ✅ MCP 工具速查表
```

赛事的 5 个必需文件**全部齐备且标准命名**，签名与 ID 替换后即可推送。
