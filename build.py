#!/usr/bin/env python3
"""账号2（小面包）发布文案网页。读 账号2_小面包/05_正式交付 里每个视频的同名 TXT，原文不改，输出 index.html。
用法: python3 build.py    然后 git add -A && git commit -m 更新 && git push
网址: https://mrssunkexin.github.io/xiaomianbao-fabu/"""
import html, os, re, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 账号2_小面包/
SRC = os.path.join(ROOT, "05_正式交付")
files = [p for p in os.listdir(SRC) if p.endswith(".txt")]
files.sort(key=lambda p: (-os.stat(os.path.join(SRC, p)).st_mtime_ns, p))   # 最新放行的排最前
items = []
for n, p in enumerate(files, 1):
    t = open(os.path.join(SRC, p), encoding="utf-8").read().rstrip("\n")
    m = re.match(r"标题：(.*)\n文案：\n(.*)\n标签：(.*)$", t, re.S)
    if not m:
        raise SystemExit(f"格式不符: {p}")
    items.append({"id": f"{len(files)-n+1:02d}", "file": p[:-4], "title": m.group(1).strip(), "body": m.group(2).strip(), "tags": m.group(3).strip()})
if not items:
    raise SystemExit("没有可发布的文案")
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
cards = "\n".join(f'''<article class="card" data-id="{i.get("file", i["id"])}">
<div class="head"><span class="no">{i["id"]}</span><span class="name">{html.escape(i.get("file", i["title"]))}.mp4</span><button class="mark" type="button">标记已发</button></div>
<section><div class="lab"><span>标题</span><button class="copy" type="button">复制</button></div><div class="text">{html.escape(i["title"])}</div></section>
<section><div class="lab"><span>文案</span><button class="copy" type="button">复制</button></div><div class="text">{html.escape(i["body"])}</div></section>
<section><div class="lab"><span>标签</span><button class="copy" type="button">复制</button></div><div class="text">{html.escape(i["tags"])}</div></section>
<button class="copy all" type="button" data-all="1">复制文案＋标签</button>
</article>''' for i in items)
page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>小面包 发布文案</title><style>
:root{{--bg:#fbf6ee;--card:#fff;--fg:#2b2520;--muted:#7a6c5e;--line:#eadfcf;--accent:#f0683c;--accent-fg:#fff;--soft:#fff0e4;--done:#eef3ea}}
@media (prefers-color-scheme:dark){{:root{{--bg:#181512;--card:#221e1a;--fg:#efe9e2;--muted:#a89a8b;--line:#3a322a;--accent:#ff8a5c;--accent-fg:#1a120c;--soft:#33261d;--done:#1f2a20;color-scheme:dark}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 "PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif}}
.wrap{{max-width:640px;margin:0 auto;padding:20px 16px 56px;display:grid;gap:14px}}
h1{{font-size:22px;margin:0}}header p{{margin:4px 0 0;color:var(--muted);font-size:13px}}
.tabs{{display:flex;gap:8px}}.tabs button{{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:999px;padding:6px 14px;font:inherit;font-size:13px}}
.tabs button[aria-pressed="true"]{{background:var(--accent);color:var(--accent-fg);border-color:var(--accent)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;display:grid;gap:12px}}.card.done{{background:var(--done)}}
.head{{display:flex;align-items:center;gap:8px}}.no{{background:var(--soft);color:var(--accent);border-radius:6px;padding:1px 8px;font-size:13px;font-weight:600}}
.name{{color:var(--muted);font-size:12px;flex:1;min-width:0;word-break:break-all}}
.mark{{border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:8px;padding:4px 10px;font:inherit;font-size:12px}}
.lab{{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}}.lab span{{color:var(--muted);font-size:12px}}
.text{{white-space:pre-wrap;word-break:break-word;background:var(--bg);border-radius:8px;padding:10px 12px;font-size:14px;user-select:text;-webkit-user-select:text}}
.copy{{border:0;background:var(--accent);color:var(--accent-fg);border-radius:8px;padding:6px 16px;font:inherit;font-size:13px;min-height:34px}}
.copy.ok{{background:#3aa08f;color:#fff}}.copy.all{{width:100%;padding:10px;font-size:14px}}
.hide{{display:none}}
</style></head><body><div class="wrap">
<header><h1>小面包 发布文案</h1><p>共 {len(items)} 条，最新的在最上面 · 更新于 {now}</p></header>
<div class="tabs"><button type="button" data-f="all" aria-pressed="true">全部</button><button type="button" data-f="todo" aria-pressed="false">未发</button><button type="button" data-f="done" aria-pressed="false">已发</button></div>
<main class="list">
{cards}
</main></div><script>
function copyText(t){{if(navigator.clipboard&&window.isSecureContext)return navigator.clipboard.writeText(t);return new Promise(function(res,rej){{var a=document.createElement("textarea");a.value=t;a.style.position="fixed";a.style.opacity="0";document.body.appendChild(a);a.select();try{{document.execCommand("copy")?res():rej()}}catch(e){{rej(e)}}document.body.removeChild(a)}})}}
var done={{}};try{{done=JSON.parse(localStorage.getItem("xiaomianbao_done")||"{{}}")}}catch(e){{}}
function save(){{try{{localStorage.setItem("xiaomianbao_done",JSON.stringify(done))}}catch(e){{}}}}
var filter="all";
function paint(){{document.querySelectorAll(".card").forEach(function(c){{var d=!!done[c.dataset.id];c.classList.toggle("done",d);c.querySelector(".mark").textContent=d?"已发 ✓":"标记已发";c.classList.toggle("hide",filter==="todo"&&d||filter==="done"&&!d)}})}}
document.addEventListener("click",function(e){{var b=e.target.closest("button");if(!b)return;
if(b.dataset.f){{filter=b.dataset.f;document.querySelectorAll(".tabs button").forEach(function(x){{x.setAttribute("aria-pressed",x===b)}});paint();return}}
var card=b.closest(".card");if(!card)return;
if(b.classList.contains("mark")){{var id=card.dataset.id;if(done[id])delete done[id];else done[id]=1;save();paint();return}}
if(b.classList.contains("copy")){{var t;if(b.dataset.all){{var s=card.querySelectorAll("section .text");t=s[1].textContent+"\\n"+s[2].textContent}}else t=b.closest("section").querySelector(".text").textContent;
var old=b.textContent;copyText(t).then(function(){{b.textContent="已复制 ✓";b.classList.add("ok")}},function(){{b.textContent="复制失败，请长按文字"}}).then(function(){{setTimeout(function(){{b.textContent=old;b.classList.remove("ok")}},1400)}})}}}});
paint();
</script></body></html>'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"), "w", encoding="utf-8").write(page)
print("已生成", len(items), "条:", " ".join(i["id"] for i in items))
