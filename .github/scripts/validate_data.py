#!/usr/bin/env python3
"""Validate data.json structure so contributor PRs fail fast on mistakes.

Checks:
- valid JSON
- top-level `meta` and `workshops` keys present
- each workshop has the required fields with sane types
- `city` is one of the three NeurIPS 2026 locations
- `deadline` is null or a YYYY-MM-DD string
- `lowEffort` is true, false, or null
- `url` looks like an http(s) link
- `topics` is a non-empty list drawn from `meta.topics`
- no duplicate (name, url) pairs
"""
import json
import re
import sys
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data.json"
REQUIRED_FIELDS = ["name", "url", "city", "deadline", "pages", "lowEffort", "lowEffortNote", "scope", "status", "topics"]
VALID_CITIES = {"Sydney", "Paris", "Atlanta"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(msg):
    print(f"::error::{msg}")
    sys.exit(1)


def main():
    if not DATA_PATH.exists():
        fail(f"{DATA_PATH} does not exist")

    try:
        raw = DATA_PATH.read_text(encoding="utf-8")
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"data.json is not valid JSON: {e}")
        return

    if "meta" not in payload or "workshops" not in payload:
        fail("data.json must have top-level 'meta' and 'workshops' keys")

    workshops = payload["workshops"]
    if not isinstance(workshops, list) or not workshops:
        fail("'workshops' must be a non-empty list")

    valid_topics = set(payload.get("meta", {}).get("topics", []))
    if not valid_topics:
        fail("meta.topics must list the allowed topic taxonomy")

    seen = set()
    errors = []

    for i, w in enumerate(workshops):
        label = w.get("name", f"<entry #{i}>")

        for field in REQUIRED_FIELDS:
            if field not in w:
                errors.append(f"[{label}] missing required field '{field}'")

        city = w.get("city")
        if city is not None and city not in VALID_CITIES:
            errors.append(f"[{label}] invalid city '{city}' (expected one of {sorted(VALID_CITIES)})")

        deadline = w.get("deadline")
        if deadline is not None and not DATE_RE.match(str(deadline)):
            errors.append(f"[{label}] deadline '{deadline}' is not null or YYYY-MM-DD")

        low_effort = w.get("lowEffort", "MISSING")
        if low_effort not in (True, False, None):
            errors.append(f"[{label}] lowEffort must be true, false, or null (got {low_effort!r})")

        url = w.get("url", "")
        if not str(url).startswith("http"):
            errors.append(f"[{label}] url '{url}' does not look like a link")

        topics = w.get("topics")
        if not isinstance(topics, list) or not topics:
            errors.append(f"[{label}] topics must be a non-empty list")
        else:
            unknown = [t for t in topics if t not in valid_topics]
            if unknown:
                errors.append(f"[{label}] topics not in meta.topics taxonomy: {unknown}")

        key = (w.get("name"), w.get("url"))
        if key in seen:
            errors.append(f"[{label}] duplicate entry (same name + url already present)")
        seen.add(key)

    if errors:
        for e in errors:
            print(f"::error::{e}")
        print(f"\n{len(errors)} issue(s) found across {len(workshops)} workshop entries.")
        sys.exit(1)

    print(f"data.json OK — {len(workshops)} workshop entries, all required fields present and well-formed.")


if __name__ == "__main__":
    main()
