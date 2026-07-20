#!/usr/bin/env python3
"""Fail CI when Katrina Li's ownership or required MIT records are altered."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md": ["Katrina Li", "## Ownership"],
    "LICENSE": ["MIT License", "Copyright (c) 2026 Katrina Li"],
    "COPYRIGHT.md": ["Copyright © 2026 Katrina Li", "MIT License"],
    "NOTICE": ["Katrina Li", "katlicolumbia-a11y"],
    ".github/CODEOWNERS": ["* @katlicolumbia-a11y"],
}

errors = []
for relative_path, markers in REQUIRED.items():
    path = ROOT / relative_path
    if not path.is_file():
        errors.append(f"missing required ownership file: {relative_path}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"missing ownership marker in {relative_path}: {marker}")

if errors:
    raise SystemExit("COPYRIGHT GUARD FAILED\n" + "\n".join(f"- {e}" for e in errors))

print("Copyright, attribution, and MIT preservation records verified.")
