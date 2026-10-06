#!/usr/bin/env python3
"""Fetch public GitHub contribution-calendar HTML and derive daily stats."""
from collections import defaultdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "eduardoruisjbv")
URL = f"https://github.com/users/{USERNAME}/contributions"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"


def fetch_days():
    response = requests.get(URL, headers={"User-Agent": "profile-readme-art/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        raise RuntimeError("GitHub contribution-calendar markup changed; no day cells were found")
    days = []
    for cell in cells:
        date = cell.get("data-date")
        if not date:
            continue
        tooltip = soup.find("tool-tip", attrs={"for": cell.get("id")}) if cell.get("id") else None
        text = tooltip.get_text(" ", strip=True) if tooltip else cell.get("aria-label", "")
        match = re.search(r"(\d[\d,]*)\s+contribution", text, re.I)
        count = int(match.group(1).replace(",", "")) if match else 0
        days.append({"date": date, "count": count, "level": int(cell.get("data-level") or 0)})
    days.sort(key=lambda day: day["date"])
    if len(days) < 350:
        raise RuntimeError(f"Expected a full contribution year, received only {len(days)} days")
    return days


def streaks(days):
    current_days = days[:-1] if days and days[-1]["count"] == 0 else days
    current = 0
    for day in reversed(current_days):
        if not day["count"]:
            break
        current += 1
    longest = run = 0
    for day in days:
        run = run + 1 if day["count"] else 0
        longest = max(longest, run)
    return current, longest


def main():
    days = fetch_days()
    monthly = defaultdict(int)
    for day in days:
        monthly[day["date"][:7]] += day["count"]
    current, longest = streaks(days)
    best = max(days, key=lambda day: day["count"])
    total = sum(day["count"] for day in days)
    active = sum(day["count"] > 0 for day in days)
    data = {
        "username": USERNAME,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active,
        "avg_per_active_day": round(total / active, 1) if active else 0,
        "current_streak": {"length": current},
        "longest_streak": {"length": longest},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": [{"month": month, "total": count} for month, count in sorted(monthly.items())],
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {total:,} contributions; current streak {current}; longest {longest}")


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        print(f"could not refresh contribution data: {exc}", file=sys.stderr)
        sys.exit(1)
