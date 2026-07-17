import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
shutil.copy2(root / "index-cyber.html", root / "index.html")
print("synced", (root / "index.html").stat().st_size)