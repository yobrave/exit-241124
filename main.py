"""Exit notice courier for the one-line resignation bounty.

Carries the draft notice from the repo into the grading dropbox,
verifying the parcel against the gate before hand-off.
"""
from pathlib import Path
import json
import os

NOTICE = "entry.txt"
LIMIT = 140
STAMP = "exit3-farewell"


def parcel(home: Path):
    raw = (home / NOTICE).read_bytes()
    for enc in ("utf-8",):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            return None
    return None


def first_line(block: str) -> str:
    """Keep the first line that shows any ink."""
    for row in block.replace("\r", "").split("\n"):
        if row.strip():
            return row
    return ""


def inspect(text):
    if text is None:
        return {"state": "reject", "why": "not utf-8 text"}
    cleaned = first_line(text)
    trimmed = cleaned.strip()
    if not trimmed:
        return {"state": "reject", "why": "blank notice"}
    if len(trimmed) > LIMIT:
        return {"state": "reject", "why": f"notice exceeds {LIMIT} chars"}
    return {"state": "ok", "line": cleaned}


def deliver(home: Path, line: str):
    drop = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
    drop.mkdir(parents=True, exist_ok=True)
    target = drop / NOTICE
    target.write_bytes(line.encode("utf-8"))
    if target.read_bytes() != line.encode("utf-8"):
        raise SystemExit("hand-off mismatch")
    return target


def main():
    home = Path(__file__).resolve().parent
    verdict = inspect(parcel(home))
    if verdict["state"] != "ok":
        print(json.dumps(verdict))
        raise SystemExit(1)
    deliver(home, verdict["line"])
    print(json.dumps({"state": "delivered", "chars": len(verdict["line"]), "stamp": STAMP}))


main()
