from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SCRAPERS = [
    ("ES BMW", BASE_DIR / "ES_MARKET", "bmw_scraper.py"),
    ("ES Audi", BASE_DIR / "ES_MARKET", "audi_scraper.py"),
    ("ES Mercedes-Benz", BASE_DIR / "ES_MARKET", "mercedes_scraper.py"),
    ("PT BMW", BASE_DIR / "PT_MARKET", "bmw_scraper_pt.py"),
    ("PT Audi", BASE_DIR / "PT_MARKET", "audi_scraper_pt.py"),
    ("PT Mercedes-Benz", BASE_DIR / "PT_MARKET", "mercedes_scraper_pt.py"),
]

SCRAPER_TIMEOUT_SECONDS = 45 * 60
BUILD_TIMEOUT_SECONDS = 10 * 60


def run_step(label: str, cwd: Path, args: list[str], env: dict[str, str], timeout: int) -> None:
    print("\n" + "=" * 80, flush=True)
    print(label, flush=True)
    print("=" * 80, flush=True)
    subprocess.run(args, cwd=str(cwd), env=env, check=True, timeout=timeout)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run daily stock scrapers and rebuild the Streamlit dataset.")
    parser.add_argument("--skip-scrapers", action="store_true", help="Only rebuild global XLSX/CSV from existing market Excel files.")
    ns = parser.parse_args()

    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("BMW_HEADLESS", "1")
    env.setdefault("PLAYWRIGHT_HEADLESS", "1")

    if not ns.skip_scrapers:
        for label, cwd, script in SCRAPERS:
            run_step(label, cwd, [sys.executable, "-u", script], env, SCRAPER_TIMEOUT_SECONDS)

    run_step(
        "Build normalized global dataset",
        BASE_DIR,
        [sys.executable, "-u", str(BASE_DIR / "scripts" / "build_global_dataset.py")],
        env,
        BUILD_TIMEOUT_SECONDS,
    )


if __name__ == "__main__":
    main()
