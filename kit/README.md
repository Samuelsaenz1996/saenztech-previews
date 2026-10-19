# Saenztech mockup kit

Builds a multi-page "design concept" website for a lead from a JSON file, then screenshots every page.
Published sites live in `/previews/<slug>/` (Home) with one folder per page, served by GitHub Pages.

Pages by category (a page only appears when there is real content for it):

| category | pages |
|---|---|
| food / food_plain | Home · Menu (`menu/`) · Gallery (4+ photos) · Hours & location (`visit/`) · Contact |
| salon | Home · Services · Gallery (4+ photos) · Contact (booking link as main button) |
| trades | Home · Services · Projects (4+ photos) · Contact with quote form |
| events | Home · Packages · Gallery (4+ photos) · Contact with quote form |
| services | Home · Services · About (if `about`) · Contact |

Every page has the header with logo + tabs (hamburger menu on phones), ES/EN switch that is remembered across pages, a call/book/quote button, and a full footer. The contact form is a demo (shows a note instead of sending).

## Run

```bash
cd kit
npm ci || npm i            # fonts + playwright (uses the preinstalled Chromium)
pip install jinja2 --break-system-packages 2>/dev/null || true
python3 build.py /tmp/leads/<slug>.json ../previews --kit . --fonts node_modules/@fontsource
node shot.js ../previews/<slug>      # writes preview.png, preview-full.png, desktop.png
```

`shot.js` prints JSON: check `fonts` is non-empty and `horizontalOverflow` is false (`overflowPages` lists any broken page).
It writes preview.png / preview-full.png / desktop.png for Home and `shots/<page>-phone.png` + `shots/<page>-desktop.png` for every page (shots/ is git-ignored).
Open `preview.png` and at least one inner page shot and look at them before publishing.

Keep lead JSON files in /tmp, not in the repo (the repo is public).

## Lead JSON

Text fields can be a plain string (same in both languages) or `{"es": "...", "en": "..."}`.
`headline` may contain one `<em>...</em>` for the accent words. Use `&amp;` for "&" inside headline HTML.

| Field | Required | Notes |
|---|---|---|
| slug | yes | lowercase-hyphens, business + city, e.g. `chepos-pasadena` |
| business | yes | exact business name |
| category | yes | `food`, `food_plain` (non-Mexican food), `salon`, `trades`, `events`, `services` |
| lang | yes | primary language: `es` or `en` |
| bilingual | no | default true (ES/EN switch) |
| city | yes | "Pasadena, TX" |
| subtitle | yes | short line under the logo, e.g. "Food truck · Pasadena, TX" |
| eyebrow | no | small pill above headline (a real, verified fact) |
| headline | yes | 4–9 words |
| lead | yes | one sentence, only verified details |
| phone / phone_display | no | `+18328820246` / `(832) 882-0246` |
| address | no | full street address if verified; enables map + directions |
| service_area | no | for businesses without a public address |
| booking_url / booking_label | no | their real Booksy/Vagaro/ordering/quote link |
| rating | no | `{"value": 4.9, "count": 99, "source": "Restaurantji"}` only if verified |
| items | no | up to 6 `{"name", "desc", "price"}`; only real dishes/services; omit price unless verified |
| themes | no | 3–4 short themes that really appear in their reviews |
| hours | no | `[{"day": 2, "es": "Martes", "en": "Tuesday", "time": "6–11 pm"}]` (day 0=Sun) |
| email | no | verified public email (shown on Contact and footer) |
| socials | no | `{"facebook": url, "instagram": url, "tiktok": url, "yelp": url, "google": url}` only real profiles |
| order_url / order_label | no | real online ordering link (becomes the main button) |
| items[].group | no | menu/service section name, e.g. `{"es":"Postres","en":"Desserts"}` |
| items[].photo | no | URL or local path of a photo of that item (only if allowed, see Photos) |
| items_title / items_note | no | override the menu/services page title and intro |
| about | no | string or list of paragraphs (bilingual objects ok) with VERIFIED facts only; adds an About page |
| photos | no | `[{"src": url-or-path, "alt": {...}, "credit": "...", "sample": true}]` first = hero, rest = gallery |
| stock_tags | no | words to pick matching stock photos, e.g. `["tacos","taqueria"]` |
| stock | no | default true; false disables stock photos |

## Photos

- Use free stock photos (Unsplash / Pexels license) that match the business type, marked `"sample": true`.
  They show a small "Foto de muestra / Sample photo" tag, and the gallery explains they get replaced with the owner's photos.
- A starter stock library lives in `kit/stock/<category>/` (food, trades, salon) with `manifest.json` = `[{"file","alt","credit","source","tags"}]`.
  The builder fills up to 7 photos from it automatically when the lead has fewer. Set `stock_tags` on the lead
  (e.g. `["tacos","birria"]`, `["bakery","pan dulce"]`, `["roofing"]`, `["hair"]`, `["nails"]`) so it picks matching photos;
  photos tagged `explicit` (bakery) are only used when asked for. If 3+ photos match the tags, only matching photos are used.
- Item photos are matched automatically when a photo tag appears in the item name (e.g. "Burritos" gets a burrito photo).
- To add photos for a new kind of business, download from images.pexels.com
  (`https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=1200`), look at each one,
  save it into the right `kit/stock/<category>/` folder and add it to that manifest with honest tags. Commit new stock photos with the day's previews.
- Do NOT copy photos from the business's Facebook/Instagram/Google/Yelp onto these public pages.
- Without any photos the hero shows a designed sign with the business name, and the gallery page is skipped.

Never invent reviews, quotes, prices, menu items, awards, years in business or photos.
Placeholders are filled automatically when there are fewer than 4 items.
