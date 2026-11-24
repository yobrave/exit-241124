"""Final error message from an employee quitting in one line."""
import os
from pathlib import Path

LAST = ("I quit my job writing error messages. This is my last one: "
        "Unexpected exit on line 1 — please restart your employee.")
CODE = "exit2"
WAIT = "one"
NOTE = "door closed"

base = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
base.mkdir(parents=True, exist_ok=True)
out = base / "entry.txt"
out.write_bytes((LAST + "\n").encode("utf-8"))
back = out.read_text(encoding="utf-8").strip()
assert back == LAST, "exit line lost in the loop"
print(CODE, "wait", WAIT, "len", len(back))
print(NOTE, "badge on the desk")
