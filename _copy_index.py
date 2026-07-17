import shutil
import os

base = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base, "inner-page-1.html")
dst = os.path.join(base, "index.html")

shutil.copy2(src, dst)

with open(src, "rb") as f:
    src_bytes = f.read()
with open(dst, "rb") as f:
    dst_bytes = f.read()

src_lines = src_bytes.count(b"\n") + (0 if src_bytes.endswith(b"\n") or not src_bytes else 1)
dst_lines = dst_bytes.count(b"\n") + (0 if dst_bytes.endswith(b"\n") or not dst_bytes else 1)

print(f"index.html exists: {os.path.exists(dst)}")
print(f"inner-page-1.html lines: {src_lines}")
print(f"index.html lines: {dst_lines}")
print(f"inner-page-1.html bytes: {len(src_bytes)}")
print(f"index.html bytes: {len(dst_bytes)}")
print(f"Byte-for-byte match: {src_bytes == dst_bytes}")