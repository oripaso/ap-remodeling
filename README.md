# A&P Remodeling and Consulting

Roofing, exterior construction and remodeling in Los Angeles and the San Fernando Valley.

**Live:** https://oripaso.github.io/ap-remodeling/ · **Phone:** 310-633-5777
**Yard:** 6323 Morella Ave, Los Angeles, CA 91606

## This is a generated site

Do not hand-edit the HTML — it is built from components so no page duplicates
another. Source lives in the `site/` build:

| File | What it is |
|---|---|
| `build.py` | Data + components + every page. Edit here. |
| `static/styles.css` | The whole design system, one file |
| `static/main.js` | All interactions, zero dependencies |

Rebuild: `python3 build.py` → writes `dist/`.
`BASE=/ap-remodeling EXT=.html` are env vars — set `BASE='' EXT=''` for a root
domain with clean URLs.

## Where the content came from

Everything on the site is A&P's own material:

- **Photography** — five job photographs published by A&P on its own site
- **Copy** — positioning, service list and about text from A&P's own pages
- **Contact** — from aproofla.com

Nothing is invented. See `CONTENT-TODO.md` for what still needs real data.

## Editing projects

`PROJECTS` in `build.py` is the project store. Fields set to `None` do not
render at all, so a project never claims a location, budget or timeline that
was not supplied. Fill a field in and it appears on the card and the case
study page automatically.

## Lead delivery

`main.js` → `LEAD.ENDPOINT`. Point it at Formspree / Basin / Zapier / Make /
a Google Apps Script webhook and leads POST as JSON. Left empty, the form
opens a pre-filled text or email so no lead is lost.

No build step, no dependencies, ~20 KB gzipped per page.
