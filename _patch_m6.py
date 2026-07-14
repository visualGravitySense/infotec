import os
base = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base, "inner-page-3.html")
dst = os.path.join(base, "inner-page-metalworking.html")
with open(src, "r", encoding="utf-8") as f:
    src_lines = f.readlines()
with open(dst, "r", encoding="utf-8") as f:
    dst_lines = f.readlines()
for i, line in enumerate(dst_lines):
    if line.strip().startswith("__M"):
        dst_lines = dst_lines[:i] + src_lines[i:]
        break
with open(dst, "w", encoding="utf-8", newline="") as f:
    f.writelines(dst_lines)
print("Source lines:", len(src_lines))
print("Destination lines:", len(dst_lines))
print("Last line:", dst_lines[-1].rstrip())
print("OK" if len(dst_lines) == 2137 and dst_lines[-1].strip() == "</html>" else "VERIFY_FAILED")