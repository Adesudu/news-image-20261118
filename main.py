# A working news-image-20261118 entry (Python 3.13, standard library only):
# its image is the entry.png beside this file, and the program copies it to
# /output/entry.png. The image sums up the world news of Wednesday
# 18 November 2026: Ukraine's second-day strike on the Crimean Bridge,
# Trump in Manila for Quad talks, Iran's drone attack in Bahrain, the
# Canada-China trade extension, UK sanctions, Nvidia's results, and more.
# It was drawn by render.py (Pillow, run at build time) from real headlines
# reported on 18 November 2026. The gate takes a whole PNG of at most 1 MiB
# and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
