#!/usr/bin/env python3
"""Saenztech mockup builder.

Usage: python3 build.py LEAD.json OUT_ROOT [--kit KIT_DIR] [--fonts NODE_MODULES/@fontsource]
Creates OUT_ROOT/<slug>/ with index.html, fonts/, robots-safe meta. Screenshots are taken by shot.js.
"""
import json, os, re, shutil, sys, copy, argparse, urllib.parse
from jinja2 import Environment, FileSystemLoader, select_autoescape

ap = argparse.ArgumentParser()
ap.add_argument("lead"); ap.add_argument("out_root")
ap.add_argument("--kit", default=os.path.dirname(os.path.abspath(__file__)))
ap.add_argument("--fonts", default="node_modules/@fontsource")
a = ap.parse_args()

themes = json.load(open(os.path.join(a.kit, "themes.json")))
b = json.load(open(a.lead))

def merge(base, over):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out

cat = b.get("category", "services")
if cat not in themes or cat.startswith("_"):
    sys.exit(f"unknown category {cat}")
th = themes[cat]
if "_extends" in th:
    th = merge(themes[th["_extends"]], {k: v for k, v in th.items() if k != "_extends"})
th = copy.deepcopy(th)
th["labels"] = merge(themes["_common_labels"], th.get("labels", {}))

# required fields
for f in ("slug", "business", "headline", "lead", "subtitle"):
    if not b.get(f):
        sys.exit(f"lead missing required field: {f}")
if not re.fullmatch(r"[a-z0-9-]{3,60}", b["slug"]):
    sys.exit("slug must be lowercase letters, digits, hyphens")

lang = b.get("lang", "en")
bilingual = b.get("bilingual", True)
alt = "en" if lang == "es" else "es"

def t(es, en):
    return es if lang == "es" else en

items = b.get("items", [])[:6]
ph = th["labels"].get("placeholders", [])
need = max(0, (4 if len(items) < 4 else 0) - len(items))
placeholders = ph[:need] if need else []

maps = ""
if b.get("address"):
    maps = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote_plus(b["address"])

# fonts
fonts_meta = themes["_fonts"]
out_dir = os.path.join(a.out_root, b["slug"])
os.makedirs(os.path.join(out_dir, "fonts"), exist_ok=True)
faces = []
for fam in {th["head_font"], th["body_font"]}:
    m = fonts_meta[fam]
    for style, weights in (("normal", m.get("weights", [])), ("italic", m.get("italic", []))):
        for w in weights:
            fn = f"{m['pkg']}-latin-{w}-{style}.woff2"
            src = os.path.join(a.fonts, m["pkg"], "files", fn)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(out_dir, "fonts", fn))
                faces.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{style};font-display:swap;src:url(fonts/{fn}) format("woff2")}}')
            else:
                print(f"warning: missing font file {src}", file=sys.stderr)

env = Environment(loader=FileSystemLoader(a.kit), autoescape=select_autoescape(["html", "j2"]))
html = env.get_template("template.html.j2").render(
    b=b, th=th, lang=lang, alt=alt, bilingual=bilingual, t=t,
    placeholders=placeholders, maps=maps, fontfaces="\n".join(faces))
open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(html)
print(out_dir)
