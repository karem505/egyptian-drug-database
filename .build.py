#!/usr/bin/env python3
"""Build the published dataset from the working translit CSV.

Drops:
  - placeholder rows whose English trade name is empty / digits-only / under 2 chars
  - the internal sequential id column (not meaningful externally)
Renames columns to the standard (CliniQ-compatible) shape:
  commercial_name_en, commercial_name_ar, scientific_name, manufacturer,
  drug_class, route, price_egp
Writes both CSV and JSON next to this script.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


SRC = Path("/home/karem/side projects/ahmed /clincD/drug-eye-extract/drugeye-with-arabic.csv")
OUT_DIR = Path(__file__).parent / "data"


def is_real(name: str) -> bool:
    n = (name or "").strip()
    if len(n) < 2:
        return False
    # purely digits/punctuation = junk placeholder
    if not re.search(r"[A-Za-z]", n):
        return False
    return True


def main() -> int:
    if not SRC.exists():
        print(f"missing source: {SRC}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    with SRC.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            trade = (r["trade_en"] or "").strip()
            if not is_real(trade):
                continue
            ar = (r["arabic_alias_brand"] or "").strip() or (r["arabic_alias"] or "").strip()
            scientific = (r["scientific"] or "").strip()
            company = (r["company"] or "").strip()
            klass = (r["drug_class"] or "").strip()
            route = (r["route"] or "").strip()
            price = (r["price"] or "").strip()
            try:
                price_val = float(price) if price else None
            except ValueError:
                price_val = None
            rows.append({
                "commercial_name_en": trade,
                "commercial_name_ar": ar,
                "scientific_name": scientific,
                "manufacturer": company,
                "drug_class": klass,
                "route": route,
                "price_egp": price_val,
            })

    rows.sort(key=lambda r: r["commercial_name_en"].lower())

    csv_path = OUT_DIR / "egyptian-drugs.csv"
    json_path = OUT_DIR / "egyptian-drugs.json"

    fields = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2)

    print(f"rows kept     : {len(rows):,}")
    print(f"csv  → {csv_path}  ({csv_path.stat().st_size:,} bytes)")
    print(f"json → {json_path}  ({json_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
