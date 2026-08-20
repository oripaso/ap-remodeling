# A&P Remodeling and Consulting

Website for A&P Remodeling and Consulting — roofing, exterior construction and
full-home remodeling in Los Angeles and the San Fernando Valley.

**Live:** https://oripaso.github.io/ap-remodeling/
**Phone:** 310-633-5777
**Address:** 6323 Morella Ave, Los Angeles, CA 91606

## Structure

| File | What it is |
|---|---|
| `index.html` | Home page |
| `services/*.html` | Four SEO service pages |
| `privacy.html`, `404.html` | Legal + not-found |
| `styles.css` | Whole design system, one file |
| `main.js` | All interactions, no dependencies |
| `CONTENT-TODO.md` | **Read this** — real data still to fill in |

No build step. Static files. ~27 KB gzipped for HTML+CSS+JS.

## Editing

Change a file, commit, push — GitHub Pages redeploys in about a minute.

## Custom domain

To serve this at `aproofla.com`: add a `CNAME` file containing `aproofla.com`,
then point the DNS at GitHub Pages (four A records for the apex, one CNAME for `www`).
