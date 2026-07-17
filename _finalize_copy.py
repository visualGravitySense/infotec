import shutil
import os

base = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base, "inner-page-3.html")
dst = os.path.join(base, "inner-page-metalworking.html")

shutil.copy2(src, dst)

with open(src, "r", encoding="utf-8") as f:
    src_lines = f.readlines()
with open(dst, "r", encoding="utf-8") as f:
    dst_lines = f.readlines()

src_count = len(src_lines)
dst_count = len(dst_lines)
last_line = dst_lines[-1].rstrip("\n") if dst_lines else ""

print(f"Source lines: {src_count}")
print(f"Destination lines: {dst_count}")
print(f"Last line: {last_line}")
print("OK" if dst_count == 2137 and last_line == "</html>" else "VERIFY_FAILED")