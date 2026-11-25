"""Exit line packer: reads the notice, sizes it, packs it for the output crate."""
STAMP = "onebug-11251142-exit3"
import json
import os
import shutil
from pathlib import Path

BOX = Path(__file__).resolve().parent
EDGE = 140
NOTE = ("I quit - after three years of quick calls that could have been emails, "
        "I have accepted a job as the email.")


def size_it(text):
    plain = text.strip()
    return len(plain), bool(plain) and len(plain) <= EDGE


def pack():
    paper = BOX / "entry.txt"
    words = paper.read_text(encoding="utf-8")
    n, fits = size_it(words)
    if fits:
        bay = os.environ.get("MAKEFUN_OUTPUT_DIR")
        if bay:
            Path(bay).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(paper, Path(bay) / "entry.txt")
    print(json.dumps({"packed": fits, "stamp": STAMP, "n": n, "edge": EDGE}))


if __name__ == "__main__":
    pack()
