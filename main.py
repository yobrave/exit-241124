"""Builds the one-line resignation letter for The One-Line Exit (140 chars max)."""
import json
import os

from pathlib import Path

PARTS = (
    "I quit my job writing error messages. ",
    "This is my last one: Unexpected exit on line 1",
    " — please restart your employee.",
)


def build_line():
    return "".join(PARTS).strip()


def deliver():
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    folder = Path(base)
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    line = build_line()
    target.write_text(line + "\n", encoding="utf-8")
    return {"chars": len(line), "path": str(target), "line": line}


print(json.dumps(deliver(), ensure_ascii=False))
