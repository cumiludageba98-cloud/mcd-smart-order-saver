#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦麦省钱精算师 —— 本地组合优化器

用途
----
当用户把「菜品价目表 + 优惠券规则」以 JSON 形式提供时，本脚本在本地穷举
组合，求解最低到手价。适用于：
  - 离线比价（不想消耗 MCP 请求额度）
  - 批量预演多套搭配方案
  - 上线前验证 MCP calculate-price 的返回是否合理

线上场景请优先使用麦当劳 MCP 的 calculate-price 工具（真实价格以服务端为准）。

输入 JSON 结构
--------------
{
  "items": [
    {"code": "BIGMAC", "name": "巨无霸", "price": 26.0, "category": "burger",
     "calories": 550, "tags": ["主食"]},
    ...
  ],
  "combos": [
    {"code": "BIGMAC_COMBO", "name": "巨无霸套餐", "price": 32.0,
     "contains": ["BIGMAC", "FRIES_M", "COLA_M"]},
    ...
  ],
  "coupons": [
    {"id": "C1", "name": "满30减8", "type": "threshold",
     "threshold": 30.0, "discount": 8.0, "applies_to": "all"},
    {"id": "C2", "name": "巨无霸立减5", "type": "item_discount",
     "item_code": "BIGMAC", "discount": 5.0, "applies_to": "BIGMAC"},
    {"id": "C3", "name": "无门槛3元", "type": "threshold",
     "threshold": 0.0, "discount": 3.0, "applies_to": "all"}
  ],
  "constraints": {
    "budget_max": 25.0,
    "calories_max": 700,
    "require_items": ["BIGMAC"],
    "quantity": 1
  }
}

用法
----
  python optimize_order.py input.json
  python optimize_order.py input.json --top 5
"""

import argparse
import itertools
import json
import sys
from typing import Any


# --------------------------------------------------------------------------
# 数据模型
# --------------------------------------------------------------------------

class Item:
    def __init__(self, raw: dict[str, Any]):
        self.code: str = raw["code"]
        self.name: str = raw.get("name", self.code)
        self.price: float = float(raw["price"])
        self.category: str = raw.get("category", "other")
        self.calories: int = int(raw.get("calories", 0) or 0)
        self.tags: list[str] = raw.get("tags", [])

    def __repr__(self) -> str:
        return f"{self.name}(¥{self.price:.1f})"


class Combo:
    def __init__(self, raw: dict[str, Any]):
        self.code: str = raw["code"]
        self.name: str = raw.get("name", self.code)
        self.price: float = float(raw["price"])
        self.contains: list[str] = raw.get("contains", [])
        self.calories: int = int(raw.get("calories", 0) or 0)

    def __repr__(self) -> str:
        return f"{self.name}(¥{self.price:.1f})"


class Coupon:
    def __init__(self, raw: dict[str, Any]):
        self.id: str = raw["id"]
        self.name: str = raw.get("name", self.id)
        self.type: str = raw.get("type", "threshold")
        self.threshold: float = float(raw.get("threshold", 0.0))
        self.discount: float = float(raw.get("discount", 0.0))
        self.item_code: str | None = raw.get("item_code")
        self.applies_to: str = raw.get("applies_to", "all")

    def __repr__(self) -> str:
        return f"{self.name}"


# --------------------------------------------------------------------------
# 计价
# --------------------------------------------------------------------------

def price_of(items: list[Item], combos: list[Combo]) -> tuple[float, str, int]:
    """朴素计价：套餐优先，其余单品按序相加。返回 (原价, 说明, 总热量)。"""
    subtotal = 0.0
    desc: list[str] = []
    calories = 0

    # 套餐：包含的菜品编码集合，用集合去重匹配单品
    used_codes: set[str] = set()
    for combo in combos:
        if not combo.contains:
            continue
        # 若套餐包含的每个单品都在所选项里（按 code 匹配，且数量足够）
        need: dict[str, int] = {}
        for c in combo.contains:
            need[c] = need.get(c, 0) + 1
        avail: dict[str, int] = {}
        for it in items:
            if it.code in used_codes:
                continue
            avail[it.code] = avail.get(it.code, 0) + 1
        if all(avail.get(c, 0) >= n for c, n in need.items()):
            subtotal += combo.price
            calories += combo.calories
            desc.append(f"{combo.name} ¥{combo.price:.1f}")
            for c in combo.contains:
                # 标记一个该单品为已用
                for it in items:
                    if it.code == c and it.code not in used_codes:
                        used_codes.add(it.code)
                        break
            continue

    for it in items:
        if it.code in used_codes:
            continue
        subtotal += it.price
        calories += it.calories
        desc.append(f"{it.name} ¥{it.price:.1f}")

    return subtotal, " + ".join(desc), calories


def apply_coupon(subtotal: float, items: list[Item], coupon: Coupon) -> float:
    """应用单张券，返回实际抵扣金额（>=0）。"""
    if coupon.type == "threshold":
        if subtotal >= coupon.threshold:
            return min(coupon.discount, subtotal)
        return 0.0
    if coupon.type == "item_discount":
        # 该券只对被点中的目标单品生效
        for it in items:
            if it.code == coupon.item_code:
                return min(coupon.discount, it.price)
        return 0.0
    return 0.0


def optimize(items_raw: list[dict], combos_raw: list[dict], coupons_raw: list[dict],
             constraints: dict, top: int = 5) -> list[dict]:
    """穷举单品子集 × 券组合，返回按到手价升序的方案列表。"""
    items_all = [Item(r) for r in items_raw]
    combos_all = [Combo(r) for r in combos_raw]
    coupons_all = [Coupon(r) for r in coupons_raw]

    budget_max = constraints.get("budget_max")
    calories_max = constraints.get("calories_max")
    require_items = set(constraints.get("require_items", []))

    results: list[dict] = []

    # 枚举单品子集（限制规模，避免组合爆炸）
    n = len(items_all)
    if n > 14:
        items_all = items_all[:14]
        n = 14

    for r in range(1, n + 1):
        for subset in itertools.combinations(items_all, r):
            codes = {it.code for it in subset}
            if require_items and not require_items.issubset(codes):
                continue

            subtotal, desc, calories = price_of(list(subset), combos_all)

            if calories_max is not None and calories > calories_max:
                continue

            # 枚举券组合（用 1~2 张，实际平台多为单券，2 张用于演示叠加）
            best_pay = subtotal
            best_coupon_desc: list[str] = []
            for k in (0, 1, 2):
                for combo_coupon in itertools.combinations(coupons_all, k):
                    pay = subtotal
                    ok = True
                    used_names: list[str] = []
                    for cp in combo_coupon:
                        d = apply_coupon(subtotal, list(subset), cp)
                        if d <= 0:
                            # 券不适用则跳过这个组合
                            if cp.type == "threshold" and subtotal < cp.threshold:
                                ok = False
                                break
                            if cp.type == "item_discount" and cp.item_code not in codes:
                                ok = False
                                break
                            continue
                        pay -= d
                        used_names.append(cp.name)
                    if not ok:
                        continue
                    if pay < best_pay:
                        best_pay = pay
                        best_coupon_desc = used_names

            if budget_max is not None and best_pay > budget_max:
                continue

            results.append({
                "items": [it.name for it in subset],
                "desc": desc,
                "subtotal": round(subtotal, 2),
                "pay": round(best_pay, 2),
                "saved": round(subtotal - best_pay, 2),
                "coupons": best_coupon_desc,
                "calories": calories,
            })

    # 去重（相同 desc 保留最低价）
    seen: dict[str, dict] = {}
    for row in results:
        key = row["desc"]
        if key not in seen or row["pay"] < seen[key]["pay"]:
            seen[key] = row

    ranked = sorted(seen.values(), key=lambda x: (x["pay"], -x["saved"]))
    return ranked[:top]


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="麦麦省钱精算师 —— 本地组合优化器")
    parser.add_argument("input", help="输入 JSON 文件路径")
    parser.add_argument("--top", type=int, default=5, help="输出方案数量（默认 5）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[错误] 找不到文件：{args.input}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"[错误] JSON 解析失败：{e}", file=sys.stderr)
        return 1

    plans = optimize(
        data.get("items", []),
        data.get("combos", []),
        data.get("coupons", []),
        data.get("constraints", {}),
        top=args.top,
    )

    if not plans:
        print("没有符合条件的方案，请放宽预算或热量约束。")
        return 0

    if args.json:
        print(json.dumps(plans, ensure_ascii=False, indent=2))
        return 0

    print(f"\n{'=' * 62}")
    print(f"  麦麦省钱精算师 · 最低到手价方案 Top {len(plans)}")
    print(f"{'=' * 62}\n")
    for i, p in enumerate(plans, 1):
        coupon_txt = "（" + "、".join(p["coupons"]) + "）" if p["coupons"] else ""
        print(f"  {i}. 到手 ¥{p['pay']:.2f}   省 ¥{p['saved']:.2f}   "
              f"[原价 ¥{p['subtotal']:.2f}] {p['calories']} kcal")
        print(f"     └ {p['desc']}{coupon_txt}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
