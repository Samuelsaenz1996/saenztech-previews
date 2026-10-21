#!/usr/bin/env python3
"""Saenztech mockup builder (multi-page).

Usage: python3 build.py LEAD.json OUT_ROOT [--kit KIT_DIR] [--fonts NODE_MODULES/@fontsource]
Creates OUT_ROOT/<slug>/ with one folder per page (index.html at the root is Home),
fonts/, img/ and pages.json. Screenshots are taken by shot.js.
"""
import json, html as _h, os, re, shutil, sys, copy, argparse, urllib.parse, urllib.request, random

ap = argparse.ArgumentParser()
ap.add_argument("lead"); ap.add_argument("out_root")
ap.add_argument("--kit", default=os.path.dirname(os.path.abspath(__file__)))
ap.add_argument("--fonts", default="node_modules/@fontsource")
a = ap.parse_args()

from jinja2 import Environment, FileSystemLoader, select_autoescape

themes = json.load(open(os.path.join(a.kit, "themes.json"), encoding="utf-8"))
b = json.load(open(a.lead, encoding="utf-8"))


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
stock_key = th.get("_extends") or cat
if "_extends" in th:
    th = merge(themes[th["_extends"]], {k: v for k, v in th.items() if k != "_extends"})
th = copy.deepcopy(th)
th["labels"] = merge(themes["_common_labels"], th.get("labels", {}))
# per-lead style override: {"colors": {...}, "head_font", "body_font", "head_weight", "deco", "radius", "tilt", "em_style", "tracking"}
for _k, _v in (b.get("style") or {}).items():
    if _k == "colors":
        th["colors"].update(_v)
    elif _k in ("head_font", "body_font", "head_weight", "deco", "radius", "tilt", "em_style", "tracking", "arch", "accent_font", "variant"):
        th[_k] = _v
L = th["labels"]

for f in ("slug", "business", "headline", "lead", "subtitle"):
    if not b.get(f):
        sys.exit(f"lead missing required field: {f}")
if not re.fullmatch(r"[a-z0-9-]{3,60}", b["slug"]):
    sys.exit("slug must be lowercase letters, digits, hyphens")

lang = b.get("lang", "en")
bilingual = b.get("bilingual", True)
alt = "en" if lang == "es" else "es"
out_dir = os.path.join(a.out_root, b["slug"])
os.makedirs(out_dir, exist_ok=True)


def t(es, en):
    return es if lang == "es" else en


# ---------- photos ----------
img_dir = os.path.join(out_dir, "img")
if os.path.isdir(img_dir):
    shutil.rmtree(img_dir)
os.makedirs(img_dir, exist_ok=True)


def fetch(src, name_hint):
    """Copy a local file or download a URL into img/. Returns relative path or None."""
    ext = os.path.splitext(urllib.parse.urlparse(src).path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".avif"):
        ext = ".jpg"
    fn = name_hint + ext
    dst = os.path.join(img_dir, fn)
    try:
        if re.match(r"https?://", src):
            req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 saenztech-kit"})
            with urllib.request.urlopen(req, timeout=20) as r, open(dst, "wb") as fh:
                fh.write(r.read())
        else:
            p = src if os.path.isabs(src) else os.path.join(os.path.dirname(os.path.abspath(a.lead)), src)
            if not os.path.exists(p):
                p = os.path.join(a.kit, src)
            shutil.copy(p, dst)
        if os.path.getsize(dst) < 2000:
            raise ValueError("file too small")
        return "img/" + fn
    except Exception as e:  # noqa
        print(f"warning: photo not used ({src}): {e}", file=sys.stderr)
        if os.path.exists(dst):
            os.remove(dst)
        return None


photos = []
for i, p in enumerate(b.get("photos", [])[:12]):
    p = dict(p) if isinstance(p, dict) else {"src": p}
    rel = fetch(p["src"], f"photo-{i+1}")
    if rel:
        p["path"] = rel
        photos.append(p)

# stock library fallback: kit/stock/<category>/manifest.json  ([{file, alt, credit, tags}])
stock_used = False
want = 7
if len(photos) < want and b.get("stock", True):
    for key in (cat, stock_key, "_any"):
        mf = os.path.join(a.kit, "stock", key, "manifest.json")
        if os.path.exists(mf):
            lib = json.load(open(mf, encoding="utf-8"))
            tags = set(t.lower() for t in b.get("stock_tags", []))
            rnd = random.Random(b["slug"])
            # photos tagged "explicit" (e.g. bakery) are only used when the lead asks for one of their tags
            match = [s for s in lib if tags & set(s.get("tags", []))]
            general = [s for s in lib if "explicit" not in s.get("tags", []) and s not in match]
            rnd.shuffle(match)
            rnd.shuffle(general)
            used = {os.path.basename(str((x.get("src") if isinstance(x, dict) else x) or "")) for x in b.get("photos", [])}
            match = [s for s in match if s["file"] not in used]
            general = [s for s in general if s["file"] not in used]
            pool = match if len(match) >= 3 else match + general
            for j, s in enumerate(pool):
                if len(photos) >= want:
                    break
                rel = fetch(os.path.join("stock", key, s["file"]), f"sample-{j+1}")
                if rel:
                    photos.append({"path": rel, "alt": s.get("alt", ""), "credit": s.get("credit", ""), "sample": True, "tags": s.get("tags", [])})
                    stock_used = True
            break

hero_photo = photos[0] if photos else None
gallery = photos[1:] if len(photos) > 1 else []

# ---------- items ----------
items = b.get("items", [])[:16]
for i, it in enumerate(items):
    if it.get("photo"):
        it["photo_path"] = fetch(it["photo"], f"item-{i+1}")
# give items a matching sample photo when a photo's tag appears in the item name (e.g. "birria", "burritos")
def _names(v):
    return " ".join(v.values()).lower() if isinstance(v, dict) else str(v).lower()
used = set()
for it in items:
    if it.get("photo_path"):
        continue
    nm = _names(it.get("name", ""))
    for k, ph in enumerate(photos):
        if not ph.get("sample") or k in used:
            continue
        if any(len(tg) > 3 and tg.rstrip("s") in nm for tg in ph.get("tags", []) if tg not in ("mexican", "plate", "explicit", "salon")):
            it["photo_path"], it["photo_sample"] = ph["path"], True
            used.add(k)
            break
groups = []
for it in items:
    g = it.get("group") or ""
    gk = json.dumps(g, sort_keys=True, ensure_ascii=False)
    for gg in groups:
        if gg["key"] == gk:
            gg["items"].append(it)
            break
    else:
        groups.append({"key": gk, "name": g, "items": [it]})

placeholders = L.get("placeholders", [])[:max(0, 4 - len(items))]

maps = embed = ""
if b.get("address"):
    q = urllib.parse.quote_plus(b["address"])
    maps = "https://www.google.com/maps/search/?api=1&query=" + q
    embed = "https://www.google.com/maps?q=" + q + "&output=embed"

# ---------- pages ----------
P = th.get("pages", {})
pages = [{"id": "home", "dir": "", "label": L["nav_home"]},
         {"id": "items", "dir": P.get("items_dir", "services"), "label": L["items_nav"]}]
if len(gallery) >= 4:
    pages.append({"id": "gallery", "dir": P.get("gallery_dir", "gallery"), "label": L["gallery_nav"]})
if b.get("about"):
    pages.append({"id": "about", "dir": "about", "label": L["nav_about"]})
if P.get("visit") and (b.get("hours") or b.get("address")):
    pages.append({"id": "visit", "dir": "visit", "label": L["nav_visit"]})
pages.append({"id": "contact", "dir": "contact", "label": L["nav_contact"]})

if b.get("order_url"):
    primary = {"href": b["order_url"], "ext": True, "label": b.get("order_label") or L["order"], "icon": "bag"}
elif b.get("booking_url"):
    primary = {"href": b["booking_url"], "ext": True, "label": b.get("booking_label") or L["book"], "icon": "cal"}
elif P.get("quote"):
    primary = {"href": "contact/", "ext": False, "internal": True, "label": L["book"], "icon": "doc"}
elif b.get("phone"):
    primary = {"href": "tel:" + b["phone"], "ext": False, "label": L["call"], "icon": "phone"}
else:
    primary = {"href": "contact/", "ext": False, "internal": True, "label": L["nav_contact"], "icon": "mail"}

stop = {"y", "and", "de", "del", "la", "el", "los", "las", "llc", "inc", "the", "co"}
words = [w for w in re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ0-9]+", b["business"]) if w.lower() not in stop]
initials = ("".join(w[0] for w in words[:2]) or b["business"][:1]).upper()

sys.path.insert(0, a.kit)
import motifs as _motifs
motif = _motifs.pick(b)
arch = th.get("arch") or ("fiesta" if b.get("category") in ("food",) else "classic")
M = _motifs.MOTIFS[motif]

# ---------- fonts ----------
fonts_meta = themes["_fonts"]
os.makedirs(os.path.join(out_dir, "fonts"), exist_ok=True)
faces = []
th.setdefault("accent_font", th["head_font"])
for fam in {th["head_font"], th["body_font"], th["accent_font"]}:
    m = fonts_meta[fam]
    for style, weights in (("normal", m.get("weights", [])), ("italic", m.get("italic", []))):
        for w in weights:
            fn = f"{m['pkg']}-latin-{w}-{style}.woff2"
            src = os.path.join(a.fonts, m["pkg"], "files", fn)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(out_dir, "fonts", fn))
                faces.append((fam, w, style, fn))
            else:
                print(f"warning: missing font file {src}", file=sys.stderr)

for d in ("menu", "services", "packages", "gallery", "projects", "about", "visit", "contact"):
    pd = os.path.join(out_dir, d)
    if os.path.isdir(pd) and d not in [p["dir"] for p in pages]:
        shutil.rmtree(pd)

env = Environment(loader=FileSystemLoader(a.kit), autoescape=select_autoescape(["html", "j2"]))
tpl = env.get_template("template.html.j2")
for pg in pages:
    root = "../" if pg["dir"] else ""
    ff = "\n".join(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url({root}fonts/{fn}) format("woff2")}}' for fam, w, st, fn in faces)
    html = tpl.render(
        b=b, th=th, lang=lang, alt=alt, bilingual=bilingual, t=t, page=pg["id"], pages=pages,
        root=root, groups=groups, items=items, placeholders=placeholders, maps=maps, embed=embed,
        fontfaces=ff, hero_photo=hero_photo, gallery=gallery, primary=primary, initials=initials,
        stock_used=stock_used, bn=_h.escape(b['business']), motif=motif, M=M, arch=arch)
    d = os.path.join(out_dir, pg["dir"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)

json.dump([p["dir"] for p in pages], open(os.path.join(out_dir, "pages.json"), "w"))
print(json.dumps({"dir": out_dir, "pages": [p["dir"] or "/" for p in pages], "photos": len(photos), "stock": stock_used}))
