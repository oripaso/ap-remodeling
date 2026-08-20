# What still needs real data

Nothing on this site is invented. That means a few places are deliberately
empty rather than filled with plausible-sounding text. Each one makes the
site measurably stronger the moment you have the real answer.

## 1. Credentials  (`build.py` → `trust()`, search `EDIT ME`)
The strip under the hero shows only what A&P has published about itself.
Add, once you can evidence them:
- CSLB licence number
- Liability + workers' compensation insurance
- Google rating and review count
- Years in business
- Workmanship warranty terms

## 2. Reviews  (not present)
There is no reviews section, on purpose. A&P has a Yelp page but no reviews
were verifiable, and a section saying "reviews coming soon" advertises the
gap. Collect three real reviews (name, neighborhood, project type, text) and
a testimonial section can be added in minutes.

## 3. Owner / founder  (`build.py` → `page_home()` and `page_about()`)
Both carry a placeholder that reads "Add owner name". Replace with the real
name, role and a portrait photograph. This is the single highest-value
addition on the whole site — a face converts better than any copy.

## 4. Project detail  (`build.py` → `PROJECTS`)
Photographs are real. `location`, `materials`, `timeline`, `budget`,
`condition`, `scope` and `solution` are `None` and therefore invisible.
Fill them in per project and the cards and case studies populate themselves.

## 5. Before / after  (`build.py` → `BEFORE_AFTER = None`)
The component is built and styled. It is switched off because there is no
matched pair from a single job — pairing two different houses would
misrepresent the work. Supply one before and one after photo of the same
property and set:

    BEFORE_AFTER = dict(before=URL, after=URL, before_alt='…', after_alt='…',
                        project='…', location='…', work='…')

## 6. Photography hosting  ⚠️ important
Project photos load from `api.support-usa.com`, where A&P published them.
If that host changes or goes away, the images break. Download the originals
and commit them to `/img` in this repo, then update `PHOTO` in `build.py`.
Self-hosted images are also faster.

## 7. Lead delivery  (`main.js` → `LEAD.ENDPOINT`)
Currently empty, so the form opens a pre-filled text message. Point it at a
real endpoint and leads arrive in an inbox or CRM with no lost submissions.

## 8. Business hours and social  (`build.py` → `footer()`, search `EDIT ME`)
Add once confirmed. If you add hours, also add `openingHoursSpecification`
to `biz_ld()` so they show in Google.

## 9. Legal  (`privacy.html`, `terms.html`)
Plain-language starting points. Have them reviewed, and update privacy if you
add analytics, ad pixels, a CRM or a form backend.
