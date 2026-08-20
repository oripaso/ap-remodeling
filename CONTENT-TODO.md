# A&P Remodeling — content to replace before/after launch

Everything below is deliberately left empty or marked. Nothing on the site claims a
license number, review count, years in business, warranty, award or project count,
because none of that was verifiable from the source material. Fill these in and the
site gets noticeably stronger.

## 1. Credentials strip (index.html — search `EDIT ME`)
A commented-out `VERIFIED-CREDENTIALS VARIANT` block sits directly under the live strip.
Fill in and swap once you can verify:
- CSLB license number
- Insurance (general liability / workers' comp)
- Google rating + review count
- Years in business / "serving Los Angeles since ____"
- Workmanship warranty terms
- Projects completed

## 2. Reviews (index.html — section `#reviews`)
Currently an honest empty state. A `REAL REVIEWS TEMPLATE` is commented out beneath it.
Only paste reviews people actually wrote — name, neighborhood, project type, rating, text.

## 3. Project cards (index.html — section `#projects`)
The photographs are licensed stock and are labelled as reference imagery on the page.
Replace each `<img>` with real A&P job photography and the disclaimer paragraph
(`.projnote`) can be deleted. Card structure supports: image, category tag, neighborhood
tag, title, description, scope list.

## 4. Before / after (index.html — section `#beforeafter`)
Swap the two images for a real matched pair from one job, then update the
`.ba__meta` list (location, work performed) and remove the "reference imagery" note.

## 5. Business hours + social (index.html footer — search `EDIT ME`)
Add once confirmed. If you add hours, also add `openingHoursSpecification` to the
JSON-LD block in `<head>`.

## 6. Form delivery (main.js — search `BUSINESS_EMAIL`)
The estimate form currently opens a pre-filled SMS to 310-633-5777. Set
`BUSINESS_EMAIL = 'you@aproofla.com'` and it switches to email instead. For a real
inbox + photo attachments, point the form at a service like Formspree or Basin —
that is a ~10 line change in `submit()`.

## 7. Privacy policy (privacy.html)
Plain-language starting point. Have it reviewed, and update it if you add analytics,
ad pixels, a CRM or a form backend.

## 8. Photography direction (when shooting real jobs)
Shoot: golden hour exteriors, roof detail close-ups, crews working, before/after pairs
from the same angle and lens, finished interiors. Landscape 4:3 and portrait 3:4 both
get used by the layout.
