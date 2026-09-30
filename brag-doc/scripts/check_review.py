"""Check a brag-doc review JSON before building the Word file.

Usage:
    python check_review.py review.json

Exit code 0 = no blocking errors (warnings may still be listed).
Exit code 1 = blocking errors: fix them before running build_review.py.

Expected JSON shape:
{
  "person":  {"name": "Sara Ahmed", "title": "Senior FP&A Analyst", "manager": "Omar Khalid"},
  "period":  {"label": "Q3 2026", "start": "2026-07-01", "end": "2026-09-30"},
  "summary": "3-4 sentences.",
  "kpis": [{"value": "3 -> 1 day", "label": "Report cycle"}],
  "objectives": [
    {"id": "O1", "title": "Reduce month-end close time", "measure": "5 working days",
     "status": "On track",
     "achievements": [
       {"result": "Cut close from 8 to 5 days", "situation": "...", "task": "...",
        "action": "...", "stakeholders": ["Treasury"]}
     ]}
  ],
  "stakeholders": [{"name": "Treasury team", "work": "Bank file automation"}],
  "extra_mile": [{"title": "...", "action": "...", "result": "..."}],
  "learning": {"skills": ["Power Query"], "development_area": "..."},
  "references": [{"from": "Head of Treasury", "quote": "..."}]
}
"""

import json
import re
import sys

HYPE_WORDS = [
    "spearheaded", "synergy", "synergies", "game-changing", "game changer",
    "rockstar", "passionate", "leveraged", "world-class", "revolutionised",
    "revolutionized", "best-in-class", "cutting-edge",
]
VALID_STATUS = {"Achieved", "On track", "At risk", "Not started"}
NUMBER = re.compile(r"\d")
PLACEHOLDER = "[add number]"
QUANT_TARGET = 0.70


def main(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    errors, warnings = [], []

    for key in ("person", "period", "summary", "objectives"):
        if not data.get(key):
            errors.append(f"Missing required section: {key}")
    if errors:
        return report(errors, warnings, 0, 0)

    if not data["person"].get("name"):
        errors.append("person.name is empty")
    if not data["period"].get("label"):
        errors.append("period.label is empty")

    total, quantified = 0, 0
    seen_ids = set()

    for obj in data["objectives"]:
        oid = obj.get("id", "").strip()
        if not oid:
            errors.append(f"Objective without id: {obj.get('title', '?')}")
        elif oid in seen_ids:
            errors.append(f"Duplicate objective id: {oid}")
        seen_ids.add(oid)

        status = obj.get("status")
        if status and status not in VALID_STATUS:
            warnings.append(f"{oid}: status '{status}' is not one of {sorted(VALID_STATUS)}")

        achievements = obj.get("achievements", [])
        if not achievements:
            warnings.append(f"{oid}: no achievements in this period. Ask the user if work is missing.")
        if len(achievements) > 3:
            warnings.append(f"{oid}: {len(achievements)} achievements; keep the strongest 2-3.")

        for i, a in enumerate(achievements, 1):
            label = f"{oid} achievement {i}"
            result = (a.get("result") or "").strip()
            if not result:
                errors.append(f"{label}: result is empty")
                continue
            if not a.get("action"):
                warnings.append(f"{label}: no action; STAR needs what YOU did")
            total += 1
            if NUMBER.search(result):
                quantified += 1
            elif PLACEHOLDER not in result:
                warnings.append(f"{label}: no number in result -> '{result}'")

    for i, e in enumerate(data.get("extra_mile", []), 1):
        result = (e.get("result") or "").strip()
        if not result:
            warnings.append(f"Extra mile {i}: no result")
            continue
        total += 1
        if NUMBER.search(result):
            quantified += 1
        elif PLACEHOLDER not in result:
            warnings.append(f"Extra mile {i}: no number in result -> '{result}'")

    if len(data.get("kpis", [])) > 4:
        warnings.append("More than 4 KPI tiles; keep the 4 strongest.")

    if not (data.get("learning") or {}).get("development_area"):
        warnings.append("No development area; one honest area shows self-awareness.")

    text = json.dumps(data, ensure_ascii=False).lower()
    for word in HYPE_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            warnings.append(f"Hype word found: '{word}'. Replace with a plain verb unless the user used it.")

    placeholders = text.count(PLACEHOLDER)
    if placeholders:
        warnings.append(f"{placeholders} '{PLACEHOLDER}' placeholder(s) for the user to fill.")

    return report(errors, warnings, total, quantified)


def report(errors, warnings, total, quantified):
    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN:  {w}")
    if total:
        share = quantified / total
        flag = "PASS" if share >= QUANT_TARGET else "WARN"
        print(f"{flag}:  {quantified}/{total} results quantified ({share:.0%}, target {QUANT_TARGET:.0%})")
    if errors:
        print("RESULT: fix the errors above before building")
        return 1
    print("RESULT: ready to build")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
