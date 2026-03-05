#!/usr/bin/env python3
"""
Build weekly inference-tech heat dashboard from local GitHub scan snapshots.

Input snapshots: reports/github_pr_scan_raw_YYYY-MM-DD.json
Generated:
  - reports/inference_heat_dashboard.md
  - reports/inference_heat_dashboard_weekly.csv
"""

from __future__ import annotations

import csv
import datetime as dt
import glob
import json
import os
import re
from collections import defaultdict

PERF_PAT = re.compile(
    r"\b(inference|latency|throughput|kv\s*cache|speculative|quant|kernel|flash|scheduler|prefill|decode|tp|pp|moe|fp8|int4|int8)\b",
    re.I,
)
FEATURE_PAT = re.compile(r"\b(add|support|implement|enable|introduce|new)\b", re.I)
FIX_PAT = re.compile(r"\b(fix|bug|regression|crash|leak|stability|correctness|hotfix)\b", re.I)


def week_key(date_str: str) -> str:
    d = dt.date.fromisoformat(date_str)
    s = d - dt.timedelta(days=d.weekday())
    e = s + dt.timedelta(days=6)
    return f"{s.isoformat()} ~ {e.isoformat()}"


def score(total: int, perf: int, feat: int, fix: int) -> float:
    if total == 0:
        return 0.0
    perf_ratio = perf / total
    feat_ratio = feat / total
    fix_ratio = fix / total
    val = 45 * min(total / 50, 1) + 35 * perf_ratio + 20 * feat_ratio - 10 * fix_ratio
    return round(max(0.0, min(val, 100.0)), 2)


def level(s: float) -> str:
    if s >= 70:
        return "高热"
    if s >= 45:
        return "中热"
    return "平稳"


def main() -> None:
    root = os.path.dirname(os.path.dirname(__file__))
    reports = os.path.join(root, "reports")
    os.makedirs(reports, exist_ok=True)

    files = sorted(glob.glob(os.path.join(reports, "github_pr_scan_raw_*.json")))
    if not files:
        raise SystemExit("No snapshot found: reports/github_pr_scan_raw_*.json")

    bucket = defaultdict(lambda: {"total": 0, "perf": 0, "feature": 0, "fix": 0})

    for fp in files:
        data = json.load(open(fp, "r", encoding="utf-8"))
        day = data.get("generated_at", "")[:10]
        wk = week_key(day)
        for pr in data.get("top", []):
            text = f"{pr.get('title', '')} {pr.get('body', '')}"
            bucket[wk]["total"] += 1
            bucket[wk]["perf"] += 1 if PERF_PAT.search(text) else 0
            bucket[wk]["feature"] += 1 if FEATURE_PAT.search(text) else 0
            bucket[wk]["fix"] += 1 if FIX_PAT.search(text) else 0

    rows = []
    for wk in sorted(bucket.keys()):
        b = bucket[wk]
        s = score(b["total"], b["perf"], b["feature"], b["fix"])
        rows.append(
            {
                "week": wk,
                "sample_pr": b["total"],
                "perf_related_pr": b["perf"],
                "feature_pr": b["feature"],
                "fix_pr": b["fix"],
                "heat_score": s,
                "level": level(s),
            }
        )

    csv_path = os.path.join(reports, "inference_heat_dashboard_weekly.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "week",
                "sample_pr",
                "perf_related_pr",
                "feature_pr",
                "fix_pr",
                "heat_score",
                "level",
            ],
        )
        w.writeheader()
        w.writerows(rows)

    md_path = os.path.join(reports, "inference_heat_dashboard.md")
    lines = [
        "# 推理技术热度周度仪表盘",
        "",
        f"- 生成时间：{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "- 数据来源：本仓库内 `reports/github_pr_scan_raw_*.json` 快照",
        "- 注意：当前是第一版样本仪表盘，随周报快照累积会变得稳定。",
        "",
        "## 指标说明",
        "- sample_pr：当周纳入样本的重点PR数量",
        "- perf_related_pr：命中推理性能关键词的PR",
        "- feature_pr：命中新功能关键词的PR",
        "- fix_pr：命中修复关键词的PR",
        "- heat_score：0~100 启发式热度分",
        "",
        "## 周度数据",
        "",
        "| 周期 | 样本PR | 推理相关 | 新功能 | 修复 | 热度分 | 级别 |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['week']} | {r['sample_pr']} | {r['perf_related_pr']} | {r['feature_pr']} | {r['fix_pr']} | {r['heat_score']} | {r['level']} |"
        )

    if rows:
        cur = rows[-1]
        lines += [
            "",
            "## 本周结论",
            f"- 当前热度：**{cur['heat_score']}（{cur['level']}）**。",
            "- 解读建议：不要只看PR数量，重点看“推理相关占比 + 新功能占比 + 修复占比”三者组合。",
        ]

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(md_path)
    print(csv_path)


if __name__ == "__main__":
    main()
