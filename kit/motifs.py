"""Original flat SVG illustrations + motion settings per business type.
Each motif: floaters (hero doodles), ride (object that travels the scroll track), trail (track style), tick (marquee separator).
All art is drawn from scratch in a 64x64 viewBox; brand colors come from CSS vars."""
import math


def _svg(body, vb="0 0 64 64"):
    return f'<svg viewBox="{vb}" aria-hidden="true">{body}</svg>'


def _gear(cx, cy, r_out, r_in, teeth, fill, hole=None):
    pts = []
    n = teeth * 4
    for i in range(n):
        a = 2 * math.pi * i / n
        r = r_out if i % 4 in (1, 2) else r_in
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    s = f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'
    if hole:
        s += f'<circle cx="{cx}" cy="{cy}" r="{hole}" fill="var(--bg)"/>'
    return s


# ---------- food ----------
TACO = _svg(
    '<path d="M10 30c3-5 7-4 9-7 3 3 6-1 9 1 3-3 6 0 9-2 3 2 6 0 8 3 3-1 6 1 9 5z" fill="#4FA83D"/>'
    '<circle cx="18" cy="27" r="3" fill="#D9412B"/><circle cx="33" cy="25" r="3" fill="#D9412B"/><circle cx="46" cy="27" r="2.6" fill="#D9412B"/>'
    '<path d="M14 30h36" stroke="#7A3E1D" stroke-width="5" stroke-linecap="round"/>'
    '<circle cx="25" cy="27" r="1.6" fill="#fff"/><circle cx="40" cy="26" r="1.6" fill="#fff"/>'
    '<path d="M5 31h54a27 27 0 0 1-54 0z" fill="#F2B544"/><path d="M5 31h54" stroke="#D99525" stroke-width="2"/>'
    '<circle cx="20" cy="40" r="1.4" fill="#D99525"/><circle cx="32" cy="46" r="1.4" fill="#D99525"/><circle cx="43" cy="39" r="1.4" fill="#D99525"/><circle cx="28" cy="37" r="1.2" fill="#D99525"/>')
CHILI = _svg('<path d="M44 14c-4 2-6 8-10 15S20 47 10 50c-2 1-1 3 1 3 14 0 28-10 34-24 2-5 2-10-1-15z" fill="#D9412B"/>'
             '<path d="M41 20c-3 6-8 14-15 21" stroke="#fff" stroke-opacity=".35" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
             '<path d="M44 14c0-4 3-7 7-8M40 13c3-1 6 0 8 3" stroke="#3E8A33" stroke-width="4" stroke-linecap="round" fill="none"/>')
LIME = _svg('<circle cx="32" cy="32" r="24" fill="#5FAE3A"/><circle cx="32" cy="32" r="19" fill="#D7EFA0"/>'
            + "".join(f'<path d="M32 32 L{32 + 17 * math.cos(math.radians(a)):.1f} {32 + 17 * math.sin(math.radians(a)):.1f}" stroke="#5FAE3A" stroke-width="2"/>' for a in range(0, 360, 45))
            + '<circle cx="32" cy="32" r="3" fill="#F4FBE3"/>')
LEAF_C = _svg('<path d="M12 52C10 30 24 12 52 10c2 26-14 42-40 42z" fill="#3E9A45"/><path d="M14 50C24 38 34 28 48 14" stroke="#2C7434" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
AVOCADO = _svg('<path d="M32 6c9 0 13 10 15 20 3 13 6 17 6 23 0 7-9 11-21 11S11 56 11 49c0-6 3-10 6-23C19 16 23 6 32 6z" fill="#3D6B2A"/>'
               '<path d="M32 11c7 0 10 8 12 17 2 11 5 15 5 20 0 5-7 8-17 8s-17-3-17-8c0-5 3-9 5-20 2-9 5-17 12-17z" fill="#CFE38A"/><circle cx="32" cy="42" r="8" fill="#8A5A2B"/>')
CONCHA = _svg('<ellipse cx="32" cy="44" rx="26" ry="9" fill="#C98A47"/><path d="M6 42c0-15 12-26 26-26s26 11 26 26z" fill="#F4A9B8"/>'
              '<path d="M14 30l26 12M22 22l26 14M32 17l20 16M50 30L24 42M42 22L16 36M32 17L10 33" stroke="#E07E93" stroke-width="2" fill="none"/>')
CONCHA_Y = CONCHA.replace("#F4A9B8", "#F6D47A").replace("#E07E93", "#DDB04F")
CUERNO = _svg('<path d="M8 44c6-14 16-22 24-22s18 8 24 22c-5-2-8-1-10 2-3-6-8-9-14-9s-11 3-14 9c-2-3-5-4-10-2z" fill="#D99A4E"/>'
              '<path d="M22 31l4 8M32 27v10M42 31l-4 8" stroke="#A86A2A" stroke-width="2.5" stroke-linecap="round"/>')
COOKIE = _svg('<circle cx="32" cy="32" r="22" fill="#E9C27D"/><circle cx="32" cy="32" r="22" fill="none" stroke="#C99A4B" stroke-width="3"/>'
              '<circle cx="24" cy="26" r="2" fill="#E0507A"/><circle cx="38" cy="24" r="2" fill="#3BAFDA"/><circle cx="40" cy="38" r="2" fill="#F2C230"/><circle cx="26" cy="40" r="2" fill="#5FB548"/><circle cx="32" cy="32" r="2" fill="#E0507A"/>')
WHEAT = _svg('<path d="M32 58V14" stroke="#C99A4B" stroke-width="3" stroke-linecap="round"/>'
             + "".join(f'<ellipse cx="{32 + s * 6}" cy="{y}" rx="4" ry="7" transform="rotate({s * 30} {32 + s * 6} {y})" fill="#E2B25B"/>' for y in (18, 28, 38) for s in (-1, 1))
             + '<ellipse cx="32" cy="10" rx="3.6" ry="6.5" fill="#E2B25B"/>')
TAMAL = _svg('<path d="M14 54L32 6l18 48c-6 3-12 4-18 4s-12-1-18-4z" fill="#E8D28A"/><path d="M32 6l8 48M32 6l-8 48" stroke="#C9B061" stroke-width="2"/>'
             '<path d="M22 40h20" stroke="#8A5A2B" stroke-width="3" stroke-linecap="round"/>')
CORN = _svg('<path d="M32 6c9 0 14 12 14 26s-5 24-14 24-14-10-14-24S23 6 32 6z" fill="#F2C230"/>'
            + "".join(f'<path d="M20 {y}h24" stroke="#D9A21B" stroke-width="1.5"/>' for y in range(14, 52, 6))
            + '<path d="M32 58c-6-6-16-6-20-20 8 2 14 8 20 20zM32 58c6-6 16-6 20-20-8 2-14 8-20 20z" fill="#5FAE3A"/>')
PUPUSA = _svg('<ellipse cx="32" cy="34" rx="26" ry="20" fill="#E9C98A"/><ellipse cx="32" cy="34" rx="26" ry="20" fill="none" stroke="#C99A4B" stroke-width="2"/>'
              '<circle cx="22" cy="30" r="3" fill="#A86A2A" fill-opacity=".55"/><circle cx="40" cy="38" r="3.5" fill="#A86A2A" fill-opacity=".55"/><circle cx="34" cy="26" r="2" fill="#A86A2A" fill-opacity=".45"/>')
FLAME = _svg('<path d="M32 58c-12 0-20-8-20-19 0-10 7-15 10-24 5 6 4 11 8 14 2-8 6-15 13-21 0 11 11 17 11 31 0 11-9 19-22 19z" fill="#F07A2B"/>'
             '<path d="M32 58c-6 0-10-4-10-10 0-6 5-9 7-14 3 5 8 8 8 14 0 6-2 10-5 10z" fill="#FBD14B"/>')
BOWL = _svg('<path d="M8 30h48c0 14-10 24-24 24S8 44 8 30z" fill="var(--accent)"/><path d="M14 30c2-8 10-12 18-12s16 4 18 12" fill="#F7E7C6"/>'
            '<path d="M40 6l-6 22M48 8l-10 21" stroke="#7A4A22" stroke-width="3" stroke-linecap="round"/>')

# ---------- beauty ----------
SCISSORS = _svg('<g class="blade-a"><path d="M30 34L56 10" stroke="#9AA3AD" stroke-width="5" stroke-linecap="round"/><circle cx="17" cy="47" r="9" fill="none" stroke="var(--accent)" stroke-width="5"/><path d="M24 40l7-7" stroke="var(--accent)" stroke-width="5" stroke-linecap="round"/></g>'
                '<g class="blade-b"><path d="M30 30L56 54" stroke="#C3CAD1" stroke-width="5" stroke-linecap="round"/><circle cx="17" cy="17" r="9" fill="none" stroke="var(--accent)" stroke-width="5"/><path d="M24 24l7 7" stroke="var(--accent)" stroke-width="5" stroke-linecap="round"/></g>'
                '<circle cx="31" cy="32" r="2.5" fill="#555"/>')
COMB = _svg('<rect x="6" y="20" width="52" height="10" rx="4" fill="var(--ink)"/>' + "".join(f'<rect x="{x}" y="28" width="3" height="18" rx="1.5" fill="var(--ink)"/>' for x in range(9, 56, 6)))
RAZOR = _svg('<rect x="28" y="26" width="8" height="32" rx="4" fill="var(--ink)"/><path d="M14 8h36v14a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4z" fill="#C3CAD1"/><path d="M14 22h36" stroke="#8B949E" stroke-width="2"/>')
POLE = ('<svg viewBox="0 0 64 64" aria-hidden="true"><defs><pattern id="pstr" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
        '<rect width="16" height="16" fill="#fff"/><rect width="5" height="16" fill="#D7263D"/><rect x="8" width="5" height="16" fill="#1F4E9C"/>'
        '<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="0 16" dur="1.2s" repeatCount="indefinite" additive="sum"/></pattern></defs>'
        '<rect x="24" y="4" width="16" height="6" rx="3" fill="#9AA3AD"/><rect x="25" y="10" width="14" height="44" rx="2" fill="url(#pstr)"/><rect x="25" y="10" width="14" height="44" rx="2" fill="none" stroke="#9AA3AD" stroke-width="2"/><rect x="24" y="54" width="16" height="6" rx="3" fill="#9AA3AD"/></svg>')
MUSTACHE = _svg('<path d="M32 30c-4-6-12-8-18-4-4 3-6 0-8-2 0 8 6 14 14 13 6-1 10-4 12-7 2 3 6 6 12 7 8 1 14-5 14-13-2 2-4 5-8 2-6-4-14-2-18 4z" fill="var(--ink)"/>')
POLISH = _svg('<rect x="24" y="4" width="16" height="20" rx="3" fill="var(--ink)"/><rect x="14" y="22" width="36" height="36" rx="9" fill="var(--accent)"/>'
              '<rect x="19" y="27" width="6" height="20" rx="3" fill="#fff" fill-opacity=".45"/>')
SPARKLE = _svg('<path d="M32 4c2 16 12 26 28 28-16 2-26 12-28 28-2-16-12-26-28-28 16-2 26-12 28-28z" fill="var(--accent2)"/>')
DROP = _svg('<path d="M32 6c10 14 18 24 18 34a18 18 0 0 1-36 0c0-10 8-20 18-34z" fill="var(--accent)"/><path d="M24 40a8 8 0 0 0 8 8" stroke="#fff" stroke-opacity=".5" stroke-width="3" fill="none" stroke-linecap="round"/>')
HEART = _svg('<path d="M32 56S6 40 6 22c0-9 7-15 14-15 6 0 10 3 12 8 2-5 6-8 12-8 7 0 14 6 14 15 0 18-26 34-26 34z" fill="var(--accent3)"/>')
DRYER = _svg('<path d="M8 22a16 16 0 0 1 16-16h16v32H24A16 16 0 0 1 8 22z" fill="var(--accent)"/><rect x="40" y="10" width="14" height="24" rx="3" fill="var(--ink)"/>'
             '<path d="M22 38h12l-3 22h-6z" fill="var(--accent)"/><circle cx="24" cy="22" r="6" fill="#fff" fill-opacity=".35"/>')
BRUSH = _svg('<rect x="28" y="4" width="8" height="30" rx="4" fill="var(--ink)"/><path d="M24 34h16l-2 14c-1 6-11 6-12 0z" fill="var(--accent)"/>')

# ---------- trades ----------
LEAF = _svg('<path d="M10 54C8 28 26 10 54 8c2 26-16 46-44 46z" fill="#4FA83D"/><path d="M12 52C24 38 34 26 48 14" stroke="#2F7A2B" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
FLOWER = _svg("".join(f'<ellipse cx="32" cy="16" rx="8" ry="12" fill="var(--accent2)" transform="rotate({a} 32 32)"/>' for a in range(0, 360, 72))
              + '<circle cx="32" cy="32" r="8" fill="#F2C230"/>')
SUN = _svg('<g class="spin">' + "".join(f'<path d="M32 2v10" stroke="#F2B544" stroke-width="5" stroke-linecap="round" transform="rotate({a} 32 32)"/>' for a in range(0, 360, 45))
           + '</g><circle cx="32" cy="32" r="14" fill="#F7C84A"/>')
GRASS = _svg('<path d="M8 58c2-14 4-26 2-40 6 10 8 26 6 40M22 58c0-18 4-32 12-46-2 16-4 30-4 46M38 58c2-16 8-30 18-40-6 14-10 26-10 40" fill="#4FA83D" stroke="#3E8A33" stroke-width="2"/>')
MOWER = _svg('<path d="M40 30L58 6" stroke="var(--ink)" stroke-width="4" stroke-linecap="round"/><path d="M8 30h36l4 16H6z" fill="var(--accent)"/>'
             '<rect x="14" y="22" width="16" height="10" rx="3" fill="var(--accent-dark)"/>'
             '<g class="wheel"><circle cx="14" cy="48" r="8" fill="var(--ink)"/><path d="M14 42v12M8 48h12" stroke="#888" stroke-width="2"/></g>'
             '<g class="wheel"><circle cx="42" cy="48" r="8" fill="var(--ink)"/><path d="M42 42v12M36 48h12" stroke="#888" stroke-width="2"/></g>', "0 0 64 64")
GEAR = _svg('<g class="spin">' + _gear(32, 32, 28, 22, 10, "var(--accent)", 9) + '</g>')
GEAR2 = _svg('<g class="spin-r">' + _gear(32, 32, 26, 20, 8, "var(--accent2)", 8) + '</g>')
WRENCH = _svg('<path d="M44 6a14 14 0 0 0-13 19L8 48a6 6 0 0 0 8 8l23-23A14 14 0 0 0 58 20l-8 8-9-3-3-9 8-8c-1-1-1-2-2-2z" fill="#8B949E"/>')
TIRE = _svg('<g class="spin"><circle cx="32" cy="32" r="28" fill="var(--ink)"/><circle cx="32" cy="32" r="14" fill="#C3CAD1"/>'
            + "".join(f'<rect x="30" y="20" width="4" height="8" fill="#8B949E" transform="rotate({a} 32 32)"/>' for a in range(0, 360, 72))
            + "".join(f'<rect x="29" y="4" width="6" height="5" rx="1" fill="#444" transform="rotate({a} 32 32)"/>' for a in range(0, 360, 30)) + '</g>')
CAR = ('<svg viewBox="0 0 96 56" aria-hidden="true"><path d="M8 34c0-6 4-8 10-9l12-11c3-3 6-4 10-4h20c4 0 7 2 10 5l9 10c6 1 9 4 9 9v6c0 2-1 3-3 3H11c-2 0-3-1-3-3z" fill="var(--accent)"/>'
       '<path d="M33 16h12v10H23zM49 16h10c2 0 4 1 5 3l6 7H49z" fill="#CFE6F7"/><rect x="80" y="32" width="6" height="4" rx="2" fill="#F7C84A"/>'
       '<g class="wheel"><circle cx="26" cy="44" r="9" fill="var(--ink)"/><circle cx="26" cy="44" r="4" fill="#C3CAD1"/><path d="M26 36v16M18 44h16" stroke="#555" stroke-width="1.5"/></g>'
       '<g class="wheel"><circle cx="72" cy="44" r="9" fill="var(--ink)"/><circle cx="72" cy="44" r="4" fill="#C3CAD1"/><path d="M72 36v16M64 44h16" stroke="#555" stroke-width="1.5"/></g></svg>')
HAMMER = _svg('<rect x="29" y="22" width="7" height="38" rx="3" fill="#A86A2A"/><path d="M14 10h30l8 6-2 8H14z" fill="#8B949E"/>')
ROLLER = _svg('<rect x="8" y="6" width="44" height="16" rx="6" fill="var(--accent)"/><path d="M52 14h6v16H34v8" stroke="var(--ink)" stroke-width="4" fill="none" stroke-linejoin="round"/><rect x="30" y="38" width="8" height="22" rx="3" fill="var(--ink)"/>')
HOUSE = _svg('<path d="M8 30L32 8l24 22" stroke="var(--accent)" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 28v28h36V28" fill="var(--accent2)"/><rect x="27" y="38" width="10" height="18" fill="var(--ink)"/>')
BOLT = _svg('<path d="M36 4L12 36h16l-4 24 26-34H34z" fill="#F2C230"/>')
PIPE = _svg('<path d="M10 20h26a10 10 0 0 1 10 10v24" stroke="#8B949E" stroke-width="10" fill="none"/><rect x="4" y="13" width="8" height="14" rx="2" fill="#6B747E"/><rect x="39" y="50" width="14" height="8" rx="2" fill="#6B747E"/>')

# ---------- cleaning ----------
BUBBLE = _svg('<circle cx="32" cy="32" r="24" fill="#BFE6FA" fill-opacity=".55" stroke="#8ACFF2" stroke-width="2"/><path d="M20 24a14 14 0 0 1 10-8" stroke="#fff" stroke-width="4" stroke-linecap="round" fill="none"/>')
SPRAY = _svg('<path d="M20 22h20l6 34H14z" fill="var(--accent)"/><path d="M22 10h18l8 6H22z" fill="var(--ink)"/><rect x="26" y="16" width="10" height="7" fill="var(--ink)"/>'
             '<circle cx="54" cy="10" r="2" fill="#8ACFF2"/><circle cx="58" cy="16" r="2" fill="#8ACFF2"/><circle cx="54" cy="20" r="1.6" fill="#8ACFF2"/>')
SQUEEGEE = _svg('<rect x="6" y="28" width="52" height="8" rx="3" fill="var(--accent)"/><rect x="6" y="34" width="52" height="4" rx="2" fill="var(--ink)"/><rect x="29" y="4" width="6" height="26" rx="3" fill="var(--ink)"/>')

MOON = _svg('<path d="M40 6a26 26 0 1 0 18 40A22 22 0 0 1 40 6z" fill="#F6D47A"/><circle cx="26" cy="26" r="3" fill="#E9BD55"/><circle cx="20" cy="40" r="2.2" fill="#E9BD55"/><circle cx="32" cy="48" r="2.6" fill="#E9BD55"/>')
STAR = _svg('<path d="M32 6l7 17 18 2-14 12 4 18-15-9-15 9 4-18L7 25l18-2z" fill="var(--accent2)"/>')
LEAF_LINE = _svg('<path d="M10 54C8 28 26 10 54 8c2 26-16 46-44 46z" fill="none" stroke="var(--accent)" stroke-width="2.5"/><path d="M12 52C24 38 34 26 48 14M26 38l-6-10M32 32l8-2M38 24l-4-10" stroke="var(--accent)" stroke-width="2" fill="none" stroke-linecap="round"/>')

MOTIFS = {
    "taco":   dict(floaters=[TACO, CHILI, LIME, LEAF_C, AVOCADO, TACO], ride=TACO, trail="salsa", tick=CHILI),
    "bakery": dict(floaters=[CONCHA, CUERNO, COOKIE, CONCHA_Y, WHEAT, COOKIE], ride=CONCHA, trail="sprinkles", tick=CONCHA_Y),
    "tamal":  dict(floaters=[TAMAL, CORN, CHILI, LIME, TAMAL, AVOCADO], ride=TAMAL, trail="salsa", tick=CORN),
    "pupusa": dict(floaters=[PUPUSA, CORN, CHILI, LIME, PUPUSA, LEAF_C], ride=PUPUSA, trail="salsa", tick=CORN),
    "grill":  dict(floaters=[FLAME, BOWL, CHILI, FLAME, SPARKLE, LEAF_C], ride=FLAME, trail="fire", tick=FLAME),
    "barber": dict(floaters=[SCISSORS, COMB, RAZOR, MUSTACHE, POLE, SPARKLE], ride=SCISSORS, trail="cut", tick=MUSTACHE),
    "nails":  dict(floaters=[POLISH, SPARKLE, DROP, HEART, BRUSH, SPARKLE], ride=BRUSH, trail="paint", tick=SPARKLE),
    "hair":   dict(floaters=[SCISSORS, DRYER, COMB, SPARKLE, HEART, SPARKLE], ride=SCISSORS, trail="cut", tick=SPARKLE),
    "lawn":   dict(floaters=[LEAF, FLOWER, SUN, GRASS, LEAF, FLOWER], ride=MOWER, trail="grass", tick=LEAF),
    "auto":   dict(floaters=[GEAR, WRENCH, TIRE, GEAR2, BOLT, GEAR], ride=CAR, trail="road", tick=GEAR),
    "tools":  dict(floaters=[HAMMER, WRENCH, HOUSE, BOLT, PIPE, GEAR2], ride=ROLLER, trail="paint", tick=HAMMER),
    "moon":   dict(floaters=[MOON, CONCHA, STAR, TACO, STAR, CONCHA_Y], ride=MOON, trail="sprinkles", tick=STAR),
    "leafline": dict(floaters=[LEAF_LINE, LEAF_LINE, LEAF_LINE, LEAF_LINE, LEAF_LINE, LEAF_LINE], ride=LEAF_LINE, trail="grass", tick=LEAF_LINE),
    "paint":  dict(floaters=[ROLLER, DROP, BRUSH, SPARKLE, DROP, ROLLER], ride=ROLLER, trail="paint", tick=DROP),
    "flower": dict(floaters=[FLOWER, LEAF, SPARKLE, HEART, FLOWER, SPARKLE], ride=FLOWER, trail="grass", tick=FLOWER),
    "clean":  dict(floaters=[BUBBLE, SPARKLE, SPRAY, BUBBLE, SPARKLE, BUBBLE], ride=SQUEEGEE, trail="shine", tick=SPARKLE),
}


def pick(b):
    """Choose a motif from the lead (override with style.motif)."""
    st = b.get("style") or {}
    if st.get("motif") in MOTIFS:
        return st["motif"]
    cat = b.get("category", "")
    tags = [t.lower() for t in b.get("stock_tags") or []]
    slug = b.get("slug", "")
    if cat in ("food", "food_plain"):
        if "panaderia" in slug or (tags and tags[0] in ("bakery", "pan dulce")):
            return "bakery"
        if tags and tags[0] == "pupusas":
            return "pupusa"
        if tags and tags[0] == "tamales":
            return "tamal"
        if cat == "food_plain":
            return "grill"
        return "taco"
    if cat == "salon":
        if "barber" in tags:
            return "barber"
        if "nails" in tags or "manicure" in tags:
            return "nails"
        return "hair"
    if cat == "trades":
        if any(t in tags for t in ("landscaping", "lawn", "sod")):
            return "lawn"
        if any(t in tags for t in ("auto repair", "mechanic")):
            return "auto"
        return "tools"
    if "cleaning" in tags:
        return "clean"
    return "tools"
