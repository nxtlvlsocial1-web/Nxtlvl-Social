"""Builds nxtlvlsocial.ai into ../website: shared header, footer, schema and styles for every page.

Run:  python3 website-src/build.py
Edit the copy in PAGES below, then rebuild. Output: website/*.html, site.css, site.js, sitemap.xml, llms.txt.
"""
import html
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', 'website'))
SITE = 'https://nxtlvlsocial.ai'
EMAIL = 'connect@nxtlvlsocial.ai'
UPDATED = '2026-11-17'
INSTAGRAM = [('Instagram · @ai.nxtlvl', 'https://www.instagram.com/ai.nxtlvl/'), ('Instagram · @nxtlvlledits', 'https://www.instagram.com/nxtlvlledits/')]
STAR = json.load(open(os.path.join(HERE, 'star.json')))
e = html.escape

# ---------------------------------------------------------------- icons (24px line icons, stroke = currentColor)
P = {
    'spark': '<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="2.5"/>',
    'trend': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'flow': '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/><path d="M10 6.5h4a3 3 0 0 1 3 3V14"/>',
    'camera': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    'code': '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
    'film': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9.5v5l4.5-2.5z"/>',
    'palette': '<path d="M12 3a9 9 0 1 0 0 18c1.3 0 2-.8 2-1.8 0-1.4-1.2-1.7-1.2-3 0-1 .8-1.7 1.9-1.7H17a4 4 0 0 0 4-4C21 6.6 17 3 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
    'chart': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'search': '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5M16 4.6a3.5 3.5 0 0 1 0 6.8M18.5 14.8c1.6.8 2.6 2.5 3 5.2"/>',
    'key': '<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 7l2 2M14 9l2 2"/>',
    'refresh': '<path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/>',
    'layers': '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'shield': '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    'mega': '<path d="M3 10v4h4l6 4V6L7 10z"/><path d="M17 9a4 4 0 0 1 0 6"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6l8.5 7 8.5-7"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}
def icon(name, cls=''):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{(' class="' + cls + '"') if cls else ''}>{P[name]}</svg>'

def star_svg(uid='s'):
    g = lambda gid, col, x1, y1, x2, y2: (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
        f'<stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".55" stop-color="{col}" stop-opacity=".9"/><stop offset="1" stop-color="{col}"/></linearGradient>')
    return (f'<svg viewBox="20.6 31.6 147.8 147.8" aria-hidden="true"><defs>{g(uid + "a", "#FFFFFF", 28.3, 171.7, 121.6, 78.4)}{g(uid + "b", "#A95CFF", 69.3, 164.7, 121.6, 112.3)}'
            f'{g(uid + "c", "#B98AFF", 43.8, 122.2, 82.0, 84.0)}</defs><path d="{STAR["t0"]}" fill="url(#{uid}a)"/><path d="{STAR["t1"]}" fill="url(#{uid}b)"/>'
            f'<path d="{STAR["t2"]}" fill="url(#{uid}c)"/><path d="{STAR["s"]}" fill="#FFFFFF"/></svg>')

# ---------------------------------------------------------------- shared blocks
NAV = [('/ai-marketing', 'Marketing'), ('/ai-automation', 'Automation'), ('/creative-studio', 'Creative'), ('/website-development', 'Websites'), ('/about', 'About')]
SERVICES = [  # url, name, short, icon, need
    ('/ai-marketing', 'AI Marketing', 'Social media management, campaigns, ads and SEO, planned with AI and run by strategists.', 'trend', 'marketing'),
    ('/ai-automation', 'AI Automation', 'WhatsApp and Instagram replies, lead capture and follow-ups that work around the clock.', 'flow', 'automation'),
    ('/creative-studio', 'Creative Studio', 'Shoots, reel and video editing, and graphic design that look like your brand.', 'camera', 'creative'),
    ('/website-development', 'Websites', 'Fast, SEO-ready websites and landing pages built to turn visitors into enquiries.', 'code', 'website'),
]

def header(active):
    links = ''.join(f'<a href="{u}"{' aria-current="page"' if u == active else ''}>{t}</a>' for u, t in NAV)
    mlinks = ''.join(f'<a href="{u}">{t}</a>' for u, t in NAV + [('/contact', 'Contact')])
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Nxtlvl Social home">{star_svg("lg")}<b>nxtlvl<span>social</span></b></a>
    <nav class="menu" aria-label="Main">{links}</nav>
    <span class="sp"></span>
    <a class="btn btn-ghost hide-m" href="/contact"{' aria-current="page"' if active == '/contact' else ''}>Contact</a>
    <a class="btn btn-primary hide-m" href="/contact">Book a call</a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mob">{icon("menu")}</button>
  </div>
  <div class="mob" id="mob" hidden><div class="wrap"><nav aria-label="Mobile">{mlinks}<a class="btn btn-primary" href="/contact">Book a free call</a></nav></div></div>
</header>'''

def footer():
    svc = ''.join(f'<li><a href="{u}">{n}</a></li>' for u, n, *_ in SERVICES)
    social = ''.join(f'<li><a href="{u}" rel="me noopener" target="_blank">{e(t.split(" · ")[1])}</a></li>' for t, u in INSTAGRAM)
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div><a class="logo" href="/" aria-label="Nxtlvl Social home">{star_svg("ft")}<b>nxtlvl<span>social</span></b></a>
        <p>An AI-driven growth company for brands in India. Marketing, automation and creative production on one monthly subscription.</p></div>
      <div><h2>Services</h2><ul>{svc}</ul></div>
      <div><h2>Company</h2><ul><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li><li><a href="/#faq">FAQ</a></li></ul></div>
      <div><h2>Connect</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>{social}</ul></div>
    </div>
    <div class="legal"><span>© 2026 Nxtlvl Social. AI-driven marketing, automation and creative services, India.</span><span>Made with AI, finished by people.</span></div>
  </div>
</footer>'''

def faq_block(items, title='Questions, answered', sub=''):
    qa = ''.join(f'<details><summary>{e(q)}</summary><div class="a">{"".join(f"<p>{x}</p>" for x in a)}</div></details>' for q, a in items)
    return f'''<section id="faq" class="rule"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">FAQ</span><h2>{title}</h2>{f'<p class="lead">{sub}</p>' if sub else ''}</div>
  <div class="faq reveal">{qa}</div></div></section>'''

def faq_schema(items):
    strip = lambda s: html.unescape(__import__('re').sub(r'<[^>]+>', '', s))
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(strip(x) for x in a)}} for q, a in items]}

NEEDS = [('unsure', 'Not sure yet, help me choose'), ('marketing', 'AI Marketing'), ('automation', 'AI Automation'), ('creative', 'Creative Studio: shoots, edits, design'), ('website', 'Website development'), ('platform', 'Early access: growth platform')]
def contact_form(heading_id='book-h'):
    opts = ''.join(f'<option value="{v}">{e(l)}</option>' for v, l in NEEDS)
    return f'''<form class="book" novalidate aria-labelledby="{heading_id}">
  <div class="f"><label for="name">Your name</label><input id="name" name="name" autocomplete="name" required placeholder="Full name"></div>
  <div class="f"><label for="business">Business</label><input id="business" name="business" autocomplete="organization" placeholder="Brand or company"></div>
  <div class="f full"><label for="email">Work email</label><input id="email" name="email" type="email" autocomplete="email" required placeholder="you@company.com"></div>
  <div class="f full"><label for="need">What do you need?</label><select id="need" name="need">{opts}</select></div>
  <div class="f full"><label for="message">Tell us about your goals</label><textarea id="message" name="message" placeholder="What you sell, who you sell to, and what growth looks like for you."></textarea></div>
  <div class="hp" aria-hidden="true"><label for="website">Website</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
  <div class="form-msg" role="status" hidden></div>
  <div class="f full"><button class="btn btn-primary" type="submit">Book my free call</button></div>
  <p class="form-note">We reply within one business day. Prefer email? Write to <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</form>'''

def cta(title='Ready to grow with AI on your side?', sub='Book a free 20-minute strategy call. We look at your brand, your channels and your goals, then send a plan you can keep, whether or not you work with us.'):
    return f'''<section><div class="wrap"><div class="cta"><div class="in reveal">
  <h2>{title}</h2><p class="lead">{sub}</p>
  <div class="btns"><a class="btn btn-primary" href="/contact">Book a free call {icon("arrow")}</a><a class="btn btn-ghost" href="mailto:{EMAIL}">Email us</a></div>
</div></div></div></section>'''

ORG = {
    '@type': 'Organization', '@id': f'{SITE}/#org', 'name': 'Nxtlvl Social', 'alternateName': ['Next Level Social', 'Nxtlvl'],
    'url': f'{SITE}/', 'logo': f'{SITE}/icon-512.png', 'image': f'{SITE}/og-image.png', 'email': EMAIL,
    'description': 'Nxtlvl Social is an AI-driven growth company in India providing marketing, business automation and creative production (shoots, video editing, graphic design) and website development on monthly subscriptions.',
    'slogan': 'AI-driven growth for modern brands', 'areaServed': {'@type': 'Country', 'name': 'India'},
    'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'email': EMAIL, 'areaServed': 'IN', 'availableLanguage': ['English', 'Hindi']},
    'sameAs': [u for _, u in INSTAGRAM],
    'knowsAbout': ['AI marketing', 'Social media management', 'Performance marketing', 'Search engine optimisation', 'Answer engine optimisation',
                   'Marketing automation', 'WhatsApp automation', 'Instagram DM automation', 'Video editing', 'Product photography', 'Graphic design', 'Website development'],
    'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'AI-driven growth services', 'itemListElement': [
        {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'url': SITE + u, 'description': s}} for u, n, s, *_ in SERVICES]},
}
WEBSITE = {'@type': 'WebSite', '@id': f'{SITE}/#website', 'url': f'{SITE}/', 'name': 'Nxtlvl Social', 'publisher': {'@id': f'{SITE}/#org'}, 'inLanguage': 'en-IN'}

def page(path, title, desc, body, active='', crumbs=None, extra_schema=(), noindex=False, page_type='WebPage'):
    url = SITE + (path if path != '/index' else '/')
    graph = [ORG, WEBSITE, {'@type': page_type, '@id': url + '#page', 'url': url, 'name': title, 'description': desc, 'isPartOf': {'@id': f'{SITE}/#website'},
             'about': {'@id': f'{SITE}/#org'}, 'inLanguage': 'en-IN', 'dateModified': UPDATED}]
    if crumbs:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (u, n) in enumerate(crumbs)]})
    graph += list(extra_schema)
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'}
<meta name="theme-color" content="#05030C">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nxtlvl Social">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/instrument-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/archivo-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/site.css?v={UPDATED}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/site.js?v={UPDATED}" defer></script>
</body>
</html>
'''

def crumbs_html(crumbs):
    out = []
    for i, (u, n) in enumerate(crumbs):
        out.append(f'<a href="{u}">{n}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{n}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(out) + '</nav>'

# ---------------------------------------------------------------- home
HOME_FAQ = [
    ('What is Nxtlvl Social?', ['Nxtlvl Social is an AI-driven growth company in India. We run marketing, business automation and creative production for brands on a monthly subscription. AI systems handle research, first drafts and repetitive work; our team handles strategy, creative direction and quality, and reviews everything before it goes live.']),
    ('How is an AI-driven growth company different from a traditional marketing agency?', ['A traditional agency staffs every task by hand, which makes it slow and expensive. We use AI for research, ideas, variations, scheduling and automated replies, so a small senior team delivers more in less time and spends its hours on decisions that move the business. You get the output of a full marketing team without hiring one.']),
    ('What services are included in a subscription?', ['Plans are built from four parts: <a href="/ai-marketing">AI marketing</a> (social media management, campaigns, ads, SEO and AEO), <a href="/ai-automation">AI automation</a> (WhatsApp and Instagram DM flows, lead capture, CRM and follow-ups), the <a href="/creative-studio">creative studio</a> (shoots, reel and video editing, graphic design) and <a href="/website-development">website development</a>. You choose what you need, and we scope it with you on a free call.']),
    ('How does the subscription work, and what does it cost?', ['Each plan has a clear monthly scope and one point of contact. There is no long contract: you can change the scope, pause or stop at the end of any month. Pricing depends on the scope, so we share a written quote after a free strategy call, before any work starts.']),
    ('Do you work with businesses across India?', ['Yes. We work remotely with brands across India, from metros to smaller cities, and with international clients. Photo and video shoots are arranged on location when a project needs them.']),
    ('Will our content look AI-generated?', ['No. AI speeds up research and drafting, but strategists, designers and editors finish every piece in your brand style. Nothing is published until you approve it.']),
    ('Who owns the content and accounts?', ['You do. Final files, source files, ad accounts and any systems we set up belong to your business.']),
    ('How do we get started?', ['Book a free call through the <a href="/contact">contact page</a>. We review your brand and goals, send a scope and plan, and once you approve it we begin onboarding: brand kit, account access and a first-month plan.']),
]

def home():
    tasks = [('film', 'Festive offer reel', 'Creative Studio · cut, captions, cover', 'In review', 'review'),
             ('mega', 'Meta ads · lead generation', 'AI Marketing · 3 creatives in rotation', 'Live', 'live'),
             ('chat', 'Instagram DM replies', 'AI Automation · FAQs, pricing, bookings', 'Running 24/7', 'live'),
             ('palette', 'Carousel · 5 tips for buyers', 'Creative Studio · brand template', 'Scheduled Fri', ''),
             ('code', 'Landing page · new launch', 'Websites · copy and design', 'Drafting', '')]
    rows = ''.join(f'<div class="task"><span class="ic">{icon(i)}</span><div><b>{t}</b><small>{s}</small></div><span class="pill {c}">{p}</span></div>' for i, t, s, p, c in tasks)
    engines = ''.join(f'''<a class="card engine reveal" href="{u}"><span class="ic">{icon(ic)}</span><h3>{n}</h3><p>{s}</p>
      <span class="more">Explore {n.split()[-1] if n != "Websites" else "websites"} {icon("arrow")}</span></a>''' for u, n, s, ic, _ in SERVICES)
    caps = [('Social media management', 'Instagram, Facebook, LinkedIn, YouTube'), ('Performance marketing', 'Meta and Google Ads, set up and optimised'),
            ('SEO and AEO', 'Rank on Google and get cited by AI assistants'), ('Content strategy', 'Monthly calendars built on research'),
            ('Reels and short video', 'Hooks, captions and motion graphics'), ('Product and brand shoots', 'Photo and video, on location'),
            ('Graphic design', 'Posts, carousels, ads, print'), ('Brand identity', 'Logo, palette, templates, brand kit'),
            ('WhatsApp automation', 'Catalogue, FAQs, bookings, broadcasts'), ('Instagram DM automation', 'Instant replies to comments and DMs'),
            ('Lead capture and CRM', 'Every enquiry logged and followed up'), ('Websites and landing pages', 'Fast, mobile-first, SEO-ready')]
    caps_html = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in caps)
    body = f'''
<section class="hero">
  <div class="wrap hero-in">
    <span class="eyebrow">AI-driven growth company · India</span>
    <h1>AI-driven growth for <span class="grad">modern brands</span></h1>
    <p class="lead">Nxtlvl Social runs your marketing, automation and creative production on one monthly subscription. AI systems do the heavy lifting. Our team brings the strategy, the taste and the final check.</p>
    <div class="btns"><a class="btn btn-primary" href="/contact">Book a free strategy call {icon("arrow")}</a><a class="btn btn-ghost" href="#services">Explore services</a></div>
    <p class="hero-note">Monthly plans · No long contracts · You own everything we make</p>
    <div class="panel" role="img" aria-label="Illustration of a Nxtlvl Social client workspace: reels, ad campaigns, DM automation, carousels and a landing page in progress, with an AI assistant suggesting hooks.">
      <div class="panel-bar"><span class="dots"><i></i><i></i><i></i></span><b>Growth workspace</b><span class="hide-s">· Your brand</span><span class="sp"></span><span class="hide-s">This week</span></div>
      <div class="panel-body"><div class="tasks">{rows}</div>
        <div class="side"><h4>Assistant</h4>
          <div class="bubble"><span class="who">{star_svg("bb")} Nxtlvl AI</span><span>Three hook ideas drafted for Friday's reel, based on last month's top posts:</span>
            <ul><li>"The one mistake buyers make…"</li><li>"We tested 3 offers. Here's the winner."</li><li>"60 seconds inside our kitchen"</li></ul>
            <div class="acts"><span>Send to editor</span><span>Regenerate</span></div></div>
          <div class="bubble"><span class="who">{icon("users")} Strategist</span><span>Approved the second hook. Shooting Thursday.</span></div>
        </div></div>
    </div>
  </div>
</section>

<div class="strip"><div class="wrap"><p>Built for growing businesses</p>
  <ul><li>D2C and e-commerce</li><li>Restaurants and cafés</li><li>Clinics and wellness</li><li>Real estate</li><li>Education</li><li>Startups</li><li>Creators and personal brands</li></ul></div></div>

<section id="services"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Services</span><h2>Four growth engines. One subscription.</h2>
    <p class="lead">Pick the engines your brand needs this quarter. They share one plan, one team and one report, so your marketing, systems and creative work together instead of in silos.</p></div>
  <div class="grid g2">{engines}</div>
</div></section>

<section class="rule"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">How it works</span><h2>From first call to compounding growth</h2></div>
  <div class="steps reveal">
    <div class="step"><span class="n">01</span><h3>Discover</h3><p>A free strategy call and an audit of your brand, channels, competitors and goals.</p></div>
    <div class="step"><span class="n">02</span><h3>Build</h3><p>AI drafts the research, calendar, creatives and automations. Our team refines every piece.</p></div>
    <div class="step"><span class="n">03</span><h3>Launch</h3><p>You approve, we publish, run the campaigns and switch on the automations.</p></div>
    <div class="step"><span class="n">04</span><h3>Improve</h3><p>A monthly report on what worked, and a sharper plan for next month.</p></div>
  </div>
</div></section>

<section class="rule"><div class="wrap split">
  <div class="sec-head reveal"><span class="eyebrow">Our approach</span><h2>AI for speed. People for judgement.</h2>
    <p class="lead">We use AI where it is genuinely better than people, and people where taste and accountability matter. That is how a small team delivers like a big one.</p></div>
  <div class="rows reveal">
    <div><span class="ic">{icon("search")}</span><div><h3>Research and ideas</h3><p>AI scans trends, competitors and your past performance to find hooks, topics and angles worth making.</p></div></div>
    <div><span class="ic">{icon("layers")}</span><div><h3>Faster production</h3><p>First drafts, edits, captions and variations in hours, so there is time to test more and polish what wins.</p></div></div>
    <div><span class="ic">{icon("flow")}</span><div><h3>Systems that never sleep</h3><p>Automations answer customers, capture leads and follow up while your team focuses on the work only people can do.</p></div></div>
    <div><span class="ic">{icon("shield")}</span><div><h3>Human-reviewed, always</h3><p>A strategist or editor checks every output for accuracy, brand fit and quality. Nothing goes live without your approval.</p></div></div>
  </div>
</div></section>

<section class="rule"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Capabilities</span><h2>Everything a growth team does</h2>
    <p class="lead">One partner for the full journey, from being discovered to being chosen.</p></div>
  <div class="caps reveal">{caps_html}</div>
</div></section>

<section class="rule"><div class="wrap">
  <div class="callout reveal">
    <div><span class="eyebrow">Subscription</span><h2 style="margin-top:14px">Plans that grow with you</h2>
      <p class="lead">Every plan is built around your goals and agreed in writing before work starts. Scale up for a launch, scale down in a quiet month.</p>
      <div class="btns" style="margin-top:24px"><a class="btn btn-primary" href="/contact">Get a custom plan {icon("arrow")}</a></div></div>
    <ul>
      <li>{icon("calendar")}<span><b style="color:var(--text);font-weight:600">Monthly plans.</b> A clear scope and deliverables each month.</span></li>
      <li>{icon("users")}<span><b style="color:var(--text);font-weight:600">One team, one contact.</b> Strategy, creative and automation under one roof.</span></li>
      <li>{icon("refresh")}<span><b style="color:var(--text);font-weight:600">No lock-in.</b> Change scope, pause or stop at the end of any month.</span></li>
      <li>{icon("key")}<span><b style="color:var(--text);font-weight:600">You own it.</b> Files, accounts and systems belong to your business.</span></li>
    </ul>
  </div>
</div></section>

<section class="rule"><div class="wrap">
  <div class="sec-head center reveal"><span class="soon">In development</span><h2>The Nxtlvl growth platform</h2>
    <p class="lead">We are building an AI workspace that turns a short brief into content ideas, scripts and ready-to-post reels, with our team one message away. Subscribers get early access.</p>
    <div class="btns" style="justify-content:center"><a class="btn btn-ghost" href="/contact?need=platform">Ask about early access</a></div></div>
</div></section>

{faq_block(HOME_FAQ, 'Questions, answered', 'Straight answers about how an AI-driven growth company works.')}
{cta()}
'''
    return page('/index', 'AI-Driven Marketing, Automation & Creative | Nxtlvl Social',
                'Nxtlvl Social is an AI-driven growth company in India. Marketing, WhatsApp and DM automation, shoots, edits, design and websites on one monthly plan.',
                body, '/', extra_schema=[faq_schema(HOME_FAQ)])

# ---------------------------------------------------------------- service pages
def service_page(path, name, title, desc, h1, intro, facts, included, how, who, faqs, need, extra_html=''):
    crumbs = [('/', 'Home'), (path, name)]
    inc = ''.join(f'<div class="card reveal"><span class="ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in included)
    steps = ''.join(f'<div class="step"><span class="n">0{i + 1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(how))
    facts_html = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in facts)
    who_html = ''.join(f'<li>{w}</li>' for w in who)
    others = ''.join(f'<a class="card reveal" href="{u}"><span class="ic">{icon(ic)}</span><h3>{n}</h3><p>{s}</p><span class="more">Learn more {icon("arrow")}</span></a>' for u, n, s, ic, _ in SERVICES if u != path)
    svc = {'@type': 'Service', '@id': SITE + path + '#service', 'name': name, 'serviceType': name, 'url': SITE + path, 'description': desc,
           'provider': {'@id': f'{SITE}/#org'}, 'areaServed': {'@type': 'Country', 'name': 'India'},
           'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': name, 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': t}} for _, t, _ in included]}}
    body = f'''
<section class="page-hero"><div class="wrap"><div class="in">
  {crumbs_html(crumbs)}
  <span class="eyebrow">{name}</span>
  <h1>{h1}</h1>
  <p class="lead">{intro}</p>
  <div class="btns"><a class="btn btn-primary" href="/contact?need={need}">Book a free call {icon("arrow")}</a><a class="btn btn-ghost" href="#included">What's included</a></div>
</div></div></section>

<section class="rule" style="padding-top:56px;padding-bottom:56px"><div class="wrap"><div class="facts reveal"><h2>At a glance</h2><dl>{facts_html}</dl></div></div></section>

<section id="included" class="rule"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">What's included</span><h2>What we do for you</h2></div>
  <div class="grid g3">{inc}</div>
</div></section>
{extra_html}
<section class="rule"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Process</span><h2>How it works</h2></div>
  <div class="steps reveal">{steps}</div>
</div></section>

<section class="rule"><div class="wrap split">
  <div class="sec-head reveal"><span class="eyebrow">Who it's for</span><h2>Built for brands that want to grow</h2></div>
  <div class="prose reveal"><ul>{who_html}</ul><p>Not sure this fits? <a href="/contact?need={need}">Tell us about your business</a> and we will say honestly whether we can help.</p></div>
</div></section>

{faq_block(faqs, f'{name}: common questions')}

<section class="rule"><div class="wrap">
  <div class="sec-head reveal"><span class="eyebrow">Pairs well with</span><h2>The rest of the growth stack</h2></div>
  <div class="grid g3">{others}</div>
</div></section>
{cta()}
'''
    return page(path, title, desc, body, path, crumbs, [svc, faq_schema(faqs)])

MARKETING = dict(
    path='/ai-marketing', name='AI Marketing', need='marketing',
    title='AI Marketing & Social Media Management in India | Nxtlvl',
    desc='AI-driven social media management, marketing campaigns, Meta and Google Ads, SEO and AEO for brands in India. Planned with AI, run by strategists.',
    h1='AI marketing and social media management for growing brands',
    intro='We plan, create and run your marketing with AI-powered research and a senior team behind it: social media, campaigns, paid ads and search, all on one monthly plan, measured against the numbers that matter to your business.',
    facts=[('What it is', 'Done-for-you marketing: social media management, campaigns, paid ads, SEO and AEO'), ('Channels', 'Instagram, Facebook, LinkedIn, YouTube, Google Search and AI assistants'),
           ('How AI is used', 'Trend and competitor research, content ideas, copy variations, audience insights, reporting'), ('Who does the work', 'A strategist owns your account and reviews everything before it goes live'),
           ('Reporting', 'A monthly report with results and next month\'s plan'), ('Commitment', 'Monthly subscription, no long contract')],
    included=[('users', 'Social media management', 'Monthly content calendars, posting, captions, hashtags and community replies across Instagram, Facebook, LinkedIn and YouTube.'),
              ('calendar', 'Content strategy', 'Pillars, formats and a posting rhythm built on research into your audience, competitors and what already works for you.'),
              ('mega', 'Performance marketing', 'Meta and Google Ads campaigns: audiences, creatives, landing pages, tracking and weekly optimisation.'),
              ('trend', 'Marketing campaigns', 'Launches, festive and seasonal campaigns, offers and collaborations, planned end to end across channels.'),
              ('search', 'SEO and AEO', 'Search engine and answer engine optimisation, so you show up on Google and get recommended by ChatGPT, Gemini and Perplexity.'),
              ('chart', 'Analytics and reporting', 'Clear monthly reports on reach, engagement, leads and sales, with what we will change next month and why.')],
    how=[('Audit', 'We review your accounts, competitors, audience and past results to find the quickest wins.'), ('Strategy', 'A 90-day plan with goals, channels, content pillars and campaign ideas.'),
         ('Execute', 'AI drafts, our team refines, you approve. We publish, run ads and manage the community.'), ('Report', 'Monthly results against goals, and a sharper plan for the next month.')],
    who=['D2C and e-commerce brands that need consistent content and profitable ads', 'Restaurants, cafés, salons and clinics that want more local customers', 'Real estate and education businesses that run on qualified leads',
         'Startups that need a marketing team before they can hire one', 'Founders and creators building a personal brand'],
    faqs=[('What is AI marketing?', ['AI marketing uses artificial intelligence for the parts of marketing that benefit from speed and data: researching trends and competitors, generating content ideas and copy variations, analysing audiences and reporting. At Nxtlvl Social a human strategist directs that work and approves every output.']),
          ('Which platforms do you manage?', ['Instagram, Facebook, LinkedIn and YouTube for social media; Meta and Google for paid ads; and Google Search plus AI assistants such as ChatGPT, Gemini and Perplexity for SEO and AEO.']),
          ('Is ad spend included in the plan?', ['No. Ad spend is paid by you directly to Meta or Google, so you keep full control and ownership of the ad accounts. Planning, creatives and campaign management are part of your plan.']),
          ('What is AEO, and why does it matter?', ['Answer engine optimisation (AEO) makes your business easy for AI assistants and Google\'s AI Overviews to understand and cite. More buyers now ask an assistant before they search, so being the answer it gives is becoming as important as ranking on page one.']),
          ('How do you measure results?', ['We agree on the numbers that matter to your business on the first call, such as leads, bookings, sales or reach, and report on them every month along with what we will change next.'])])

AUTOMATION = dict(
    path='/ai-automation', name='AI Automation', need='automation',
    title='AI Automation: WhatsApp, Instagram DM & Lead Flows | Nxtlvl',
    desc='AI automation for Indian businesses: WhatsApp and Instagram DM auto-replies, lead capture, CRM and follow-ups that run 24/7. Set up and managed for you.',
    h1='AI automation that answers, qualifies and follows up for you',
    intro='Your customers message at midnight, ask the same ten questions and expect replies in minutes. We build automations on WhatsApp, Instagram and your website that answer instantly, capture every lead and hand the right conversations to your team.',
    facts=[('What it is', 'Done-for-you business automation for customer messages, leads and follow-ups'), ('Channels', 'WhatsApp Business, Instagram and Facebook DMs and comments, website forms, email'),
           ('How AI is used', 'Understanding questions, drafting replies, qualifying and tagging leads, summarising conversations'), ('Human handover', 'Complex or high-value conversations go straight to your team'),
           ('Tools', 'Official Meta and WhatsApp Business tools, plus Google Sheets, CRMs and no-code platforms'), ('Commitment', 'Monthly subscription with setup, monitoring and improvements')],
    included=[('chat', 'Instagram and Facebook DM automation', 'Instant replies to DMs and comments: prices, availability, links and offers, with keyword triggers for campaigns.'),
              ('flow', 'WhatsApp automation', 'WhatsApp Business flows for FAQs, catalogues, bookings, order updates and opt-in broadcasts.'),
              ('users', 'Lead capture and qualification', 'Every enquiry captured from ads, DMs and your website, qualified with a few questions and tagged by intent.'),
              ('layers', 'CRM and lead tracking', 'Leads flow into a simple CRM or Google Sheet, so nothing gets lost and you can see the pipeline at a glance.'),
              ('refresh', 'Follow-up sequences', 'Timed follow-ups on WhatsApp and email for quotes, abandoned enquiries and repeat customers.'),
              ('calendar', 'Booking and reminder flows', 'Appointment booking, confirmations and reminders that cut no-shows for clinics, salons and service businesses.')],
    how=[('Map', 'We list the questions you answer every day and the steps from enquiry to sale.'), ('Build', 'We write the flows, connect your channels and test every path with real examples.'),
         ('Launch', 'Automations go live with a human handover for anything they should not answer.'), ('Improve', 'We read the conversations monthly, add answers and tune what converts.')],
    who=['Businesses that get many repeat questions on WhatsApp and Instagram', 'Clinics, salons, gyms and studios that run on appointments', 'Real estate, education and service businesses that depend on fast lead response',
         'E-commerce brands handling order and delivery questions', 'Any team that loses leads because nobody replied in time'],
    faqs=[('What is AI automation for business?', ['AI automation uses software and AI models to handle repetitive work such as answering common customer questions, capturing and qualifying leads, sending follow-ups and updating records, so your team only steps in where a person adds value.']),
          ('Is WhatsApp and Instagram automation allowed?', ['Yes, when it uses the official tools. We build on Meta\'s approved WhatsApp Business and Instagram messaging features and follow their policies, including opt-in for broadcasts.']),
          ('Will customers know they are talking to an automation?', ['We write replies in your brand voice and make it clear when a message is automated. Customers can reach a person at any point, and complex or sensitive conversations are handed over automatically.']),
          ('Do I need the WhatsApp Business API?', ['Not always. Simple setups work with the WhatsApp Business app; larger volumes, multiple team members and advanced flows need the WhatsApp Business Platform. We recommend the right option on the free call.']),
          ('Which CRM do you use?', ['We work with what you already have. If you have nothing yet, we set up a simple CRM or a Google Sheet that your team can use from day one.'])])

CREATIVE = dict(
    path='/creative-studio', name='Creative Studio', need='creative',
    title='Shoots, Reel Editing & Graphic Design Studio | Nxtlvl Social',
    desc='Product and brand shoots, reel and video editing, and graphic design for brands in India. AI-assisted production, finished by editors and designers.',
    h1='Creative studio for shoots, reel editing and graphic design',
    intro='Great growth needs great creative. Our studio plans, shoots, edits and designs the content your brand runs on, using AI to move faster and editors and designers to make every frame look like you.',
    facts=[('What it is', 'Creative production: photo and video shoots, reel and video editing, graphic design, brand identity'), ('Formats', 'Reels, YouTube Shorts and long-form, product photos, carousels, ads, posters and print'),
           ('How AI is used', 'Concepts and scripts, rough cuts, captions, background clean-up and design variations'), ('Who does the work', 'Editors and designers finish every piece by hand in your brand style'),
           ('Footage', 'We shoot on location, or edit the raw footage you send'), ('Commitment', 'Monthly subscription or a defined monthly batch')],
    included=[('camera', 'Product and brand shoots', 'Photo and video shoots for products, food, spaces and teams, planned with a shot list and styled for your feed and ads.'),
              ('film', 'Reels and short-form video', 'Instagram Reels and YouTube Shorts with strong hooks, subtitles, motion graphics, music and covers.'),
              ('layers', 'Video editing', 'YouTube videos, ads, testimonials and event films edited from your footage or ours.'),
              ('palette', 'Graphic design', 'Social posts, carousels, story sets, ad creatives, menus, posters and brochures.'),
              ('spark', 'Brand identity', 'Logos, colour palettes, typography and a brand kit with templates your team can reuse.'),
              ('refresh', 'AI-assisted visuals', 'Concept art, backgrounds and variations created with AI and finished by designers, never posted raw.')],
    how=[('Brief', 'We learn your brand, audience and goals, and build a monthly content plan.'), ('Create', 'Scripts, shoots, edits and designs, with AI speeding up the first drafts.'),
         ('Review', 'You get drafts with time to request changes before anything is final.'), ('Deliver', 'Final files in the right sizes for every platform, ready to post or run as ads.')],
    who=['Brands that post often and need a steady flow of quality creative', 'Restaurants, fashion, beauty and D2C brands that sell visually', 'Businesses with raw footage and no time to edit it',
         'Creators who need a reliable editor', 'Teams launching a product, rebrand or campaign'],
    faqs=[('Do you shoot on location?', ['Yes. We plan and run photo and video shoots on location for products, food, spaces and people. If you prefer, we edit the footage you shoot on your phone.']),
          ('How fast is the turnaround?', ['It depends on the format and the monthly plan. Turnaround times are agreed in your scope, and AI-assisted drafting means first versions arrive quickly so there is time for revisions.']),
          ('Do you use AI-generated images and video?', ['We use AI for concepts, rough cuts, clean-up and variations. Designers and editors finish every piece, and we never post raw AI output or use AI to misrepresent real products.']),
          ('Can you follow our existing brand guidelines?', ['Yes. We work inside your brand guidelines, or create a brand kit if you do not have one yet.']),
          ('Where can I see your editing work?', ['Our editing account on Instagram, <a href="https://www.instagram.com/nxtlvlledits/" rel="noopener" target="_blank">@nxtlvlledits</a>, shows recent edits. We also share relevant samples on the free call.'])])

WEBSITES = dict(
    path='/website-development', name='Website Development', need='website',
    title='Website Development & Landing Pages, SEO-Ready | Nxtlvl Social',
    desc='Fast, mobile-first websites and landing pages for brands in India, built for Google and AI search, with enquiry and booking forms. Hosting and updates included.',
    h1='Websites and landing pages built to rank and convert',
    intro='Your website is the one channel you fully own. We design and build fast, mobile-first websites and campaign landing pages that load quickly, rank on Google, get understood by AI search and turn visitors into enquiries.',
    facts=[('What it is', 'Design and development of business websites and landing pages'), ('Built for', 'Speed, mobile, Google search, AI answers and lead generation'),
           ('How AI is used', 'Research, copy drafts, image variations and testing ideas, all reviewed by our team'), ('Included', 'Enquiry or booking forms, analytics, schema markup and on-page SEO'),
           ('After launch', 'Updates, improvements and monitoring on a monthly plan'), ('Ownership', 'You own the domain, the content and the code')],
    included=[('globe', 'Business websites', 'Clear, fast websites that explain what you do, show your work and make it easy to contact you.'),
              ('trend', 'Landing pages', 'Focused pages for ads and campaigns, built to convert and easy to test.'),
              ('search', 'SEO and AEO setup', 'Page structure, schema markup, speed and content set up for Google and AI assistants from day one.'),
              ('chat', 'Forms and integrations', 'Enquiry, booking and WhatsApp buttons connected to your inbox, CRM or automations.'),
              ('chart', 'Analytics', 'Visitor and conversion tracking, so you know which pages and campaigns bring business.'),
              ('shield', 'Care and updates', 'Hosting setup, security headers, backups and content updates after launch.')],
    how=[('Plan', 'Goals, pages, content and the actions you want visitors to take.'), ('Design', 'A design in your brand that works on every screen size.'),
         ('Build', 'Fast, accessible code with SEO and analytics in place, tested on real phones.'), ('Grow', 'Launch, then monthly improvements based on what visitors actually do.')],
    who=['Businesses without a website, or with one that looks dated or loads slowly', 'Brands running ads that need a landing page that converts', 'Service businesses that want enquiries and bookings online',
         'Startups launching a product', 'Anyone who wants to be found on Google and in AI answers'],
    faqs=[('How long does a website take?', ['A landing page usually takes days and a multi-page website a few weeks, depending on content and features. We share a timeline in your scope before we start.']),
          ('Is SEO included?', ['Yes. Every site we build includes on-page SEO, schema markup, a sitemap, fast loading and mobile optimisation. Ongoing SEO and content growth are part of our <a href="/ai-marketing">AI marketing</a> plans.']),
          ('Do I own the website?', ['Yes. The domain, content and code belong to you. We can host and maintain it, or hand it over to your team.']),
          ('Can you connect the website to WhatsApp and my CRM?', ['Yes. Forms, WhatsApp buttons and booking tools can feed straight into your inbox, CRM or the automations we build in <a href="/ai-automation">AI automation</a>.']),
          ('Do you redesign existing websites?', ['Yes. We can redesign and rebuild an existing site, keeping the pages that already rank and redirecting old addresses so you keep your search traffic.'])])

# ---------------------------------------------------------------- about and contact
def about():
    crumbs = [('/', 'Home'), ('/about', 'About')]
    body = f'''
<section class="page-hero"><div class="wrap"><div class="in">
  {crumbs_html(crumbs)}<span class="eyebrow">About Nxtlvl Social</span>
  <h1>A growth company built around AI</h1>
  <p class="lead">Nxtlvl Social (Next Level Social) is an AI-driven growth company in India. We give businesses the marketing, automation and creative capacity of a full team, delivered on a simple monthly subscription.</p>
</div></div></section>
<section class="rule"><div class="wrap split">
  <div class="sec-head reveal"><span class="eyebrow">What we believe</span><h2>Growth should not need a big team</h2></div>
  <div class="prose reveal">
    <p>Most growing businesses face the same choice: hire an expensive agency, build an in-house team they cannot yet afford, or try to do everything themselves. We started Nxtlvl Social to offer a better option.</p>
    <p>We work like a technology company. AI systems handle research, first drafts, repetitive tasks and round-the-clock customer replies. A small, senior team sets the strategy, directs the creative and checks every result. The outcome is a growth partner that moves fast, costs less than a traditional agency and still feels personal.</p>
    <h2>What we do</h2>
    <p>We provide company solutions in three areas that work best together:</p>
    <ul><li><strong>Marketing:</strong> <a href="/ai-marketing">social media management, campaigns, paid ads, SEO and AEO</a>, for growth on social and beyond it.</li>
      <li><strong>Automation:</strong> <a href="/ai-automation">WhatsApp and Instagram automation, lead capture, CRM and follow-ups</a>.</li>
      <li><strong>Creativity:</strong> <a href="/creative-studio">shoots, reel and video editing, graphic design and brand identity</a>, plus <a href="/website-development">websites and landing pages</a>.</li></ul>
    <h2>How we work</h2>
    <ul><li><strong>AI for speed, people for judgement.</strong> Every output is reviewed by a person, and nothing goes live without your approval.</li>
      <li><strong>Subscriptions, not one-off projects.</strong> Growth compounds when the same team learns your business month after month.</li>
      <li><strong>Clear numbers.</strong> We agree on the metrics that matter and report on them every month.</li>
      <li><strong>You own everything.</strong> Files, accounts and systems belong to your business.</li></ul>
    <h2>What is next</h2>
    <p>We are building the Nxtlvl growth platform: an AI workspace that turns a brief into ideas, scripts and ready-to-post reels, with our team one message away. Today we deliver that work for clients by hand with AI tools; subscribers will be first to use the platform.</p>
    <p>Want to work with us? <a href="/contact">Book a free strategy call</a> or write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</div></section>
{cta()}
'''
    return page('/about', 'About Nxtlvl Social: An AI-Driven Growth Company in India',
                'Nxtlvl Social is an AI-driven growth company providing marketing, automation and creative solutions for businesses in India on monthly subscriptions.',
                body, '/about', crumbs, page_type='AboutPage')

CONTACT_FAQ = [('What happens on the free call?', ['We spend about 20 minutes on your business, goals and current channels, answer your questions and suggest where AI, automation and creative work can help most. Afterwards we send a written scope and quote.']),
               ('Is the call really free?', ['Yes, with no obligation. If we are not the right fit, we will say so and point you in a better direction.']),
               ('How quickly do you reply?', ['We reply to every request by email within one business day.'])]

def contact():
    crumbs = [('/', 'Home'), ('/contact', 'Contact')]
    social = ''.join(f'<dd><a class="link" href="{u}" rel="noopener" target="_blank">{e(t.split(" · ")[1])}</a></dd>' for t, u in INSTAGRAM)
    body = f'''
<section class="page-hero"><div class="wrap"><div class="in">
  {crumbs_html(crumbs)}<span class="eyebrow">Contact</span>
  <h1>Book a free growth call</h1>
  <p class="lead">Tell us about your brand and what you want to grow. We will reply within one business day to set up a 20-minute call and send a plan with a clear scope.</p>
</div></div></section>
<section class="rule" style="padding-top:56px"><div class="wrap contact">
  <div class="info reveal">
    <h2 id="book-h" style="font-size:clamp(24px,2.6vw,32px)">Let's talk growth</h2>
    <dl><div><dt>Email</dt><dd><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      <div><dt>Instagram</dt>{social}</div>
      <div><dt>Where we work</dt><dd>Remote-first, serving brands across India and abroad. Shoots on location.</dd></div>
      <div><dt>Response time</dt><dd>Within one business day</dd></div></dl>
  </div>
  <div class="reveal">{contact_form()}</div>
</div></section>
{faq_block(CONTACT_FAQ, 'Before you book')}
'''
    return page('/contact', 'Contact Nxtlvl Social: Book a Free Growth Call',
                'Book a free 20-minute strategy call with Nxtlvl Social for AI marketing, automation, creative production or a new website. We reply within one business day.',
                body, '/contact', crumbs, [faq_schema(CONTACT_FAQ)], page_type='ContactPage')

def not_found():
    body = f'''<section class="hero"><div class="wrap hero-in"><span class="eyebrow">404</span><h1>This page took a different route</h1>
<p class="lead">The page you are looking for has moved or no longer exists. Try one of these instead.</p>
<div class="btns"><a class="btn btn-primary" href="/">Go to the home page</a><a class="btn btn-ghost" href="/contact">Contact us</a></div></div></section>'''
    return page('/404', 'Page not found | Nxtlvl Social', 'This page could not be found.', body, noindex=True)

# ---------------------------------------------------------------- write
def main():
    pages = {'index.html': home(), 'about.html': about(), 'contact.html': contact(), '404.html': not_found()}
    for d in (MARKETING, AUTOMATION, CREATIVE, WEBSITES):
        pages[d['path'].strip('/') + '.html'] = service_page(**d)
    for name, content in pages.items():
        with open(os.path.join(OUT, name), 'w') as f:
            f.write(content)
    for asset in ('site.css', 'site.js'):
        shutil.copy(os.path.join(HERE, asset), os.path.join(OUT, asset))
    urls = ['/', '/ai-marketing', '/ai-automation', '/creative-studio', '/website-development', '/about', '/contact']
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write(LLMS)
    print('wrote', ', '.join(sorted(pages)))

LLMS = f"""# Nxtlvl Social

> Nxtlvl Social (Next Level Social) is an AI-driven growth company in India. It provides marketing, business automation, creative production (shoots, video editing, graphic design) and website development to businesses on monthly subscriptions. AI systems handle research, drafts and repetitive work; a human team handles strategy, creative direction and quality, and reviews everything before it goes live.

## Services

- [AI Marketing]({SITE}/ai-marketing): social media management (Instagram, Facebook, LinkedIn, YouTube), content strategy, marketing campaigns, Meta and Google Ads, SEO and AEO (answer engine optimisation), analytics and monthly reporting. Ad spend is paid by the client directly to the platform.
- [AI Automation]({SITE}/ai-automation): Instagram and Facebook DM and comment automation, WhatsApp Business automation, lead capture and qualification, CRM and lead tracking, follow-up sequences, booking and reminder flows, with human handover. Built on official Meta and WhatsApp tools.
- [Creative Studio]({SITE}/creative-studio): product and brand photo and video shoots on location, reels and short-form video, video editing, graphic design, brand identity, AI-assisted visuals finished by designers.
- [Website Development]({SITE}/website-development): business websites and landing pages, SEO and AEO setup with schema markup, forms and integrations, analytics, hosting and updates.

## Key facts

- Model: monthly subscription with a written scope; no long contract; change scope, pause or stop at the end of any month.
- Pricing: custom, quoted in writing after a free 20-minute strategy call.
- Ownership: clients own all final files, source files, accounts and systems.
- Approach: AI for speed, people for judgement; nothing is published without client approval.
- Who it serves: D2C and e-commerce, restaurants and cafés, clinics and wellness, real estate, education, startups, creators and personal brands.
- Where: remote-first across India and internationally; shoots on location.
- In development: the Nxtlvl growth platform, an AI workspace that turns a brief into ideas, scripts and reels; subscribers get early access.
- Contact: {EMAIL}. Instagram: @ai.nxtlvl (AI and growth), @nxtlvlledits (editing work).

## Pages

- [Home]({SITE}/)
- [About]({SITE}/about)
- [Contact]({SITE}/contact)
"""

if __name__ == '__main__':
    main()
