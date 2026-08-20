# -*- coding: utf-8 -*-
"""A&P Remodeling and Consulting — static site build.
Components + data in, pages out. No page duplicates another page's markup."""
import os, json, shutil, time, pathlib

OUT   = pathlib.Path('/root/site/dist')
BASE  = os.environ.get('BASE', '/ap-remodeling')   # '' for a root domain
EXT   = os.environ.get('EXT', '.html')             # '' when the host does clean URLs
SITE  = os.environ.get('SITE', 'https://oripaso.github.io/ap-remodeling')
VER   = str(int(time.time()))

# ---------------------------------------------------------------- business
BIZ = dict(
    name='A&P Remodeling and Consulting',
    phone='310-633-5777', tel='+13106335777',
    street='6323 Morella Ave', city='Los Angeles', region='CA', zip='91606',
    maps='https://maps.google.com/?q=6323+Morella+Ave,+Los+Angeles,+CA+91606',
    yelp='https://www.yelp.com/biz/a-and-p-remodeling-and-consulting-north-hollywood',
    logo='https://api.support-usa.com/brand/files/52/refined_WhatsApp_Image_2026-07-20_at_8.16.10_PM.png',
)
IMG = 'https://api.support-usa.com/brand/files/52/'

# ---------------------------------------------------------------- real photography
# Every photograph below is A&P's own, published by the company on its own site.
# Descriptions state only what is visible in the frame — no invented location,
# date, budget or client.
PHOTO = {
 'estate':   dict(u=IMG+'WhatsApp_Image_2026-07-21_at_10.21.05_PM__1_.jpeg', w=1600, h=1200, pos='center 38%'),
 'finished': dict(u=IMG+'WhatsApp_Image_2026-07-21_at_10.21.07_PM.jpeg',     w=1600, h=1200, pos='center 55%'),
 'tearoff':  dict(u=IMG+'WhatsApp_Image_2026-07-21_at_10.21.05_PM.jpeg',     w=1600, h=1200, pos='center 40%'),
 'aerial':   dict(u=IMG+'WhatsApp_Image_2026-07-21_at_10.21.06_PM.jpeg',     w=1280, h=720,  pos='center 45%'),
 'tile':     dict(u=IMG+'WhatsApp_Image_2026-07-21_at_10.21.02_PM.jpeg',     w=1600, h=898,  pos='center 40%'),
}
def PU(k):  return PHOTO[k]['u']
def PAR(k): return '%d/%d' % (PHOTO[k]['w'], PHOTO[k]['h'])

ALT = {
 'estate':   'A&P crew stripping the roof of a large traditional Los Angeles home with dormer windows and a brick driveway',
 'finished': 'Completed composition shingle roof on an A&P project, ridge line running toward a pool and palm trees',
 'tearoff':  'A&P roofer climbing a ladder on a white two-storey home during a roof tear-off, old shingles stacked above',
 'aerial':   'Aerial view of an A&P re-roof in progress, crew working on the pitched section beside a freshly coated flat roof',
 'tile':     'Aerial view of a terracotta tile roof alongside a newly finished white low-slope roof on an A&P project',
}

# ---------------------------------------------------------------- projects (the CMS)
# Unverified fields are left as None. Nothing renders for a None field, so the
# page never claims a location, budget, timeline or client that was not supplied.
# Fill these in and the case study pages fill in with them.
PROJECTS = [
 dict(slug='estate-reroof', n='01', key='estate',
      title='Estate re-roof, stripped to the deck',
      blurb='A full tear-off on a large traditional home. Old material off, deck inspected, new system laid from the eave up.',
      layout='wide',
      location=None, project_type='Roof replacement', materials=None, timeline=None, budget=None,
      condition=None, scope=None, solution=None,
      gallery=['tearoff'],
      caption='Crew working the upper roof during tear-off.'),
 dict(slug='shingle-reroof', n='02', key='finished',
      title='Composition shingle, finished',
      blurb='Ridge cap set and the field closed. The line down the hip is where a re-roof is judged.',
      layout='split',
      location=None, project_type='Roof replacement', materials='Composition shingle', timeline=None, budget=None,
      condition=None, scope=None, solution=None,
      gallery=[],
      caption='Completed roof looking down the ridge.'),
 dict(slug='tile-and-flat', n='03', key='tile',
      title='Tile roof and low-slope, one property',
      blurb='Two roof systems on one house. The pitched tile and the flat section have to be detailed where they meet.',
      layout='splitR',
      location=None, project_type='Tile & low-slope roofing', materials=None, timeline=None, budget=None,
      condition=None, scope=None, solution=None,
      gallery=['aerial'],
      caption='Aerial of the finished low-slope section beside the tile.'),
 dict(slug='aerial-reroof', n='04', key='aerial',
      title='Re-roof in progress, from above',
      blurb='Pitched section being laid while the adjoining flat roof is already coated. One crew, one schedule.',
      layout='wide',
      location=None, project_type='Roof replacement', materials=None, timeline=None, budget=None,
      condition=None, scope=None, solution=None,
      gallery=['finished'],
      caption='Crew on the pitched roof mid-installation.'),
]

# ---------------------------------------------------------------- before / after
# Set this to a dict with real matched images from ONE job and the section renders.
# Left as None deliberately: A&P has not supplied a matched before/after pair, and
# pairing two different houses would misrepresent the work.
BEFORE_AFTER = None

# ---------------------------------------------------------------- disciplines
DISC = [
 dict(slug='roofing', n='01', name='Roofing', key='finished',
      lede='The system everything else depends on.',
      items=['Roof replacement','Roof repair','Roof maintenance','Leak diagnosis & flashing'],
      h1='Roofing that holds through a Los Angeles winter.',
      sub='Replacement, repair and maintenance across Los Angeles and the San Fernando Valley — diagnosed on the roof, not from the driveway.',
      title='Roofing Contractor in Los Angeles | Roof Repair &amp; Replacement — A&amp;P',
      desc='Roof replacement, roof repair and roof maintenance across Los Angeles and the San Fernando Valley. Shingle, tile and low-slope systems. Free consultation — 310-633-5777.',
      body=[('What A&amp;P does on a roof',
             ['Most roof failures in Los Angeles are not the field of the roof. They are the edges — flashing at a chimney, a valley that was never lapped correctly, a vent boot dried out by ten summers of Valley heat.',
              'Those details are where we start.']),
            ('Repair or replace',
             ['A contractor should be willing to tell you the repair is enough. Age of the system, condition of the deck and how many layers are already up there decide that answer — and you get it in writing.']),
            ],
      list_title='Roofing services',
      lists=['Roof replacement','Roof repair','Roof maintenance','Tear-off & deck inspection','Flashing, valleys & vent boots','Leak diagnosis','Composition shingle','Tile roofing','Low-slope & flat systems','Restoration']),
 dict(slug='exterior', n='02', name='Exterior', key='tile',
      lede='Paint, stucco and the envelope that sheds water.',
      items=['Exterior paint','Trim paint','Stucco repair','Gutters & siding'],
      h1='The envelope is one system. Treat it that way.',
      sub='Exterior paint, trim, stucco repair, gutters and siding — handled together so the finish lasts.',
      title='Exterior Painting, Stucco &amp; Siding in Los Angeles — A&amp;P Remodeling',
      desc='Exterior painting, trim paint, stucco repair, gutters and siding across Los Angeles and the San Fernando Valley. Free consultation — 310-633-5777.',
      body=[('Why these go together',
             ['Water hits the wall, runs down the surface and is supposed to leave through the gutter. Paint is what stops the wall drinking any of it.',
              'Repaint over failed stucco and you have bought two years. Do it in one scope and it lasts.']),
            ('The prep nobody sees',
             ['Exterior finishes in Los Angeles fail from ultraviolet at the top of the wall and moisture at the bottom. Both are prep problems before they are paint problems, so prep is priced as part of the job.'])],
      list_title='Exterior services',
      lists=['Exterior paint','Trim paint','Stucco repair','Siding installation & repair','Seamless gutters','Gutter repair & re-pitching','Fascia & trim','Surface prep & priming','Caulking & sealing','Restoration']),
 dict(slug='remodeling', n='03', name='Remodeling', key='estate',
      lede='General contracting, with one point of contact.',
      items=['Home remodeling','General contracting','Foundation repair','Attic insulation'],
      h1='One contractor. One schedule. One number to call.',
      sub='Home remodeling and general contracting across Los Angeles and the San Fernando Valley.',
      title='Home Remodeling &amp; General Contracting in Los Angeles — A&amp;P',
      desc='Home remodeling, general contracting, foundation repair and attic insulation across Los Angeles and the San Fernando Valley. Free consultation — 310-633-5777.',
      body=[('What general contracting actually buys you',
             ['On a remodel the expensive failures are rarely craftsmanship. They are sequencing — a trade booked for a day the work is not ready, an order placed against a measurement that changed.',
              'Someone has to hold that sequence. Hire trades individually and that someone is you.']),
            ('Scope before demolition',
             ['What is included, what is not, and what would move the number — in writing, before anything starts.'])],
      list_title='Remodeling services',
      lists=['Home remodeling','General contracting','Interior renovation','Foundation repair','Attic insulation','Restoration','Trade coordination','Scheduling & sequencing','Materials management','Site protection & cleanup']),
 dict(slug='decks', n='04', name='Outdoor Living', key='aerial',
      lede='Decks, hardscape and the ground around the house.',
      items=['Decks & porches','Hardscape','Landscape','Solar panel installation'],
      h1='Where the house stops and the yard begins.',
      sub='Decks, porches, hardscape, landscape and solar across Los Angeles and the San Fernando Valley.',
      title='Decks, Hardscape &amp; Solar in Los Angeles — A&amp;P Remodeling',
      desc='Deck and porch construction, hardscape, landscape and solar panel installation across Los Angeles and the San Fernando Valley. Free consultation — 310-633-5777.',
      body=[('Structure first',
             ['Almost every deck that feels bouncy has a framing problem, not a decking problem. Ledger attachment, post bases in soil, missing flashing where the deck meets the house.',
              'We check those before quoting a surface.']),
            ('Built for Valley sun',
             ['Relentless ultraviolet, wide daily temperature swings, then a short intense wet season. Material and fixing choices follow from that, not from a catalogue.'])],
      list_title='Outdoor services',
      lists=['Deck construction & repair','Porch repair & additions','Hardscape','Landscape','Solar panel installation','Framing & ledger repair','Railings & stairs','Exterior structures','Resurfacing','Site clearing']),
]

AREAS = ['North Hollywood','Studio City','Valley Village','Sherman Oaks','Van Nuys','Toluca Lake',
         'Burbank','Glendale','Encino','Tarzana','Woodland Hills','Northridge','Hollywood','Sun Valley']

WHY = [
 ('01','Clear scope before construction','You know what is included, what the timeline looks like and what happens next — in writing.'),
 ('02','One point of contact','No homeowner should be coordinating five trades. That is our job.'),
 ('03','Respect for your home','The property is protected while the work happens and the site is cleared before we leave.'),
 ('04','Communication throughout','You hear what is next from us, not after chasing us.'),
 ('05','Built for Los Angeles','Valley heat, low-slope roofs, stucco and a wet season that arrives all at once. The local failure points are the ones we plan for.'),
]

PROCESS = [
 ('01','Tell us about the project','Share what you are planning. A call or the form — no pressure at this stage.','tearoff'),
 ('02','On-site consultation','We inspect the property and understand the real scope.','estate'),
 ('03','Scope, estimate and timeline','Clear expectations, in writing, before work begins.','aerial'),
 ('04','Build','Construction, communication and a clean site on completion.','finished'),
]

FAQ = [
 ('What does a consultation cost?','Nothing. A&amp;P provides a free consultation and a written estimate, with no obligation.'),
 ('Which areas do you serve?','Los Angeles and the San Fernando Valley, from a yard at 6323 Morella Ave in North Hollywood. If your address is not on our list, call and ask.'),
 ('I have a roof leak right now.','Call 310-633-5777 and say it is active. Water moves from the roof into sheathing, insulation and drywall, and the repair grows with every day it runs.'),
 ('Do you take small repairs?','Yes. A gutter re-pitch is as welcome as a full tear-off.'),
 ('What roofing materials do you work with?','Composition shingle, tile, and low-slope and flat systems. If you are not sure what is on your house, we identify it on the visit.'),
 ('Can one company handle the roof and the remodel?','Yes. That is what general contracting is for — one scope, one schedule, one point of contact.'),
 ('How long will my project take?','It depends on scope, permits and material lead times. You get an estimated schedule in writing alongside the price.'),
 ('How do payments work?','Terms are set out in the written estimate before work begins. Call 310-633-5777 to discuss terms for your project.'),
]

# ================================================================ helpers
def url(p=''):
    if p == '': return (BASE + '/index' + EXT) if EXT else (BASE + '/')
    return BASE + '/' + p + EXT

def asset(p): return BASE + '/' + p + '?v=' + VER
def canon(p): return SITE + ('/' if p == '' else '/' + p + EXT)

ARROW  = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m0 0-6-6m6 6-6 6"/></svg>'

def fr(key, ratio_cls='', alt=None, sizes='100vw', eager=False, zoom=True, ar=None, cover_pos=None):
    """Image frame. Defaults to the photograph's own aspect ratio and focal point,
    so a landscape job photo is never squeezed into a portrait crop."""
    p = PHOTO[key]
    a = alt if alt is not None else ALT.get(key, '')
    cls = 'fr' + (' fr--z' if zoom else '') + ((' ' + ratio_cls) if ratio_cls else '')
    style = '--ar:%s;--pos:%s' % (ar or PAR(key), cover_pos or p['pos'])
    ld = ('loading="eager" fetchpriority="high"' if eager else 'loading="lazy"')
    return ('<figure class="%s" style="%s">'
            '<img src="%s" alt="%s" width="%d" height="%d" %s decoding="async" sizes="%s">'
            '</figure>') % (cls, style, p['u'], a, p['w'], p['h'], ld, sizes)

def head(title, desc, path, og_key='estate', extra='', page_class=''):
    ld = extra
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon(path)}">
<meta name="theme-color" content="#F3F0EA">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon(path)}">
<meta property="og:image" content="{PHOTO[og_key]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://api.support-usa.com" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{asset('styles.css')}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%23111111'/%3E%3Cpath d='M22 64 50 30l28 34' fill='none' stroke='%23B95432' stroke-width='9' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
{ld}
</head>
<body{(' class="' + page_class + '"') if page_class else ''}>
<a class="skip" href="#main">Skip to main content</a>'''

NAV = [('Projects','projects'),('Services','services'),('About','about'),
       ('Process','process'),('Areas','areas'),('Contact','contact')]

def header(active=''):
    links = ''.join(
        '<a href="%s"%s>%s</a>' % (url(p), ' aria-current="page"' if p == active else '', n)
        for n, p in NAV)
    return f'''
<header class="hdr" id="hdr">
  <div class="hdr__in">
    <a class="brand" href="{url('')}" aria-label="{BIZ['name']} — home">
      <img src="{BIZ['logo']}" alt="{BIZ['name']}" width="120" height="99">
    </a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <div class="hdr__r">
      <a class="tel" href="tel:{BIZ['tel']}">{BIZ['phone']}</a>
      <a class="btn btn--sm" href="{url('contact')}">Start a Project</a>
      <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu"><i></i><i></i></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <nav class="drawer__nav" aria-label="Mobile">
    {''.join('<a href="%s"><em>%02d</em> %s</a>' % (url(p), i+1, n) for i,(n,p) in enumerate(NAV))}
    <a href="{url('contact')}"><em>07</em> Start a Project</a>
  </nav>
  <div class="drawer__foot">
    <a class="big" href="tel:{BIZ['tel']}">{BIZ['phone']}</a>
    <p>{BIZ['street']}, {BIZ['city']}, {BIZ['region']} {BIZ['zip']}<br>Los Angeles &amp; the San Fernando Valley</p>
  </div>
</div>'''

def footer():
    svc = ''.join('<li><a href="%s">%s</a></li>' % (url('services/' + d['slug']), d['name']) for d in DISC)
    ar  = ''.join('<li><span>%s</span></li>' % a for a in AREAS[:8])
    return f'''
<footer class="ftr">
  <div class="ftr__wm" aria-hidden="true"></div>
  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__b">
        <img src="{BIZ['logo']}" alt="{BIZ['name']}" width="120" height="99" loading="lazy">
        <p>Roofing, exterior construction and remodeling for Los Angeles and the San Fernando Valley.</p>
      </div>
      <div class="ftr__c">
        <h2 class="fh">Services</h2>
        <ul>{svc}<li><a href="{url('services')}">All services</a></li></ul>
      </div>
      <div class="ftr__c">
        <h2 class="fh">Company</h2>
        <ul>
          <li><a href="{url('projects')}">Projects</a></li>
          <li><a href="{url('about')}">About</a></li>
          <li><a href="{url('process')}">Process</a></li>
          <li><a href="{url('areas')}">Service areas</a></li>
          <li><a href="{url('contact')}">Start a project</a></li>
        </ul>
      </div>
      <div class="ftr__c">
        <h2 class="fh">Contact</h2>
        <ul>
          <li><a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></li>
          <li><span>{BIZ['street']}<br>{BIZ['city']}, {BIZ['region']} {BIZ['zip']}</span></li>
          <li><a href="{BIZ['maps']}" target="_blank" rel="noopener">Google Maps</a></li>
          <li><a href="{BIZ['yelp']}" target="_blank" rel="noopener">Yelp</a></li>
          <!-- EDIT ME: add verified business hours and social profiles here. -->
        </ul>
      </div>
    </div>
    <div class="ftr__bot">
      <span>© <span id="yr">2026</span> {BIZ['name']}. All rights reserved.</span>
      <nav aria-label="Legal">
        <a href="{url('privacy')}">Privacy</a>
        <a href="{url('terms')}">Terms</a>
        <a href="{url('contact')}">Free consultation</a>
      </nav>
    </div>
  </div>
</footer>
<div class="mbar" id="mbar">
  <a href="tel:{BIZ['tel']}">Call</a>
  <a class="primary" href="{url('contact')}">Start a Project</a>
</div>
<script src="{asset('main.js')}" defer></script>
</body>
</html>
'''

def trust():
    return f'''
<section class="trust" aria-label="At a glance">
  <div class="trust__in">
    <p class="trust__i"><b>Los Angeles &amp; the San Fernando Valley</b></p>
    <p class="trust__i"><b>Free consultation</b></p>
    <p class="trust__i"><b>14 services under one roof</b></p>
    <p class="trust__i"><b>Taking new projects now</b></p>
    <a class="alink trust__more" href="{BIZ['yelp']}" target="_blank" rel="noopener">See our work on Yelp {ARROW}</a>
  </div>
</section>
<!-- EDIT ME — verified credentials belong here once you can evidence them.
     Add as <p class="trust__i"><b>Licensed</b> CSLB #000000</p> etc.
     Candidates: CSLB licence no. · liability & workers' comp insurance ·
     Google rating + review count · years in business · workmanship warranty.
     Nothing above is invented: each line is drawn from A&P's own published material. -->'''

def lead_form(dark=True):
    return f'''
<div class="lead" id="start">
  <div class="lead__side">
    <span class="kicker">Start your project</span>
    <h2 class="d3">Tell us about<br><em class="serif">the house.</em></h2>
    <p>Five short questions. A real answer about what your project takes — not a sales sequence.</p>
    <a class="lead__tel" href="tel:{BIZ['tel']}">{BIZ['phone']}</a>
    <address class="lead__addr">
      {BIZ['name']}<br>{BIZ['street']}, {BIZ['city']}, {BIZ['region']} {BIZ['zip']}<br>
      <a href="{BIZ['maps']}" target="_blank" rel="noopener">Open in Google Maps</a>
    </address>
  </div>

  <div class="lead__form">
    <form id="leadForm" novalidate>
      <div class="pbar" id="pbar" role="progressbar" aria-valuemin="1" aria-valuemax="5" aria-valuenow="1" aria-label="Form progress">
        <i class="on"></i><i></i><i></i><i></i><i></i>
      </div>
      <p class="pmeta"><span id="pstep">Step 1 / 5</span><span id="pname">Project</span></p>

      <fieldset class="step on">
        <legend class="sr">What are you planning?</legend>
        <p class="step__q">What are you planning?</p>
        <p class="step__h">Closest match is fine — we get into detail on the call.</p>
        <div class="opts">
          <label class="opt"><input type="radio" name="project" value="Roof repair or leak" checked><span>Roof repair or leak</span></label>
          <label class="opt"><input type="radio" name="project" value="Roof replacement"><span>Roof replacement</span></label>
          <label class="opt"><input type="radio" name="project" value="Exterior — paint, stucco, gutters"><span>Paint, stucco or gutters</span></label>
          <label class="opt"><input type="radio" name="project" value="Deck, hardscape or outdoor"><span>Deck or outdoor</span></label>
          <label class="opt"><input type="radio" name="project" value="Home remodeling"><span>Home remodeling</span></label>
          <label class="opt"><input type="radio" name="project" value="Not sure yet"><span>Not sure yet</span></label>
        </div>
      </fieldset>

      <fieldset class="step">
        <legend class="sr">Where is the property?</legend>
        <p class="step__q">Where is the property?</p>
        <p class="step__h">Neighborhood and ZIP is enough.</p>
        <div class="fields">
          <div class="f"><label for="lArea">Neighborhood or city</label><input type="text" id="lArea" name="area" autocomplete="address-level2"></div>
          <div class="f"><label for="lZip">ZIP code</label><input type="text" id="lZip" name="zip" inputmode="numeric" autocomplete="postal-code"></div>
        </div>
      </fieldset>

      <fieldset class="step">
        <legend class="sr">When would you like to start?</legend>
        <p class="step__q">When would you like to start?</p>
        <p class="step__h">An honest answer helps us schedule properly.</p>
        <div class="opts">
          <label class="opt"><input type="radio" name="timing" value="Urgent — active leak or damage" checked><span>It's urgent</span></label>
          <label class="opt"><input type="radio" name="timing" value="Within a month"><span>Within a month</span></label>
          <label class="opt"><input type="radio" name="timing" value="1–3 months"><span>1–3 months</span></label>
          <label class="opt"><input type="radio" name="timing" value="Planning / budgeting"><span>Just planning</span></label>
        </div>
      </fieldset>

      <fieldset class="step">
        <legend class="sr">Tell us about the project</legend>
        <p class="step__q">Tell us about the project</p>
        <p class="step__h">Optional — the more we know, the more useful the first visit is.</p>
        <div class="fields">
          <div class="f f--full"><label for="lMsg">What's going on with the house?</label><textarea id="lMsg" name="message" rows="3"></textarea></div>
        </div>
        <label class="drop" for="lPhotos" id="lDrop">
          <b>Add photos</b><span>Roof, damage, the room — anything that helps</span>
          <input type="file" id="lPhotos" accept="image/*" multiple class="sr">
        </label>
        <div class="thumbs" id="lThumbs"></div>
      </fieldset>

      <fieldset class="step">
        <legend class="sr">How should we contact you?</legend>
        <p class="step__q">How should we reach you?</p>
        <p class="step__h">We come back with next steps.</p>
        <div class="fields">
          <div class="f"><label for="lName">Full name</label><input type="text" id="lName" name="name" required autocomplete="name" aria-describedby="lNameE"><span class="f__e" id="lNameE" role="alert"></span></div>
          <div class="f"><label for="lPhone">Phone</label><input type="tel" id="lPhone" name="phone" required autocomplete="tel" aria-describedby="lPhoneE"><span class="f__e" id="lPhoneE" role="alert"></span></div>
          <div class="f f--full"><label for="lEmail">Email (optional)</label><input type="email" id="lEmail" name="email" autocomplete="email"></div>
          <div class="f f--full"><label for="lPref">Preferred contact</label>
            <select id="lPref" name="preferred"><option>Phone call</option><option>Text message</option><option>Email</option></select></div>
        </div>
      </fieldset>

      <div class="lnav">
        <button class="lback" type="button" id="lBack" hidden>← Back</button>
        <button class="btn btn--light" type="button" id="lNext">Continue {ARROW}</button>
        <p class="lalt">or <a href="tel:{BIZ['tel']}">call</a></p>
      </div>
    </form>

    <div class="done" id="leadDone" role="status">
      <div class="done__rule"></div>
      <h3>Thanks. We received your project.</h3>
      <p>We'll review the details and contact you to discuss the next step.</p>
      <div class="done__row">
        <a class="btn btn--light" href="tel:{BIZ['tel']}">Call A&amp;P</a>
        <a class="btn btn--onDark" href="{url('projects')}">View projects</a>
        <button class="btn btn--onDark" type="button" id="lAgain">Send another</button>
      </div>
    </div>
  </div>
</div>'''

# ================================================================ schema
def biz_ld():
    return {"@type":"RoofingContractor","@id":SITE+"/#biz","name":BIZ['name'],
      "url":SITE+"/","telephone":"+1-310-633-5777","image":PU('estate'),
      "logo":BIZ['logo'],"sameAs":[BIZ['yelp']],
      "description":"Roofing, exterior construction and remodeling contractor serving Los Angeles and the San Fernando Valley.",
      "address":{"@type":"PostalAddress","streetAddress":BIZ['street'],"addressLocality":BIZ['city'],
                 "addressRegion":BIZ['region'],"postalCode":BIZ['zip'],"addressCountry":"US"},
      "areaServed":[{"@type":"City","name":"Los Angeles"}]+[{"@type":"Place","name":a} for a in AREAS],
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Services","itemListElement":[
        {"@type":"Offer","itemOffered":{"@type":"Service","name":i}}
        for d in DISC for i in d['lists']][:24]}}

def ld(*objs):
    return '<script type="application/ld+json">%s</script>' % json.dumps(
        {"@context":"https://schema.org","@graph":list(objs)}, ensure_ascii=False)

def crumbs_ld(items):
    return {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":n+1,"name":t,"item":SITE+u}
        for n,(t,u) in enumerate(items)]}

def crumbs(items):
    out=[]
    for i,(t,u) in enumerate(items):
        last = i == len(items)-1
        out.append('<li aria-current="page">%s</li>' % t if last else '<li><a href="%s">%s</a></li>' % (u,t))
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">%s</ol></nav>' % ''.join(out)

def write(path, html):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding='utf-8')

# ================================================================ shared blocks
def phero(kicker_items, h1, sub, key, ctas=True, extra_html=''):
    return f'''
<section class="phero">
  <div class="phero__bg" aria-hidden="true"><img src="{PHOTO[key]}" alt="" fetchpriority="high" decoding="async"></div>
  <div class="wrap phero__in">
    {kicker_items}
    <h1 class="d2">{h1}</h1>
    <p class="phero__sub">{sub}</p>
    {'<div class="phero__cta"><a class="btn btn--light" href="' + url('contact') + '">Start a Project ' + ARROW + '</a><a class="btn btn--onDark" href="tel:' + BIZ['tel'] + '">' + BIZ['phone'] + '</a></div>' if ctas else ''}
    {extra_html}
  </div>
</section>'''

def endcta(title='Get a written scope<br><em class="serif">and a real number.</em>'):
    return f'''
<section class="sec sec--tight"><div class="wrap">
  <div class="endcta rv">
    <div><span class="kicker" style="margin-bottom:16px">Next step</span><h2 class="d3">{title}</h2></div>
    <div class="endcta__r">
      <a class="btn" href="{url('contact')}">Start a Project {ARROW}</a>
      <a class="btn btn--line" href="tel:{BIZ['tel']}">{BIZ['phone']}</a>
    </div>
  </div>
</div></section>'''

def project_block(p, link=True, hl='h3'):
    lay = p['layout']
    tags = [t for t in [p['project_type'], p['location'], p['materials']] if t]
    tag_html = '<ul class="proj__tags">%s</ul>' % ''.join('<li>%s</li>' % t for t in tags) if tags else ''
    href = url('projects/' + p['slug'])
    meta = f'''<div class="proj__meta">
        <span class="proj__no">{p['n']}</span>
        <{hl} class="proj__t">{p['title']}</{hl}>
        <p class="proj__d">{p['blurb']}</p>
        {tag_html}
        {'<a class="alink" href="' + href + '">View project ' + ARROW + '</a>' if link else ''}
      </div>'''
    sizes = '100vw' if lay == 'wide' else '(max-width:860px) 92vw, 55vw'
    figure = fr(p['key'], 'proj__fig', sizes=sizes)
    inner = (figure + meta) if lay != 'splitR' else (meta + figure)
    return f'<article class="proj proj--{lay} rv"><div class="proj__grid">{inner}</div></article>'

# ================================================================ HOME
def page_home():
    projects = ''.join(project_block(p) for p in PROJECTS)
    disc = ''.join(f'''
      <article class="disc__i rv rv-{min(i,3)}">
        {fr(d['key'],'disc__fig',sizes='(max-width:560px) 92vw, (max-width:1000px) 46vw, 23vw')}
        <span class="disc__n">{d['n']} / {d['name']}</span>
        <h3 class="h3">{d['lede']}</h3>
        <ul>{''.join('<li>%s</li>' % x for x in d['items'])}</ul>
        <a class="alink" href="{url('services/' + d['slug'])}">{d['name']} {ARROW}</a>
      </article>''' for i, d in enumerate(DISC))
    why = ''.join(f'''<div class="why__i rv"><span class="why__n">{n}</span>
        <h3 class="h3">{t}</h3><p>{b}</p></div>''' for n, t, b in WHY)
    proc = ''.join(f'''<li class="proc__s rv"><b>{n}</b><div><h3 class="h3">{t}</h3><p>{b}</p></div></li>'''
                   for n, t, b, k in PROCESS)
    proc_imgs = ''.join('<img%s src="%s" alt="" loading="lazy" decoding="async">'
                        % (' class="on"' if i == 0 else '', PHOTO[k])
                        for i, (n, t, b, k) in enumerate(PROCESS))
    areas = ''.join('<li><span>%s</span></li>' % a for a in AREAS)

    ba = ''
    if BEFORE_AFTER:
        ba = f'''
<section class="sec paper"><div class="wrap">
  <div class="shead"><div><span class="kicker">Before &amp; after</span><h2 class="d2">The part you <em class="serif">actually notice.</em></h2></div></div>
  <div class="ba rv" id="ba">
    <img src="{BEFORE_AFTER['after']}" alt="{BEFORE_AFTER['after_alt']}" loading="lazy" decoding="async">
    <div class="ba__b" id="baClip"><img src="{BEFORE_AFTER['before']}" alt="{BEFORE_AFTER['before_alt']}" loading="lazy" decoding="async"><span class="ba__lab ba__lab--b">Before</span></div>
    <span class="ba__lab ba__lab--a">After</span>
    <div class="ba__h" id="baHandle" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 6 4 12l5 6M15 6l5 6-5 6"/></svg></div>
    <p class="ba__hint" aria-hidden="true">Drag to compare</p>
    <input class="ba__r" id="baRange" type="range" min="0" max="100" value="50" step="0.5" aria-label="Reveal before and after">
  </div>
  <dl class="ba__meta rv">
    <div><dt>Project</dt><dd>{BEFORE_AFTER['project']}</dd></div>
    <div><dt>Location</dt><dd>{BEFORE_AFTER['location']}</dd></div>
    <div><dt>Work completed</dt><dd>{BEFORE_AFTER['work']}</dd></div>
  </dl>
</div></section>'''

    return head(
        'A&amp;P Remodeling and Consulting | Roofing &amp; Exterior Contractor, Los Angeles',
        'Roofing, exterior construction and remodeling across Los Angeles and the San Fernando Valley. 14 services under one roof. Free consultation — 310-633-5777.',
        '', 'estate', ld(biz_ld(), {"@type":"WebSite","@id":SITE+"/#site","url":SITE+"/",
             "name":BIZ['name'],"publisher":{"@id":SITE+"/#biz"}})
    ) + header('') + f'''
<main id="main">

<section class="hero">
  <div class="hero__media">
    <img src="{PU('estate')}" alt="{ALT['estate']}" width="1600" height="1200" fetchpriority="high" decoding="async">
  </div>
  <div class="hero__in">
    <span class="kicker rv">Los Angeles / San Fernando Valley</span>
    <h1 class="d1 lines">
      <span class="ln"><span>Built right.</span></span>
      <span class="ln"><span>Designed <em class="serif">to last.</em></span></span>
    </h1>
    <p class="hero__sub rv rv-1">Premium roofing, remodeling and exterior construction across Los Angeles.</p>
    <div class="hero__cta rv rv-2">
      <a class="btn btn--light" href="{url('contact')}">Start Your Project {ARROW}</a>
      <a class="btn btn--onDark" href="{url('projects')}">View Our Work</a>
      <a class="hero__tel" href="tel:{BIZ['tel']}">{BIZ['phone']}</a>
    </div>
  </div>
</section>

{trust()}

<section class="sec"><div class="wrap">
  <div class="stmt">
    <p class="kicker rv">The company</p>
    <div>
      <h2 class="stmt__t rv">We specialise in elevating residential exteriors with <em>refined craftsmanship</em>.</h2>
      <p class="lead rv rv-1" style="margin-top:24px;max-width:52ch">A&amp;P works out of North Hollywood across Los Angeles and the San Fernando Valley. Roofing, exterior and remodeling run through one scope and one schedule.</p>
      <p class="lead rv rv-2" style="margin-top:16px;max-width:52ch">Fourteen services under one roof — so a homeowner is never left holding the coordination.</p>
    </div>
  </div>
</div></section>

<section class="sec paper" id="work"><div class="wrap">
  <div class="shead">
    <div><span class="kicker">Selected projects</span><h2 class="d2">Los Angeles homes, <em class="serif">rebuilt better.</em></h2></div>
    <div class="shead__a"><a class="alink" href="{url('projects')}">All projects {ARROW}</a></div>
  </div>
  {projects}
  <p class="projnote">Photographs are A&amp;P's own work. Locations, dates and scope are being added to each project —
     <a href="tel:{BIZ['tel']}">call {BIZ['phone']}</a> to ask about any of them, or for references near you.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="shead">
    <div><span class="kicker">What we build</span><h2 class="d2">Four disciplines, <em class="serif">one contractor.</em></h2></div>
    <div class="shead__a"><a class="alink" href="{url('services')}">All services {ARROW}</a></div>
  </div>
  <div class="disc">{disc}</div>
</div></section>

{ba}

<section class="sec dark"><div class="wrap">
  <div class="shead">
    <div><span class="kicker">Why A&amp;P</span><h2 class="d2" style="color:#F3F0EA">Most of what goes wrong on a job <em class="serif">isn't the construction.</em></h2></div>
  </div>
  <div class="why">{why}</div>
</div></section>

<section class="sec paper"><div class="wrap">
  <div class="people">
    {fr('tearoff','people__fig',sizes='(max-width:860px) 92vw, 46vw')}
    <div>
      <span class="kicker rv">The people behind A&amp;P</span>
      <h2 class="people__q rv rv-1">Your home deserves <em class="serif">accountability.</em></h2>
      <p class="lead rv rv-2" style="max-width:44ch">When someone hires us, they are trusting us with their home. We take that responsibility seriously.</p>
      <!-- EDIT ME — founder block. Replace the placeholder below with the owner's
           name, role and a real portrait. No name is invented here on purpose. -->
      <div class="people__sig rv rv-2" style="margin-top:26px">
        <b>Add owner name</b><span>Add role · A&amp;P Remodeling and Consulting</span>
      </div>
      <a class="btn rv rv-3" href="{url('contact')}">Talk to A&amp;P {ARROW}</a>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="proc">
    <div class="proc__aside">
      <span class="kicker rv">How it goes</span>
      <h2 class="d2 rv rv-1" style="margin-top:18px;max-width:9ch">Four steps.</h2>
      <figure class="proc__fig rv" aria-hidden="true">{proc_imgs}</figure>
    </div>
    <ol class="proc__steps">{proc}</ol>
  </div>
</div></section>

<section class="sec paper"><div class="wrap">
  <div class="shead">
    <div><span class="kicker">Service areas</span><h2 class="d2">Remodeling Los Angeles, <em class="serif">one home at a time.</em></h2></div>
    <div class="shead__a"><a class="alink" href="{url('areas')}">All areas {ARROW}</a></div>
  </div>
  <ul class="areas rv">{areas}</ul>
</div></section>

<section class="sec dark"><div class="wrap">{lead_form()}</div></section>

</main>''' + footer()

# ================================================================ PROJECTS
def page_projects():
    body = ''.join(project_block(p, hl='h2') for p in PROJECTS)
    return head('Projects | A&amp;P Remodeling and Consulting, Los Angeles',
      "Roofing and exterior projects photographed on site by A&P Remodeling and Consulting across Los Angeles and the San Fernando Valley.",
      'projects','tearoff',
      ld(crumbs_ld([('Home','/'),('Projects','/projects'+EXT)]))
    ) + header('projects') + f'''
<main id="main">
{phero(crumbs([('Home',url('')),('Projects','')]), 'The work, as it actually looked.',
       "Every photograph on this page was taken on an A&amp;P job site. Locations, scope and dates are added as each project is written up.", 'tearoff')}
<section class="sec"><div class="wrap">
  {body}
  <p class="projnote">Want to see a job like yours? <a href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a> and we'll point you at one nearby.</p>
</div></section>
{endcta()}
</main>''' + footer()

def page_project(p):
    facts = []
    for label, v in [('Project type', p['project_type']), ('Location', p['location']),
                     ('Materials', p['materials']), ('Timeline', p['timeline'])]:
        if v: facts.append(f'<div><dt>{label}</dt><dd>{v}</dd></div>')
    facts_html = ('<dl class="case__facts rv">%s</dl>' % ''.join(facts)) if facts else ''
    gal = ''.join(fr(k, sizes='(max-width:640px) 92vw, 46vw') for k in p['gallery'])
    gal_html = f'<div class="case__gal rv" style="margin-top:clamp(30px,4vw,52px)">{gal}</div>' if gal else ''
    story = ''
    for label, v in [('The original condition', p['condition']), ('Scope', p['scope']), ('Solution', p['solution'])]:
        if v: story += f'<h2>{label}</h2><p>{v}</p>'
    if not story:
        story = ('<p>This project is being written up. The photograph is A&amp;P\'s own; the full scope, '
                 'materials and timeline are added once confirmed with the homeowner.</p>')
    idx = PROJECTS.index(p)
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    return head(p['title'] + ' | A&amp;P Remodeling and Consulting',
      p['blurb'], 'projects/' + p['slug'], p['key'],
      ld(crumbs_ld([('Home','/'),('Projects','/projects'+EXT),(p['title'],'/projects/'+p['slug']+EXT)]))
    ) + header('projects') + f'''
<main id="main">
<section class="sec" style="padding-top:clamp(140px,15vw,200px)"><div class="wrap">
  {crumbs([('Home',url('')),('Projects',url('projects')),(p['title'],'')]).replace('class="crumbs"','class="crumbs" style="color:var(--ink-40)"')}
  <span class="kicker" style="margin-bottom:16px">{p['n']} — {p['project_type']}</span>
  <h1 class="d2" style="max-width:16ch;margin-bottom:26px">{p['title']}</h1>
  {fr(p['key'],'case__hero',eager=True,zoom=False)}
  {facts_html}
  <div class="prose rv">{story}</div>
  {gal_html}
  <p class="projnote">Photograph: {p['caption']}</p>
</div></section>
<section class="sec sec--tight paper"><div class="wrap">
  <div class="endcta">
    <div><span class="kicker" style="margin-bottom:16px">Next project</span>
      <h2 class="d3" style="max-width:16ch">{nxt['title']}</h2></div>
    <div class="endcta__r"><a class="btn" href="{url('projects/' + nxt['slug'])}">View project {ARROW}</a>
      <a class="btn btn--line" href="{url('projects')}">All projects</a></div>
  </div>
</div></section>
</main>''' + footer()

# ================================================================ SERVICES
def page_services():
    cards = ''.join(f'''
      <article class="disc__i rv">
        {fr(d['key'],'disc__fig',sizes='(max-width:560px) 92vw, (max-width:1000px) 46vw, 23vw')}
        <span class="disc__n">{d['n']} / {d['name']}</span>
        <h2 class="h3">{d['lede']}</h2>
        <ul>{''.join('<li>%s</li>' % x for x in d['lists'][:6])}</ul>
        <a class="alink" href="{url('services/' + d['slug'])}">{d['name']} {ARROW}</a>
      </article>''' for d in DISC)
    return head('Services | Roofing, Exterior, Remodeling &amp; Outdoor — A&amp;P Los Angeles',
      'Roofing, exterior construction, remodeling and outdoor living across Los Angeles and the San Fernando Valley. 14 services under one roof.',
      'services','tile', ld(crumbs_ld([('Home','/'),('Services','/services'+EXT)]))
    ) + header('services') + f'''
<main id="main">
{phero(crumbs([('Home',url('')),('Services','')]),'Fourteen services, one contractor.',
   'Roofing, exterior, remodeling and outdoor living — grouped so you can see in seconds whether A&amp;P covers your project.','tile')}
<section class="sec"><div class="wrap"><div class="disc">{cards}</div></div></section>
{endcta()}
</main>''' + footer()

def page_service(d):
    body = ''.join('<h2>%s</h2>%s' % (h, ''.join('<p>%s</p>' % x for x in ps)) for h, ps in d['body'])
    lists = ''.join('<li>%s</li>' % i for i in d['lists'])
    others = ''.join(f'''<article class="disc__i rv">
        <span class="disc__n">{o['n']} / {o['name']}</span>
        <h3 class="h3" style="margin-bottom:16px">{o['lede']}</h3>
        <a class="alink" href="{url('services/' + o['slug'])}">{o['name']} {ARROW}</a></article>'''
        for o in DISC if o['slug'] != d['slug'])
    svc_ld = {"@type":"Service","name":d['name'],"serviceType":d['name'],
        "provider":{"@id":SITE+"/#biz"},"url":canon('services/'+d['slug']),
        "areaServed":[{"@type":"City","name":"Los Angeles"}]+[{"@type":"Place","name":a} for a in AREAS],
        "hasOfferCatalog":{"@type":"OfferCatalog","name":d['name'],
          "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":i}} for i in d['lists']]}}
    return head(d['title'], d['desc'], 'services/'+d['slug'], d['key'],
      ld(biz_ld(), svc_ld, crumbs_ld([('Home','/'),('Services','/services'+EXT),(d['name'],'/services/'+d['slug']+EXT)]))
    ) + header('services') + f'''
<main id="main">
{phero(crumbs([('Home',url('')),('Services',url('services')),(d['name'],'')]), d['h1'], d['sub'], d['key'])}
<section class="sec"><div class="wrap">
  <div class="split">
    <div class="prose rv">{body}</div>
    {fr(d['key'],'split__fig',sizes='(max-width:900px) 92vw, 36vw')}
  </div>
</div></section>
<section class="sec paper"><div class="wrap">
  <span class="kicker rv">{d['list_title']}</span>
  <h2 class="d3 rv" style="margin:18px 0 34px;max-width:18ch">Everything under <em class="serif">{d['name'].lower()}</em>.</h2>
  <ul class="areas rv">{lists}</ul>
</div></section>
{endcta()}
<section class="sec sec--tight"><div class="wrap">
  <span class="kicker rv">Also from A&amp;P</span>
  <h2 class="d3 rv" style="margin:18px 0 34px">The rest of the house.</h2>
  <div class="disc">{others}</div>
</div></section>
</main>''' + footer()

# ================================================================ ABOUT / PROCESS / AREAS / CONTACT / LEGAL
def page_about():
    why = ''.join(f'<div class="why__i rv"><span class="why__n">{n}</span><h3 class="h3">{t}</h3><p>{b}</p></div>'
                  for n, t, b in WHY)
    return head('About | A&amp;P Remodeling and Consulting, North Hollywood',
      "A&P Remodeling and Consulting is a Los Angeles contractor working out of North Hollywood — roofing, exterior construction and remodeling across the San Fernando Valley.",
      'about','estate', ld(biz_ld(), crumbs_ld([('Home','/'),('About','/about'+EXT)]))
    ) + header('about') + f'''
<main id="main">
{phero(crumbs([('Home',url('')),('About','')]),'Your home deserves accountability.',
   "When someone hires us, they are trusting us with their home. We take that responsibility seriously.",'estate')}

<section class="sec"><div class="wrap">
  <div class="people">
    {fr('tearoff','people__fig',sizes='(max-width:860px) 92vw, 46vw')}
    <div>
      <span class="kicker rv">The people behind A&amp;P</span>
      <h2 class="people__q rv rv-1">We specialise in elevating residential exteriors with <em class="serif">refined craftsmanship.</em></h2>
      <p class="lead rv rv-2" style="max-width:46ch">From roofing to solar, every project should leave the house better than a coat of paint could. That is the whole business.</p>
      <!-- EDIT ME — replace with the owner's real name, role and portrait. -->
      <div class="people__sig rv rv-2" style="margin-top:28px"><b>Add owner name</b><span>Add role · {BIZ['name']}</span></div>
      <a class="btn rv rv-3" href="{url('contact')}">Talk to A&amp;P {ARROW}</a>
    </div>
  </div>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="shead"><div><span class="kicker">Why A&amp;P</span>
    <h2 class="d2" style="color:#F3F0EA">Most of what goes wrong on a job <em class="serif">isn't the construction.</em></h2></div></div>
  <div class="why">{why}</div>
</div></section>

<section class="sec paper"><div class="wrap">
  <div class="stmt">
    <p class="kicker rv">Where we are</p>
    <div>
      <h2 class="stmt__t rv">North Hollywood yard. <em>Valley-wide</em> crew.</h2>
      <p class="lead rv rv-1" style="margin-top:22px;max-width:50ch">{BIZ['street']}, {BIZ['city']}, {BIZ['region']} {BIZ['zip']}.
        Most of the Valley is a short drive rather than a dispatch across the county.</p>
      <div class="rv rv-2" style="margin-top:28px;display:flex;gap:14px;flex-wrap:wrap">
        <a class="btn btn--line" href="{BIZ['maps']}" target="_blank" rel="noopener">Open in Google Maps {ARROW}</a>
        <a class="btn btn--line" href="{BIZ['yelp']}" target="_blank" rel="noopener">See our work on Yelp {ARROW}</a>
      </div>
    </div>
  </div>
</div></section>
{endcta()}
</main>''' + footer()

def page_process():
    proc = ''.join(f'<li class="proc__s rv"><b>{n}</b><div><h3 class="h3">{t}</h3><p>{b}</p></div></li>'
                   for n, t, b, k in PROCESS)
    imgs = ''.join('<img%s src="%s" alt="" loading="lazy" decoding="async">'
                   % (' class="on"' if i == 0 else '', PHOTO[k]) for i, (n,t,b,k) in enumerate(PROCESS))
    return head('Our Process | A&amp;P Remodeling and Consulting, Los Angeles',
      'Four steps from first call to finished job: tell us about the project, on-site consultation, written scope and timeline, then build.',
      'process','aerial', ld(crumbs_ld([('Home','/'),('Process','/process'+EXT)]))
    ) + header('process') + f'''
<main id="main">
{phero(crumbs([('Home',url('')),('Process','')]),'Four steps. No surprises.',
   'The point of a process is that you always know what happens next.','aerial')}
<section class="sec"><div class="wrap">
  <div class="proc">
    <div class="proc__aside">
      <span class="kicker rv">How it goes</span>
      <h2 class="d2 rv rv-1" style="margin-top:18px;max-width:9ch">From call to <em class="serif">clean site.</em></h2>
      <figure class="proc__fig rv" aria-hidden="true">{imgs}</figure>
    </div>
    <ol class="proc__steps">{proc}</ol>
  </div>
</div></section>
{endcta()}
</main>''' + footer()

def page_areas():
    items = ''.join('<li><span>%s</span></li>' % a for a in AREAS)
    return head('Service Areas | Los Angeles &amp; the San Fernando Valley — A&amp;P',
      'A&P Remodeling and Consulting serves Los Angeles and the San Fernando Valley from North Hollywood — Studio City, Sherman Oaks, Burbank, Encino, Woodland Hills and surrounding areas.',
      'areas','tile', ld(biz_ld(), crumbs_ld([('Home','/'),('Service areas','/areas'+EXT)]))
    ) + header('areas') + f'''
<main id="main">
{phero(crumbs([('Home',url('')),('Service areas','')]),'Remodeling Los Angeles, one home at a time.',
   'Based on Morella Ave in North Hollywood, working across the San Fernando Valley and greater Los Angeles. Not sure whether you are in range? Call and ask.','tile')}
<section class="sec"><div class="wrap">
  <ul class="areas rv">{items}</ul>
  <p class="projnote">Every area above is served from the North Hollywood yard. Dedicated pages for individual
     neighborhoods will be added as A&amp;P publishes local project photography — not as duplicated text.</p>
</div></section>
{endcta()}
</main>''' + footer()

def page_contact():
    faq = ''.join(f'''<div class="faq__i"><h3><button class="faq__q" type="button" aria-expanded="false">{q}<i aria-hidden="true"></i></button></h3>
      <div class="faq__a"><p>{a}</p></div></div>''' for q, a in FAQ)
    faq_ld = {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q.replace('&amp;','&'),
         "acceptedAnswer":{"@type":"Answer","text":a.replace('&amp;','&')}} for q, a in FAQ]}
    return head('Start a Project | A&amp;P Remodeling and Consulting — 310-633-5777',
      'Start your project with A&P Remodeling and Consulting. Free consultation across Los Angeles and the San Fernando Valley. Call 310-633-5777.',
      'contact','finished', ld(biz_ld(), faq_ld, crumbs_ld([('Home','/'),('Contact','/contact'+EXT)]))
    ) + header('contact') + f'''
<main id="main">
{phero(crumbs([('Home',url('')),('Start a project','')]),'Start your project.',
   'Five short questions, or one phone call. Free consultation across Los Angeles and the San Fernando Valley.','finished',ctas=False)}
<section class="sec dark" style="padding-top:0"><div class="wrap">
  {lead_form()}
</div></section>
<section class="sec paper"><div class="wrap">
  <div class="shead"><div><span class="kicker">Questions</span><h2 class="d2">Before <em class="serif">you call.</em></h2></div>
    <div class="shead__a"><a class="alink" href="tel:{BIZ['tel']}">{BIZ['phone']} {ARROW}</a></div></div>
  <div class="faq">{faq}</div>
</div></section>
</main>''' + footer()

def legal(slug, title, desc, blocks):
    body = ''.join('<h2>%s</h2>%s' % (h, ''.join('<p>%s</p>' % p for p in ps)) for h, ps in blocks)
    return head(title, desc, slug, 'tile', '<meta name="robots" content="noindex,follow">') + header('') + f'''
<main id="main">
<section class="sec" style="padding-top:clamp(140px,15vw,200px)"><div class="wrap">
  {crumbs([('Home',url('')),(title.split('|')[0].strip(),'')]).replace('class="crumbs"','class="crumbs" style="color:var(--ink-40)"')}
  <h1 class="d2" style="max-width:14ch;margin-bottom:30px">{title.split('|')[0].strip()}</h1>
  <div class="prose">{body}</div>
</div></section>
</main>''' + footer()

def page_404():
    return head('Page not found | A&amp;P Remodeling and Consulting',
      'That page does not exist. Return to the A&P Remodeling and Consulting home page or call 310-633-5777.',
      '404','tile','<meta name="robots" content="noindex,nofollow">') + header('') + f'''
<main id="main">
<section class="sec err" style="padding-top:clamp(140px,15vw,200px)"><div class="wrap">
  <span class="kicker">404</span>
  <h1 class="d2" style="margin:20px 0 20px;max-width:14ch">That page isn't here.</h1>
  <p class="lead" style="max-width:46ch;margin-bottom:34px">The link may be old or mistyped. The work is all a click away.</p>
  <div style="display:flex;flex-wrap:wrap;gap:14px">
    <a class="btn" href="{url('')}">Back to home {ARROW}</a>
    <a class="btn btn--line" href="{url('projects')}">View projects</a>
    <a class="btn btn--line" href="tel:{BIZ['tel']}">{BIZ['phone']}</a>
  </div>
</div></section>
</main>''' + footer()

# ================================================================ RUN
PRIVACY = [
 ('Who we are', [f"{BIZ['name']}, {BIZ['street']}, {BIZ['city']}, {BIZ['region']} {BIZ['zip']}. Phone {BIZ['phone']}. This policy covers this website."]),
 ('What this site collects', ["The project form sends what you enter to A&amp;P so we can respond. Photos you attach stay on your device until you send them. This site sets no advertising or tracking cookies."]),
 ('Information you send us', ["When you call, text, email or submit the form we receive what you chose to include — typically your name, phone number, property location and a description of the work. We use it to respond, prepare an estimate and carry out work you engage us for."]),
 ('Sharing', ["We do not sell your information. We share it only with subcontractors, suppliers or inspectors where that is necessary to quote or deliver your project, and where the law requires it."]),
 ('Third parties on this site', ["Fonts load from Google Fonts and photographs from A&amp;P's media host. Those providers receive your IP address as part of serving the files."]),
 ('Your choices', [f"Ask us to correct or delete what you have sent by calling {BIZ['phone']}. California residents have additional rights under the CCPA — contact us and we will honour them."]),
 ('Changes', ["If this policy changes, the updated version is posted here."]),
 ('EDIT ME', ["This is a plain-language starting point, not legal advice. Have it reviewed, and update it if you add analytics, advertising pixels, a CRM or a form backend."]),
]
TERMS = [
 ('Using this site', ["This website describes services offered by " + BIZ['name'] + ". Nothing on it is a binding quotation. Pricing, scope and schedule are set out in a written estimate for your specific property."]),
 ('Photography', ["Project photographs on this site are A&amp;P's own work. Every project varies; images are illustrative of workmanship, not a guarantee of a particular result on your home."]),
 ('Estimates', ["Consultations and written estimates are provided free of charge with no obligation. An estimate is valid for the period stated on it."]),
 ('Contact', [f"Questions about these terms: {BIZ['phone']}, {BIZ['street']}, {BIZ['city']}, {BIZ['region']} {BIZ['zip']}."]),
 ('EDIT ME', ["Placeholder terms. Have a professional review before relying on them, especially warranty, liability and dispute-resolution language."]),
]

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copy('/root/site/static/styles.css', OUT / 'styles.css')
    shutil.copy('/root/site/static/main.js',   OUT / 'main.js')
    (OUT / '.nojekyll').write_text('')

    write('index.html',    page_home())
    write('projects.html', page_projects())
    for p in PROJECTS: write('projects/%s.html' % p['slug'], page_project(p))
    write('services.html', page_services())
    for d in DISC: write('services/%s.html' % d['slug'], page_service(d))
    write('about.html',   page_about())
    write('process.html', page_process())
    write('areas.html',   page_areas())
    write('contact.html', page_contact())
    write('privacy.html', legal('privacy','Privacy Policy | A&amp;P Remodeling and Consulting',
        'How A&P Remodeling and Consulting handles information submitted through this website.', PRIVACY))
    write('terms.html',   legal('terms','Terms | A&amp;P Remodeling and Consulting',
        'Terms of use for the A&P Remodeling and Consulting website.', TERMS))
    write('404.html',     page_404())

    urls = ['', 'projects', 'services', 'about', 'process', 'areas', 'contact'] \
         + ['projects/' + p['slug'] for p in PROJECTS] \
         + ['services/' + d['slug'] for d in DISC]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = '1.0' if u == '' else ('0.9' if u.startswith('services') or u == 'projects' else '0.8')
        sm.append('  <url><loc>%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>' % (canon(u), pr))
    sm.append('</urlset>')
    write('sitemap.xml', '\n'.join(sm))
    write('robots.txt', 'User-agent: *\nAllow: /\nDisallow: /privacy\nDisallow: /terms\n\nSitemap: %s/sitemap.xml\n' % SITE)

    n = sum(1 for _ in OUT.rglob('*.html'))
    print('built %d html pages -> %s (BASE=%r)' % (n, OUT, BASE))

if __name__ == '__main__':
    main()
