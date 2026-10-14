#!/usr/bin/env python3
"""Clean a messy sales CSV and produce a summary report.

Usage:
    python3 csv_report.py sample/sales.csv --out report.md --clean cleaned.csv
"""
import argparse
import csv
from collections import defaultdict
from datetime import datetime

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%d.%m.%Y")


def parse_date(text):
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def parse_amount(text):
    """Accept '1,234.50', '1.234,50', '€ 99', '  45 ' ..."""
    text = text.strip().replace("€", "").replace("$", "").replace(" ", "")
    if not text:
        return None
    if "," in text and "." in text:
        # The last separator is the decimal one
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def clean_rows(rows):
    """Return (clean_rows, rejected_count). Removes duplicates and invalid rows."""
    seen = set()
    cleaned = []
    rejected = 0
    for row in rows:
        date = parse_date(row.get("date", ""))
        amount = parse_amount(row.get("amount", ""))
        product = row.get("product", "").strip().title()
        if date is None or amount is None or not product:
            rejected += 1
            continue
        key = (date, product, amount)
        if key in seen:
            rejected += 1
            continue
        seen.add(key)
        cleaned.append({"date": date, "product": product, "amount": amount})
    return cleaned, rejected


def summarize(rows):
    by_product = defaultdict(float)
    by_month = defaultdict(float)
    for r in rows:
        by_product[r["product"]] += r["amount"]
        by_month[r["date"].strftime("%Y-%m")] += r["amount"]
    return {
        "total": sum(r["amount"] for r in rows),
        "orders": len(rows),
        "by_product": dict(sorted(by_product.items(), key=lambda kv: -kv[1])),
        "by_month": dict(sorted(by_month.items())),
    }


def render_markdown(summary, rejected):
    lines = [
        "# Sales report",
        "",
        f"- Valid orders: **{summary['orders']}**",
        f"- Rejected rows (invalid or duplicated): **{rejected}**",
        f"- Total revenue: **{summary['total']:.2f}**",
        "",
        "## Revenue by product",
        "",
        "| Product | Revenue |",
        "|---|---:|",
    ]
    lines += [f"| {p} | {v:.2f} |" for p, v in summary["by_product"].items()]
    lines += ["", "## Revenue by month", "", "| Month | Revenue |", "|---|---:|"]
    lines += [f"| {m} | {v:.2f} |" for m, v in summary["by_month"].items()]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input")
    ap.add_argument("--out", default="report.md")
    ap.add_argument("--clean", help="optional path for the cleaned CSV")
    args = ap.parse_args()

    with open(args.input, newline="", encoding="utf-8") as f:
        rows, rejected = clean_rows(csv.DictReader(f))

    if args.clean:
        with open(args.clean, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["date", "product", "amount"])
            w.writeheader()
            for r in rows:
                w.writerow({**r, "date": r["date"].isoformat(), "amount": f"{r['amount']:.2f}"})

    report = render_markdown(summarize(rows), rejected)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)


if __name__ == "__main__":
    main()
