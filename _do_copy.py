import shutil
src = r"C:\Users\Admin\Documents\cust\infotec\inner-page-3.html"
dst = r"C:\Users\Admin\Documents\cust\infotec\inner-page-metalworking.html"
shutil.copy2(src, dst)
with open(dst, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"Copied. Line count: {len(lines)}")