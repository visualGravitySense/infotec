# -*- coding: utf-8 -*-
"""Пересобрать галерею: скриншоты всех .html + gallery.html.
Запуск:  python _gallery/rebuild.py
Нужен запущенный статический сервер:  python -m http.server 8899 --bind 127.0.0.1
Флаг --skip-shots — только перегенерировать gallery.html из существующих скриншотов.
"""
import os, subprocess, urllib.parse, html, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "_gallery", "shots")
PORT = 8899
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SKIP = "--skip-shots" in sys.argv
os.makedirs(SHOTS, exist_ok=True)

files = []
for dp, dn, fns in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ("_gallery", "node_modules", ".git")]
    for fn in fns:
        if fn.lower().endswith(".html") and fn != "gallery.html":
            files.append(os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/"))
files.sort()

def slug(r): return r.replace("/", "__").replace(" ", "_")[:-5]

items = []
for rel in files:
    s = slug(rel)
    shot_abs = os.path.join(SHOTS, s + ".png")
    if not SKIP:
        print("shot:", rel)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--no-sandbox", "--virtual-time-budget=9000", "--window-size=1440,1900",
                        "--screenshot=" + shot_abs,
                        "http://127.0.0.1:%d/%s" % (PORT, urllib.parse.quote(rel))],
                       capture_output=True, timeout=90)
    items.append({"rel": rel, "name": rel.split("/")[-1],
                  "dir": "/".join(rel.split("/")[:-1]) or ".",
                  "shot": ("_gallery/shots/%s.png" % s) if os.path.exists(shot_abs) else ""})

json.dump(items, open(os.path.join(ROOT, "_gallery", "items.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

cards = []
for it in items:
    thumb = ("<img loading='lazy' src='%s' alt=''>" % html.escape(it["shot"])) if it["shot"] \
            else "<div class='noshot'>нет скриншота</div>"
    cards.append(
        '<figure class="card" data-src="%s" data-name="%s"><div class="thumb">%s</div>'
        '<figcaption><span class="fn">%s</span><span class="dir">%s</span></figcaption></figure>'
        % (html.escape(it["rel"]), html.escape(it["name"]), thumb,
           html.escape(it["name"]), html.escape(it["dir"])))

TPL = r"""<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Галерея шаблонов — Infotec</title><style>
*{box-sizing:border-box}
body{margin:0;background:#0e1420;color:#e8eef7;font:14px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{padding:20px 28px;border-bottom:1px solid #24324a;display:flex;align-items:baseline;gap:14px;position:sticky;top:0;background:#0e1420;z-index:5;flex-wrap:wrap}
header h1{font-size:18px;margin:0}
header .count{color:#93a1b5}
header input{margin-left:auto;background:#182234;border:1px solid #2b3a55;color:#e8eef7;padding:8px 12px;border-radius:8px;width:260px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px;padding:24px 28px}
.card{margin:0;background:#141d2e;border:1px solid #24324a;border-radius:12px;overflow:hidden;cursor:pointer;transition:.15s;display:flex;flex-direction:column}
.card:hover{border-color:#3b82f6;transform:translateY(-3px)}
.thumb{height:210px;overflow:hidden;background:#0b1120;border-bottom:1px solid #24324a}
.thumb img{width:100%;display:block;object-fit:cover;object-position:top}
.noshot{display:flex;align-items:center;justify-content:center;height:100%;color:#5b6b82}
figcaption{padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.fn{font-weight:600;word-break:break-all}
.dir{color:#93a1b5;font-size:12px;word-break:break-all}
.hidden{display:none}
.modal{position:fixed;inset:0;background:rgba(5,8,14,.92);display:none;flex-direction:column;z-index:50}
.modal.open{display:flex}
.mbar{display:flex;align-items:center;gap:12px;padding:10px 16px;background:#141d2e;border-bottom:1px solid #24324a;flex-wrap:wrap}
.mbar .title{font-weight:600}
.mbar a{color:#7fb0ff;text-decoration:none;font-size:13px}
.mbar button{background:#24324a;border:0;color:#e8eef7;width:34px;height:34px;border-radius:8px;font-size:18px;cursor:pointer}
.mbar #mclose{margin-left:auto}
.mbar .zoom{background:#1f2c44;padding:0 12px;width:auto;font-size:13px}
.frameWrap{flex:1;overflow:auto;background:#fff}
iframe{border:0;background:#fff;display:block}
</style></head><body>
<header><h1>Галерея HTML-шаблонов</h1><span class="count" id="count"></span>
<input id="q" type="search" placeholder="фильтр по имени/папке…"></header>
<div class="grid" id="grid">
__CARDS__
</div>
<div class="modal" id="modal"><div class="mbar">
<span class="title" id="mtitle"></span>
<a id="mopen" target="_blank" rel="noopener">открыть в новой вкладке ↗</a>
<button class="zoom" id="zoomOut">−</button>
<span id="zoomLabel" style="font-size:13px;min-width:44px;text-align:center">100%</span>
<button class="zoom" id="zoomIn">+</button>
<button class="zoom" id="zoomReset">сброс</button>
<button id="mclose" title="закрыть (Esc)">×</button>
</div><div class="frameWrap" id="frameWrap"><iframe id="frame" title="preview"></iframe></div></div>
<script>
var modal=document.getElementById('modal'),frame=document.getElementById('frame'),
frameWrap=document.getElementById('frameWrap'),mtitle=document.getElementById('mtitle'),
mopen=document.getElementById('mopen'),q=document.getElementById('q'),
countEl=document.getElementById('count'),zoomLabel=document.getElementById('zoomLabel');
var cards=[].slice.call(document.querySelectorAll('.card')),zoom=1;
function refreshCount(){countEl.textContent=cards.filter(function(c){return !c.classList.contains('hidden')}).length+' / '+cards.length;}
refreshCount();
function applyZoom(){zoomLabel.textContent=Math.round(zoom*100)+'%';
frame.style.width=(100/zoom)+'%';frame.style.height=(frameWrap.clientHeight/zoom)+'px';
frame.style.transform='scale('+zoom+')';frame.style.transformOrigin='top left';}
function openModal(src,name){mtitle.textContent=name;mopen.href=src;frame.src=src;zoom=1;
modal.classList.add('open');document.body.style.overflow='hidden';setTimeout(applyZoom,50);}
function closeModal(){modal.classList.remove('open');frame.src='about:blank';document.body.style.overflow='';}
cards.forEach(function(c){c.addEventListener('click',function(){openModal(c.dataset.src,c.dataset.name);});});
document.getElementById('mclose').addEventListener('click',closeModal);
modal.addEventListener('click',function(e){if(e.target===modal)closeModal();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&modal.classList.contains('open'))closeModal();});
document.getElementById('zoomIn').addEventListener('click',function(){zoom=Math.min(3,zoom+0.25);applyZoom();});
document.getElementById('zoomOut').addEventListener('click',function(){zoom=Math.max(0.25,zoom-0.25);applyZoom();});
document.getElementById('zoomReset').addEventListener('click',function(){zoom=1;applyZoom();});
window.addEventListener('resize',function(){if(modal.classList.contains('open'))applyZoom();});
q.addEventListener('input',function(){var t=q.value.toLowerCase();
cards.forEach(function(c){var hay=(c.dataset.src+' '+c.dataset.name).toLowerCase();
c.classList.toggle('hidden',t&&hay.indexOf(t)===-1);});refreshCount();});
</script></body></html>
"""
open(os.path.join(ROOT, "gallery.html"), "w", encoding="utf-8").write(
    TPL.replace("__CARDS__", "\n".join(cards)))
print("OK:", len(items), "->", os.path.join(ROOT, "gallery.html"))
