import shutil
from pathlib import Path

src = Path(__file__).parent / "inner-page-1.html"
dst = Path(__file__).parent / "index.html"
shutil.copy2(src, dst)
print("copied")