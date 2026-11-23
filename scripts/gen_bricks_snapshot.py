#!/usr/bin/env python3
"""Emit scripts/bricks.json for the aitherium.org periodic table.

The site used a DATED hand-refreshed snapshot (49 bricks) while the registry
(ecosystem.yaml) held 98, so the page was permanently missing elements. This
script reads `scripts/bricks_source.json` (a generated copy of the registry's
brick rows) and writes the snapshot the page generator consumes.

Never edit bricks.json by hand:
    python scripts/gen_bricks_snapshot.py
    python scripts/gen_pages.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "bricks_source.json"
OUT = ROOT / "scripts" / "bricks.json"


def main() -> int:
    source = json.loads(SRC.read_text(encoding="utf-8"))
    rows = source.get("bricks")
    if not isinstance(rows, list) or not rows:
        print("gen_bricks_snapshot: bricks_source.json has no bricks")
        return 2
    bricks = []
    for b in rows:
        if not isinstance(b, dict) or not b.get("id"):
            print(f"gen_bricks_snapshot: malformed row {b!r}")
            return 2
        public = b.get("status") == "public"
        bricks.append({
            "id": b["id"],
            "kind": b.get("kind") or "tool",
            "status": b.get("status"),
            "install": b.get("install") or "",
            "tagline": b.get("tagline") or "",
            "instead_of_trusting": b.get("instead_of_trusting") or "",
            "you_check": b.get("you_check") or "",
            "pairs_with": b.get("pairs_with") or [],
            # only a public brick has a repo and a docs page that answer
            "repo_ok": public,
            "pages_ok": public,
        })
    payload = {
        "_source": "scripts/gen_bricks_snapshot.py <- scripts/bricks_source.json "
                   "(AitherOS/config/ecosystem.yaml), do not edit by hand",
        "measured": dt.date.today().isoformat(),
        "source": source.get("_source"),
        "count": len(bricks),
        "bricks": bricks,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(bricks)} bricks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
