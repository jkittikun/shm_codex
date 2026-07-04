from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OUTPUT = ROOT / "docs" / "generated" / "interactives"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from shm_site.interactives.labs import build_all_labs, write_lab_page  # noqa: E402


def main() -> int:
    generated = [write_lab_page(lab, OUTPUT) for lab in build_all_labs()]
    for path in generated:
        print(f"generated {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
