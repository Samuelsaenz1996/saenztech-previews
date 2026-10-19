# Saenztech mockup kit

Builds a one-page "design concept" site for a lead from a JSON file, then screenshots it.
Published pages live in `/previews/<slug>/` and are served by GitHub Pages.

## Run

```bash
cd kit
npm ci || npm i            # fonts + playwright (uses the preinstalled Chromium)
pip install jinja2 --break-system-packages 2>/dev/null || true
python3 build.py /tmp/leads/<slug>.json ../previews --kit . --fonts node_modules/@fontsource
node shot.js ../previews/<slug>      # writes preview.png, preview-full.png, desktop.png
```

`shot.js` prints JSON: check `fonts` is non-empty and `horizontalOverflow` is false.
Open `preview.png` and look at it before publishing.

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
| photo_label | no | override the hero photo placeholder text |

Never invent reviews, quotes, prices, menu items, awards, years in business or photos.
Placeholders are filled automatically when there are fewer than 4 items.
