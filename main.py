"""exit6 resignation conveyor. A generator walks the line through stages."""
import json
import os
import sys
from pathlib import Path

SPAN = 140


def stages(root: Path, drop: Path):
    text = (root / "entry.txt").read_text(encoding="utf-8").strip()
    yield {"stage": "collected", "n": len(text)}
    verdict = text != "" and len(text) <= SPAN and not text.isspace()
    yield {"stage": "cleared", "verdict": verdict}
    if verdict:
        drop.mkdir(parents=True, exist_ok=True)
        (drop / "entry.txt").write_bytes(text.encode("utf-8"))
        yield {"stage": "handed_over", "drop": str(drop)}


def main():
    drop = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    trail = list(stages(Path(__file__).resolve().parent, drop))
    final = trail[-1]
    done = final["stage"] == "handed_over"
    print("VERDICT", json.dumps({"done": done, "span": SPAN, "door": "exit6", "trail": [t["stage"] for t in trail]}))
    return 0 if done else 1


if __name__ == "__main__":
    sys.exit(main())
