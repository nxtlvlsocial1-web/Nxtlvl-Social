"""Builds nxtlvlsocial.ai into ../website: shared header, footer, schema and styles for every page.

Run:  python3 website-src/build.py
Edit the copy in PAGES below, then rebuild. Output: website/*.html, site.css, site.js, sitemap.xml, llms.txt.
"""
import html
import json
import os
import shutil
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', 'website'))
SITE = 'https://nxtlvlsocial.ai'
EMAIL = 'connect@nxtlvlsocial.ai'
UPDATED = '2026-11-20'
INSTAGRAM = [('Instagram · @ai.nxtlvl', 'https://www.instagram.com/ai.nxtlvl/'), ('Instagram · @nxtlvlledits', 'https://www.instagram.com/nxtlvlledits/')]
STAR = json.load(open(os.path.join(HERE, 'star.json')))
e = html.escape

# ---------------------------------------------------------------- icons (24px line icons, stroke = currentColor)
P = {
    'bot': '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4M9.5 13.5h.01M14.5 13.5h.01M9.5 17h5"/>',
    'pen': '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/>',
    'bolt': '<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>',
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
BRAND = json.load(open(os.path.join(HERE, 'brandicons.json')))   # Simple Icons (CC0) paths and official colours
DARK_OK = {'notion': 'FFFFFF', 'razorpay': '3395FF'}               # brand marks too dark for a dark page

def brand(slug, mono=False, cls='bi'):
    b = BRAND[slug]; col = 'currentColor' if mono else '#' + DARK_OK.get(slug, b['hex'])
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="{col}" aria-hidden="true"><path d="{b["d"]}"/></svg>'

def icon(name, cls=''):
    if name.startswith('b:'):
        return brand(name[2:])
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{(' class="' + cls + '"') if cls else ''}>{P[name]}</svg>'

def star_svg(uid='s', dark=False):
    main = '#0B0816' if dark else '#FFFFFF'
    g = lambda gid, col, x1, y1, x2, y2: (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
        f'<stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".55" stop-color="{col}" stop-opacity=".9"/><stop offset="1" stop-color="{col}"/></linearGradient>')
    return (f'<svg viewBox="20.6 31.6 147.8 147.8" aria-hidden="true"><defs>{g(uid + "a", main, 28.3, 171.7, 121.6, 78.4)}{g(uid + "b", "#A95CFF", 69.3, 164.7, 121.6, 112.3)}'
            f'{g(uid + "c", "#7D18FC" if dark else "#B98AFF", 43.8, 122.2, 82.0, 84.0)}</defs><path d="{STAR["t0"]}" fill="url(#{uid}a)"/><path d="{STAR["t1"]}" fill="url(#{uid}b)"/>'
            f'<path d="{STAR["t2"]}" fill="url(#{uid}c)"/><path d="{STAR["s"]}" fill="{main}"/></svg>')


WORD = json.load(open(os.path.join(HERE, 'wordmark.json')))['paths']   # "nxtlvl social" from brands/nxtlvl/logo-white.svg
def wordmark_svg(label=False):
    lab = ' role="img" aria-label="Nxtlvl Social"' if label else ' aria-hidden="true"'
    return f'<svg class="lg-word" viewBox="118 24 296 54"{lab}><path d="{WORD[0][0]}" fill="#FFFFFF"/><path d="{WORD[1][0]}" fill="#D8BBFF"/></svg>'

def logo_html(uid='lg'):
    """Nxtlvl Social logo: the shooting star on its violet gradient tile, then the wordmark."""
    return f'<span class="lg-tile">{star_svg(uid)}</span>{wordmark_svg()}'

# ---------------------------------------------------------------- shared blocks
NAV = [('/ai-marketing', 'Marketing'), ('/ai-automation', 'Automation'), ('/creative-studio', 'Creative'), ('/website-development', 'Websites'), ('/guides', 'Guides'), ('/about', 'About')]
SERVICES = [  # url, name, short, icon, need
    ('/ai-marketing', 'AI Marketing', 'Social media management, campaigns, ads and SEO, planned with AI and run by strategists.', 'trend', 'marketing'),
    ('/ai-automation', 'AI Automation', 'WhatsApp and Instagram replies, lead capture and follow-ups that work around the clock.', 'flow', 'automation'),
    ('/creative-studio', 'Creative Studio', 'Shoots, reel and video editing, and graphic design that look like your brand.', 'camera', 'creative'),
    ('/website-development', 'Websites', 'Fast, SEO-ready websites and landing pages built to turn visitors into enquiries.', 'code', 'website'),
]

def header(active):
    links = ''.join(f'<a href="{u}"' + (' aria-current="page"' if u == active else '') + f'>{t}</a>' for u, t in NAV)
    mlinks = ''.join(f'<a href="{u}">{t}</a>' for u, t in NAV + [('/contact', 'Contact')])
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="bar frame" style="max-width:none">
  <div class="in">
    <a class="logo" href="/" aria-label="Nxtlvl Social home">{logo_html("lg")}</a>
    <nav class="menu" aria-label="Main">{links}</nav>
    <span class="sp"></span>
    <a class="btn btn-light hide-m" href="/contact">Contact</a>
    <a class="btn btn-primary hide-m" href="/contact">Book a call</a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mob">{icon("menu")}</button>
  </div>
  <div class="mob" id="mob" hidden><nav aria-label="Mobile">{mlinks}<a class="btn btn-primary" href="/contact">Book a free call</a></nav></div>
</header>'''

def footer():
    svc = ''.join(f'<li><a href="{u}">{n}</a></li>' for u, n, *_ in SERVICES)
    social = ''.join(f'<li><a href="{u}" rel="me noopener" target="_blank">{e(t.split(" · ")[1])}</a></li>' for t, u in INSTAGRAM)
    return f'''<footer class="frame">
  <div class="fcols">
    <div class="brand-f"><a class="logo" href="/" aria-label="Nxtlvl Social home">{logo_html("fl")}</a><p>An AI-driven growth company in India. Marketing, automation and creative production on one monthly subscription, made with AI and finished by people.</p></div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Company</h2><ul><li><a href="/about">About</a></li><li><a href="/guides">Guides</a></li><li><a href="/contact">Contact</a></li><li><a href="/#faq">Questions</a></li></ul></div>
    <div><h2>Follow</h2><ul>{social}</ul></div>
    <div><h2>Write to us</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
  </div>
  <div class="bigmark" aria-hidden="true"><span class="word">{wordmark_svg()}</span></div>
  <div class="legal"><span>© 2026 Nxtlvl Social · AI-driven marketing, automation and creative services, India</span><span>Made with AI, finished by people.</span></div>
</footer>'''

def faq_block(items, title='Questions, answered'):
    bands = ''.join(f'<div class="band" data-rise><h3>{e(q)}</h3><div class="a">{"".join(f"<p>{x}</p>" for x in a)}</div></div>' for q, a in items)
    return f'''<section class="faq frame" id="faq" aria-labelledby="faq-h" data-sec><div class="wrapq">
  <div class="h" data-rise><h2 id="faq-h">{title}</h2><p class="soft">Straight answers about how an AI-driven growth company works. Anything else, just ask.</p><div class="btns"><a class="btn btn-light" href="/contact">Ask us anything</a></div></div>
  <div class="list">{bands}</div></div></section>'''

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

def close_row(title='Ready to meet your AI growth team?', sub='Book a free 20-minute strategy call. We look at your brand, channels and goals, then send a plan you can keep, whether or not you work with us.'):
    return f'''<section class="sec frame" data-sec aria-labelledby="close-h"><div class="close" data-rise>
  <h2 id="close-h">{title}</h2><p>{sub}</p>
  <form action="/contact" method="get" aria-label="Start with your email"><label class="sr" for="close-email">Work email</label><input id="close-email" name="email" type="email" placeholder="you@company.com" autocomplete="email"><input type="hidden" name="need" value="unsure"><button class="btn btn-primary" type="submit">Book a free call {icon("arrow")}</button></form>
</div></section>'''

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

def page(path, title, desc, body, active='', crumbs=None, extra_schema=(), noindex=False, page_type='WebPage', og_image='/og-image.png'):
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
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/satoshi-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/unbounded-variable.woff2" as="font" type="font/woff2" crossorigin>
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
    ('How is this different from a marketing agency?', ['A traditional agency staffs every task by hand, which makes it slow and expensive. We use AI for research, ideas, variations, scheduling and automated replies, so a small senior team delivers more in less time and spends its hours on decisions that move the business. You get the output of a full marketing team without hiring one.']),
    ('What services are included in a subscription?', ['Plans are built from four parts: <a href="/ai-marketing">AI marketing</a> (social media management, campaigns, ads, SEO and AEO), <a href="/ai-automation">AI automation</a> (WhatsApp and Instagram DM flows, lead capture, CRM and follow-ups), the <a href="/creative-studio">creative studio</a> (shoots, reel and video editing, graphic design) and <a href="/website-development">website development</a>. You choose what you need, and we scope it with you on a free call.']),
    ('How does the subscription work?', ['Each plan has a clear monthly scope and one point of contact. There is no long contract: you can change the scope, pause or stop at the end of any month. Pricing depends on the scope, so we share a written quote after a free strategy call, before any work starts.']),
    ('Do you work with businesses across India?', ['Yes. We work remotely with brands across India, from metros to smaller cities, and with international clients. Photo and video shoots are arranged on location when a project needs them.']),
    ('Will our content look AI-generated?', ['No. AI speeds up research and drafting, but strategists, designers and editors finish every piece in your brand style. Nothing is published until you approve it.']),
    ('Who owns the content and accounts?', ['You do. Final files, source files, ad accounts and any systems we set up belong to your business.']),
    ('How do we get started?', ['Book a free call through the <a href="/contact">contact page</a>. We review your brand and goals, send a scope and plan, and once you approve it we begin onboarding: brand kit, account access and a first-month plan.']),
]

FRAG = {
    'ads': '<div class="frag" data-ui><div class="fbox"><div class="fhead">Meta lead ads <small>Example · last 30 days</small></div><div class="kv3"><div><span>Spend</span><b>₹18,000</b></div><div><span>Leads</span><b>142</b></div><div><span>Per lead</span><b>₹127</b></div></div><div class="fhead"><span class="pillx ok">Optimised Tuesday</span><small>3 creatives in rotation</small></div></div></div>',
    'flow': '<div class="frag" data-ui><div class="fbox"><div class="fhead">Flow: price enquiry <small>Live</small></div><div class="flow"><div>New DM: "price?" <small>trigger</small></div><div>Ask budget and area <small>2 questions</small></div><div class="hot">Qualified lead <small>tagged hot</small></div><div>Owner notified <small>WhatsApp</small></div></div></div></div>',
    'reel': '<div class="frag" data-ui><div class="fbox"><div class="fhead">Reel · festive offer <small>0:28</small></div><div class="tl">\n        <div class="row">Video<div class="lane"><i class="d" style="flex:3"></i><i class="d" style="flex:2"></i><i class="d" style="flex:4"></i><i class="d" style="flex:2"></i></div></div>\n        <div class="row">Text<div class="lane"><i class="v" style="flex:2"></i><i class="l" style="flex:1"></i><i class="v" style="flex:3"></i><i class="l" style="flex:1"></i><i class="v" style="flex:4"></i></div></div>\n        <div class="row">Audio<div class="lane"><i style="flex:11"></i></div></div></div><div class="fhead"><span class="pillx v">Ready for review</span><small>Hook B approved</small></div></div></div>',
    'web': '<div class="frag" data-ui><div class="fbox"><div class="score"><b>98</b><div><div class="fhead">Performance</div><small class="soft">Mobile, landing page</small></div></div><div class="check"><div>Mobile-first layout<em>Pass</em></div><div>Schema markup<em>Pass</em></div><div>Enquiry form to WhatsApp<em>Pass</em></div></div></div></div>',
    'seo': '<div class="frag" data-ui><div class="fbox"><div class="fhead">Search readiness <small>Example · monthly check</small></div><div class="check"><div>Pages indexed on Google<em>7 of 7</em></div><div>Questions answered on page<em>36</em></div><div>Facts file for AI crawlers<em>Live</em></div></div></div></div>',
    'report': '<div class="frag" data-ui><div class="fbox"><div class="fhead">Leads by week <small>Example · 114 total</small></div><div class="bars" role="img" aria-label="Leads rising from 18 to 39 per week"><i style="height:46%"></i><i style="height:67%"></i><i style="height:79%"></i><i style="height:100%"></i></div><div class="fhead"><small>Week 1: 18</small><small>Week 4: 39</small></div></div></div>',
}

def home():
    a = icon('arrow')
    INDUSTRIES_HTML = ''.join(f'<a class="tile ind" href="{u}" data-rise><img src="/img/ind-{im}-480.webp" srcset="/img/ind-{im}-480.webp 480w, /img/ind-{im}-800.webp 800w" sizes="(max-width: 700px) 100vw, 33vw" width="480" height="360" loading="lazy" decoding="async" alt="{alt}"><h3>{t}</h3><p>{d}</p><ul>' + ''.join(f'<li>{x}</li>' for x in tags) + '</ul></a>' for (t, d, tags, u), (im, alt) in zip(INDUSTRIES, IND_IMG))
    GUIDE_CARDS = guide_cards()
    feed0 = [('pen', 'Content Agent', 'Drafted 3 hooks for the festive reel', 'now'), ('b:instagram', 'Reply Agent', 'Answered "price?" on Instagram in 4 s', '1m'),
             ('mega', 'Ads Agent', 'Shifted ₹2,000 to the better creative', '3m'), ('film', 'Edit Agent', 'Reel v2 ready: 0:28, captions on', '6m'), ('b:meta', 'Meta lead ad', 'New lead: Rahul, 2 BHK, Baner, call today', '8m'), ('b:whatsapp', 'Automation', 'Hot lead sent to the owner on WhatsApp', '9m')]
    feed = ''.join(f'<div class="row-f"><span class="av">{icon(i)}</span><div><b>{w}</b><small>{t}</small></div><em>{m}</em></div>' for i, w, t, m in feed0)
    agents_nav = [('Content Agent', True), ('Reply Agent', False), ('Ads Agent', False), ('Edit Agent', True), ('SEO Agent', False), ('Report Agent', False)]
    nav_ag = ''.join(f'<span class="ag">{n}<i class="{"busy" if b else ""}"></i></span>' for n, b in agents_nav)
    tools = [('whatsapp', 'WhatsApp'), ('instagram', 'Instagram'), ('meta', 'Meta Ads'), ('facebook', 'Facebook'), ('googleads', 'Google Ads'), ('youtube', 'YouTube'),
             ('google', 'Google Search'), ('googlemaps', 'Google Business'), ('shopify', 'Shopify'), ('googlesheets', 'Google Sheets'), ('hubspot', 'HubSpot'),
             ('razorpay', 'Razorpay'), ('zapier', 'Zapier'), ('googlegemini', 'Gemini')]
    mq = ''.join(f'<span>{brand(b, mono=True)}{t}</span>' for b, t in tools)
    tools_txt = ', '.join(t for _, t in tools)
    biz = [('cafe', 'Café or restaurant'), ('clinic', 'Clinic or wellness'), ('d2c', 'D2C or e-commerce brand'), ('realestate', 'Real estate'), ('education', 'Education'), ('creator', 'Creator or personal brand')]
    goals = [('leads', 'Leads'), ('sales', 'Sales'), ('bookings', 'Bookings'), ('awareness', 'Awareness')]
    chans = [('ch_ig', 'Instagram', True), ('ch_wa', 'WhatsApp', True), ('ch_meta', 'Meta ads', True), ('ch_google', 'Google ads', False), ('ch_web', 'Website', True)]
    seg = ''.join(f'<label><input type="radio" name="goal" value="{v}"' + (' checked' if v == 'leads' else '') + f'><span>{l}</span></label>' for v, l in goals)
    chips = ''.join(f'<label><input type="checkbox" name="{n}"' + (' checked' if c else '') + f'><span>{l}</span></label>' for n, l, c in chans)
    caps = [('Social media management', 'Instagram, Facebook, LinkedIn and YouTube'), ('Performance marketing', 'Meta and Google Ads, optimised weekly'),
            ('SEO and AEO', 'Rank on Google, get named by AI assistants'), ('Content strategy', 'A monthly calendar built on research'),
            ('Reels and short video', 'Hooks, subtitles, motion graphics, covers'), ('Product and brand shoots', 'Photo and video, on location'),
            ('Graphic design', 'Posts, carousels, ads, menus, print'), ('Brand identity', 'Logo, palette, templates, brand kit'),
            ('WhatsApp automation', 'Catalogue, FAQs, bookings, broadcasts'), ('Instagram DM automation', 'Instant replies to comments and messages'),
            ('Lead capture and CRM', 'Every enquiry logged and followed up'), ('Websites and landing pages', 'Fast, mobile-first, ready for search')]
    SVC = [('/ai-marketing', 'mega', 'AI Marketing', 'Campaigns and content planned on research and optimised every week.',
            ['Social media management', 'Meta and Google Ads', 'SEO and AEO', 'Content strategy and calendar']),
           ('/ai-automation', 'bolt', 'AI Automation', 'Replies, lead capture and follow-ups that run around the clock.',
            ['WhatsApp automation', 'Instagram DM automation', 'Lead capture and CRM', 'Booking and reminder flows']),
           ('/creative-studio', 'film', 'Creative Studio', 'Shoots, edits and design that look like your brand.',
            ['Reels and short video editing', 'Product and brand shoots', 'Graphic design', 'Brand identity']),
           ('/website-development', 'globe', 'Websites', 'Fast sites and landing pages that rank and turn visitors into enquiries.',
            ['Websites and landing pages', 'Mobile-first and fast', 'Built for Google and AI search', 'Enquiry and WhatsApp forms'])]
    SVC_HTML = ''.join(f'<a class="tile svc-c" href="{u}" data-rise><i>{icon(ic)}</i><h3>{t}</h3><p>{d}</p><ul>' + ''.join(f'<li>{x}</li>' for x in li) + f'</ul><span class="more">Explore {t} {icon("arrow")}</span></a>' for u, ic, t, d, li in SVC)
    node = lambda ic, t, s, cls='': f'<div class="node {cls}" data-n><i>{icon(ic)}</i><div><b>{t}</b><small>{s}</small></div></div>'
    body = f'''
<section class="hero" data-sec aria-labelledby="hero-h">
  <div class="hero-bg" aria-hidden="true"><canvas class="sky" data-sky></canvas></div>
  <div class="frame hero-in">
    <span class="kicker" data-rise><i>{icon("spark")}</i>AI agents plus human experts, on one subscription</span>
    <h1 id="hero-h" data-rise>Your AI growth <span class="g">team</span></h1>
    <p class="lead" data-rise>Nxtlvl Social is an AI-driven growth company in India. Our agents and experts run your marketing, automation and creative production every day, and a person checks every result.</p>
    <div class="btns" data-rise><a class="btn btn-primary" href="/contact">Book a free strategy call {a}</a><a class="btn btn-light" href="#agents">Meet the agents</a></div>
    <p class="hero-note" data-rise><span>Monthly plans</span><span>No lock-in</span><span>You own everything</span></p>
    <div class="console" data-ui data-rise role="img" aria-label="Example Nxtlvl workspace: AI agents drafting hooks, replying to messages, optimising ads and editing reels, with live counters and a WhatsApp booking.">
      <div class="c-top"><span class="dots"><i></i><i></i><i></i></span><b>Example workspace</b><span class="hide-s">· Café Aroma</span><span class="sp"></span><span class="live">Agents running</span></div>
      <div class="c-body">
        <div class="c-nav"><span class="on">{icon("chart")} Overview</span><span>{icon("pen")} Content</span><span>{icon("mega")} Campaigns</span><span>{icon("flow")} Automations</span><span>{icon("users")} Leads</span><small>Agents</small>{nav_ag}</div>
        <div class="c-main">
          <div class="stats"><div class="stat"><span>Tasks done today</span><b data-tick="128">128</b><small>by agents and team</small></div><div class="stat"><span>Messages answered</span><b data-tick="47">47</b><small>24/7, in seconds</small></div><div class="stat"><span>Leads this week</span><b data-tick="39">39</b><small>all logged</small></div></div>
          <div class="feed"><h4>Live activity <span>reviewed by your strategist</span></h4><div data-feed>{feed}</div></div>
          <svg class="spark" viewBox="0 0 600 64" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A95CFF" stop-opacity=".35"/><stop offset="1" stop-color="#A95CFF" stop-opacity="0"/></linearGradient></defs>
            <path class="a" d="M0 52 C60 50 90 44 140 46 S230 34 280 36 S370 22 420 24 S520 10 600 6 L600 64 L0 64Z"/><path class="l" d="M0 52 C60 50 90 44 140 46 S230 34 280 36 S370 22 420 24 S520 10 600 6"/></svg>
        </div>
        <div class="c-side"><h4><span class="h4b">{brand("whatsapp")}WhatsApp</span> <span data-ist>11:42 pm IST</span></h4>
          <div class="chat">
            <div class="chat-top"><span class="av">CA</span><div><b>Café Aroma</b><small>Reply Agent on</small></div></div>
            <div class="chat-body">
              <div class="msg in" data-step>Hi! Are you open tonight? Table for 4 at 8?<small data-time>11:42 pm</small></div>
              <div class="msg out" data-step>Hi Priya, yes, open till 11. I can hold a table for 4 at 8:00 pm. Shall I book it?<small data-time>11:42 pm</small></div>
              <div class="msg in" data-step>Yes please<small data-time>11:43 pm</small></div>
              <div class="msg out" data-step>Booked: table for 4, tonight at 8:00 pm. See you soon!<small data-time>11:43 pm</small></div>
              <div class="note" data-step>Lead saved · owner notified</div>
              <div class="typing" aria-hidden="true"><i></i><i></i><i></i></div>
            </div></div></div>
      </div>
    </div>
  </div>
  <div class="frame logos" data-rise><p>Works with the platforms your customers already use</p><div class="mq" role="img" aria-label="Platforms: {tools_txt}"><div class="track" aria-hidden="true">{mq}{mq}</div></div></div>
</section>

<section class="sec frame" id="agents" data-sec aria-labelledby="ag-h">
  <div class="sec-head center"><span class="kicker" data-rise><i>{icon("bot")}</i>Your AI team</span><h2 id="ag-h" data-rise>Meet your <span class="g">agents</span></h2>
    <p class="soft" data-rise>Six specialist AI agents work on your brand every day. A strategist directs them, and nothing goes live until a person and you approve it.</p></div>
  <div class="agents">
    <div class="tile agent glowline" data-rise><div class="top"><div class="who-a"><b><i>{icon("pen")}</i>Content Agent</b><span class="state">Writing</span></div><p>Researches trends and your best posts, then drafts hooks, scripts and captions.</p></div>
      <div class="stage" data-ui><div class="lbl"><span>Hooks for Friday's reel</span><span>3 of 3</span></div><div class="hooks" data-hooks><div>The one mistake buyers make...</div><div>We tested 3 offers. Here is the winner.</div><div class="cur"><span data-type>60 seconds inside our kitchen</span><span class="caret"></span></div></div></div></div>
    <div class="tile agent glowline" data-rise><div class="top"><div class="who-a"><b><i>{icon("chat")}</i>Reply Agent</b><span class="state">Online 24/7</span></div><p>Answers DMs, comments and WhatsApp messages in your voice, and books appointments.</p></div>
      <div class="stage" data-ui><div class="lbl"><span>Instagram DM</span><span>4 s reply</span></div><div class="mini-chat"><div class="b i">Price for the facial?</div><div class="b o">₹1,499, 60 minutes. Want Saturday at 11?</div><div class="b i">Yes!</div><div class="b o">Booked. See you Saturday.</div></div></div></div>
    <div class="tile agent glowline" data-rise><div class="top"><div class="who-a"><b><i>{icon("mega")}</i>Ads Agent</b><span class="state">Optimising</span></div><p>Watches Meta and Google campaigns daily and moves budget to what converts.</p></div>
      <div class="stage" data-ui><div class="lbl"><span>Budget split, live</span><span>Example</span></div><div class="budget"><div>Creative A<span class="track2"><i></i></span><b>Winner</b></div><div>Creative B<span class="track2"><i></i></span><b>Testing</b></div><div>Creative C<span class="track2"><i></i></span><b>Paused</b></div></div>
        <div class="lbl" style="margin-top:16px"><span>Cost per lead</span><span style="color:var(--green)">down this week</span></div></div></div>
    <div class="tile agent glowline" data-rise><div class="top"><div class="who-a"><b><i>{icon("film")}</i>Edit Agent</b><span class="state">Rendering</span></div><p>Rough-cuts reels with captions and beats, so editors spend their time on the finish.</p></div>
      <div class="stage" data-ui><div class="lbl"><span>Reel · festive offer</span><span>0:28</span></div><div class="edit"><div class="ln v"><i style="flex:3"></i><i style="flex:2"></i><i style="flex:4"></i><i style="flex:2"></i></div><div class="ln t"><i style="flex:2"></i><i style="flex:1;opacity:0"></i><i style="flex:3"></i><i style="flex:1;opacity:0"></i><i style="flex:4"></i></div><div class="ln a"><i style="flex:11"></i></div><span class="ph"></span></div>
        <div class="edit"><div class="cap"><span>Hook B approved</span><span>Captions on</span></div></div></div></div>
    <div class="tile agent glowline" data-rise><div class="top"><div class="who-a"><b><i>{icon("search")}</i>SEO Agent</b><span class="state">Climbing</span></div><p>Writes answers buyers search for, so you rank on Google and get named by AI assistants.</p></div>
      <div class="stage" data-ui><div class="lbl"><span>"best café near me"</span><span>Example</span></div><div class="rank"><div class="you"><b>1</b>Your brand</div><div><b>2</b>Competitor café</div><div><b>3</b>Food blog list</div><div><b>4</b>Another café</div></div></div></div>
    <div class="tile agent glowline" data-rise><div class="top"><div class="who-a"><b><i>{icon("chart")}</i>Report Agent</b><span class="state">Counting</span></div><p>Pulls every channel into one plain-language monthly report, with next month's plan.</p></div>
      <div class="stage" data-ui><div class="lbl"><span>This month · example</span><span>Auto-updated</span></div><div class="nums"><div><span>Reach</span><b data-count="48200">48,200</b><small>up 31%</small></div><div><span>Enquiries</span><b data-count="114">114</b><small>up 22%</small></div><div><span>Bookings</span><b data-count="63">63</b><small>up 18%</small></div><div><span>Replies</span><b data-count="412">412</b><small>24/7</small></div></div></div></div>
  </div>
</section>

<section class="sec frame" data-sec aria-labelledby="fl-h">
  <div class="sec-head"><span class="kicker" data-rise><i>{icon("bolt")}</i>Automations</span><h2 id="fl-h" data-rise>Every enquiry, handled in <span class="g">seconds</span></h2>
    <p class="soft" data-rise>Messages from Instagram, WhatsApp, your website and ads flow to one agent. It answers, qualifies and books, logs the lead, and hands the important ones to your team.</p></div>
  <div class="flowbox" data-flow data-rise>
    <svg class="wires" aria-hidden="true"><defs><linearGradient id="wg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7D18FC"/><stop offset="1" stop-color="#D8BBFF"/></linearGradient></defs></svg>
    <div class="nodes">
      <div class="col c1">{node("b:instagram", "Instagram DM", "Price? Timings?", "br")}{node("b:whatsapp", "WhatsApp", "Booking request", "br")}{node("globe", "Website form", "Quote needed")}{node("b:meta", "Meta lead ad", "New lead", "br")}</div>
      <div class="col c2"><div class="node brain" data-n data-brain><i>{icon("bot")}</i><div><b>Nxtlvl Agent</b><small>Understands, answers, qualifies</small></div></div></div>
      <div class="col c3">{node("chat", "Replied in your voice", "In seconds, 24/7")}{node("users", "Lead qualified", "Budget, area, timeline")}{node("calendar", "Booking created", "Reminder scheduled")}</div>
      <div class="col c4">{node("b:googlesheets", "Saved to CRM", "Sheets, HubSpot or Zoho", "done br")}{node("b:whatsapp", "Owner notified", "On WhatsApp", "done br")}{node("refresh", "Follow-up in 24 h", "If no reply", "done")}</div>
    </div>
    <div class="flow-cap"><span><b>24/7</b> replies</span><span><b>100%</b> of leads logged</span><span><b>1 tap</b> human handover</span></div>
  </div>
</section>

<section class="sec frame" id="industries" data-sec aria-labelledby="ind-h">
  <div class="sec-head"><span class="kicker" data-rise><i>{icon("users")}</i>Industries</span><h2 id="ind-h" data-rise>AI marketing for <span class="g">every</span> kind of business</h2>
    <p class="soft" data-rise>The same agents and team, tuned to how your customers buy.</p></div>
  <div class="inds">{INDUSTRIES_HTML}</div>
  <p class="cities" data-rise>We work with brands anywhere in India, including Mumbai, Delhi NCR, Bengaluru, Pune, Hyderabad, Chennai, Kolkata, Ahmedabad, Jaipur, Chandigarh, Lucknow and Indore, and with clients abroad.</p>
</section>

<section class="sec frame" id="build" data-sec aria-labelledby="plan-h">
  <div class="sec-head"><span class="kicker" data-rise><i>{icon("calendar")}</i>Try it</span><h2 id="plan-h" data-rise>Build your month</h2>
    <p class="soft" data-rise>Pick your business, goal and channels. This is the plan our agents and team would start you on, and it changes as you do.</p></div>
  <div class="demo" id="planner" data-rise>
    <div class="plan" data-ui data-plan aria-live="polite">
      <div class="plan-head"><div><h3>Your month as a café or restaurant</h3><p>Planned for more leads. AI drafts, your strategist approves.</p></div><span class="plan-count">26 deliverables</span></div>
      <div class="groups"><div class="group"><b>Creative Studio</b><ul><li>8 reels with hooks, captions and covers</li><li>6 carousels and posts</li><li>4 story sets</li><li>1 shoot day: food and space shoot</li></ul></div>
        <div class="group"><b>AI Marketing</b><ul><li>Instagram calendar, posting and replies</li><li>Meta lead ads</li><li>Monthly report on more leads</li></ul></div>
        <div class="group"><b>AI Automation</b><ul><li>Menu, timings and offers on DM</li><li>Table booking on WhatsApp</li><li>Every lead logged and sent to your WhatsApp</li></ul></div>
        <div class="group"><b>Websites</b><ul><li>Order and reservation page</li><li>Speed, SEO and AEO checks</li></ul></div></div>
    </div>
    <form class="controls" aria-label="Plan options" onsubmit="return false">
      <div class="ctl"><label for="biz">Your business</label><select id="biz" name="biz">{''.join(f'<option value="{v}">{l}</option>' for v, l in biz)}</select></div>
      <div class="ctl" role="radiogroup" aria-labelledby="goal-l"><span id="goal-l">Main goal</span><div class="seg">{seg}</div></div>
      <div class="ctl" role="group" aria-labelledby="ch-l"><span id="ch-l">Channels</span><div class="chips">{chips}</div></div>
      <div class="ctl"><label for="reels">Reels a month</label><div class="range"><input id="reels" name="reels" type="range" min="4" max="20" step="2" value="8"><output for="reels">8</output></div></div>
      <div class="ctl"><label for="shoot">Shoot days</label><select id="shoot" name="shoot"><option value="0">None, we edit your footage</option><option value="1" selected>1 a month</option><option value="2">2 a month</option></select></div>
      <a class="btn btn-primary" href="/contact?need=marketing" data-plan-cta>Send me this plan {a}</a>
    </form>
  </div>
</section>

<section class="sec frame" id="services" data-sec aria-labelledby="eng-h">
  <div class="sec-head"><span class="kicker" data-rise><i>{icon("layers")}</i>Services</span><h2 id="eng-h" data-rise>Four services, one team</h2>
    <p class="soft" data-rise>Pick what your brand needs this quarter. Everything shares one plan, one strategist and one monthly report.</p></div>
  <div class="svc">{SVC_HTML}</div>
</section>

<section class="sec frame" data-sec aria-labelledby="how-h">
  <div class="sec-head"><span class="kicker" data-rise><i>{icon("refresh")}</i>How it works</span><h2 id="how-h" data-rise>From first call to compounding growth</h2></div>
  <div class="steps2" data-rise>
    <div class="step2"><span class="dot">{icon("search")}</span><h3>Discover</h3><p>A free strategy call and an audit of your brand, channels, competitors and goals.</p></div>
    <div class="step2"><span class="dot">{icon("bot")}</span><h3>Agents draft</h3><p>Research, calendars, scripts, creatives and automations, drafted in hours.</p></div>
    <div class="step2"><span class="dot">{icon("users")}</span><h3>People finish</h3><p>Strategists, editors and designers polish everything. You approve.</p></div>
    <div class="step2"><span class="dot">{icon("trend")}</span><h3>It compounds</h3><p>We publish, automate and report monthly, and each month gets sharper.</p></div>
  </div>
</section>

<section class="sec frame" data-sec aria-labelledby="proof-h">
  <div class="sec-head"><span class="kicker" data-rise><i>{icon("trend")}</i>Proof</span><h2 id="proof-h" data-rise>We grow our own page first</h2>
    <p class="soft" data-rise>Our Instagram, @ai.nxtlvl, is our lab: every format, hook and automation is tested there before it reaches a client.</p></div>
  <div class="proof">
    <div class="tile shot" data-rise><img src="/img/ai-nxtlvl-profile.jpg" width="1320" height="1245" alt="The @ai.nxtlvl Instagram profile by Nxtlvl Social: 31 posts, 9,924 followers and 1.0M views in the last 30 days" loading="lazy">
      <p class="over">Screenshot of @ai.nxtlvl. <a href="https://www.instagram.com/ai.nxtlvl/" rel="noopener" target="_blank">See the page</a></p></div>
    <div class="facts">
      <div class="tile bigstat" data-rise><b data-count="9924">9,924</b><span>followers on @ai.nxtlvl</span></div>
      <div class="tile pale bigstat" data-rise><b data-count="1000000" data-fmt="m">1.0M</b><span>views in the last 30 days</span></div>
      <div class="tile bigstat" data-rise><b data-count="31">31</b><span>posts to get there</span></div>
    </div>
  </div>
</section>
<section class="sec frame" data-sec aria-labelledby="plat-h">
  <div class="tile night platform glowline" data-rise>
    <div style="display:grid;gap:18px"><span class="kicker"><i>{icon("bolt")}</i>Coming next</span><h2 id="plat-h">The Nxtlvl growth platform</h2>
      <p class="soft">An AI workspace that turns one line into ideas, scripts and ready-to-post reels, with our team one message away. Subscribers get early access.</p>
      <div class="btns"><a class="btn btn-primary" href="/contact?need=platform">Ask about early access {a}</a></div></div>
    <div class="prompt" data-ui aria-hidden="true"><div class="in-p"><b data-prompt>Make a Diwali offer reel for my café</b><i>{icon("arrow")}</i></div>
      <div class="outs"><div><b>Idea</b>Behind the counter at 6 am, one sweet at a time</div><div><b>Script</b>0:00 hook · 0:04 offer · 0:22 call to action</div><div><b>Reel</b><i></i></div></div></div>
  </div>
</section>

<section class="sec frame" data-sec aria-labelledby="gd-h">
  <div class="sec-head"><span class="kicker" data-rise><i>{icon("pen")}</i>Guides</span><h2 id="gd-h" data-rise>Learn how AI-driven growth works</h2>
    <p class="soft" data-rise>Practical guides from our team on automation, marketing and AI for Indian businesses.</p></div>
  <div class="guides">{GUIDE_CARDS}</div>
</section>

{faq_block(HOME_FAQ)}
{close_row()}
'''
    return page('/index', 'AI-Driven Marketing, Automation & Creative | Nxtlvl Social',
                'Nxtlvl Social is an AI-driven growth company in India. AI agents and experts run your marketing, WhatsApp and DM automation, shoots, edits, design and websites.',
                body, '/', extra_schema=[faq_schema(HOME_FAQ)])

# ---------------------------------------------------------------- service pages
SERVICE_FRAGS = {
    '/ai-marketing': [('ads', 'Campaigns, optimised weekly', 'An example Meta lead campaign after 30 days: spend, leads and cost per lead, with the creatives we rotate.'),
                      ('report', 'One report a month', 'Results against the goal we agreed, in plain words, and what we will change next month.')],
    '/ai-automation': [('flow', 'Flows that qualify leads', 'An example price-enquiry flow: two quick questions, a hot lead tagged, and the owner told on WhatsApp.'),
                       ('report', 'Every lead counted', 'Leads your automations capture, week by week, in the monthly report.')],
    '/creative-studio': [('reel', 'Edited for the first second', 'An example reel timeline: cuts, captions and audio, with the approved hook marked.'),
                         ('ads', 'Creatives that run as ads', 'The same shoot feeds posts, reels and ad creatives, tested against each other.')],
    '/website-development': [('web', 'Fast and ready for search', 'Every page is checked for speed, mobile layout, schema markup and working enquiry forms.'),
                             ('seo', 'Found on Google and by AI', 'Search readiness is checked monthly once the site is live.')],
}

def service_page(path, name, title, desc, h1, intro, facts, included, how, who, faqs, need, extra_html=''):
    crumbs = [('/', 'Home'), (path, name)]
    a = icon('arrow'); ne = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
    inc = ''.join(f'<div data-rise><b>{t}</b><span>{d}</span></div>' for _, t, d in included)
    words = ['First', 'Then', 'Next', 'Finally']
    fields = ''.join(f'<div class="field" data-rise>' + (f'<h2 id="how-h">How it works</h2>' if i == 0 else '<span></span>') +
                     f'<div class="clause"><p>{t}</p><p>{d}</p></div></div>' for i, (t, d) in enumerate(how))
    facts_html = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)
    practice = ''.join(f'<div class="cell{" rev" if i % 2 else ""}" data-rise><div class="txt"><b>{t}</b><span>{d}</span></div>{FRAG[k]}</div>' for i, (k, t, d) in enumerate(SERVICE_FRAGS.get(path, [])))
    who_html = ''.join(f'<div data-rise>{w}</div>' for w in who)
    bgs = ['', 't2', 'pale']
    others = ''.join(f'<a class="tile engine {bgs[i % 3]}" href="{u}" data-rise><b>{n}</b><span>{s}</span></a>' for i, (u, n, s, _, _) in enumerate(x for x in SERVICES if x[0] != path))
    svc = {'@type': 'Service', '@id': SITE + path + '#service', 'name': name, 'serviceType': name, 'url': SITE + path, 'description': desc,
           'provider': {'@id': f'{SITE}/#org'}, 'areaServed': {'@type': 'Country', 'name': 'India'},
           'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': name, 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': t}} for _, t, _ in included]}}
    body = f'''
<section class="frame" data-sec aria-labelledby="ph-h"><div class="ph">
  <div class="tile main" data-rise>{crumbs_html(crumbs)}<h1 id="ph-h">{h1}</h1><p class="lead soft">{intro}</p>
    <div class="btns"><a class="btn btn-primary" href="/contact?need={need}">Book a free call {a}</a><a class="btn btn-light" href="#included">What is included</a></div></div>
  <aside class="tile night aside" data-rise aria-labelledby="glance-h"><h2 id="glance-h">{name} at a glance</h2><dl>{facts_html}</dl></aside>
</div></section>

<section class="sec frame" id="included" data-sec aria-labelledby="inc-h">
  <div class="sec-head"><h2 id="inc-h" data-rise>What we do for you</h2></div>
  <div class="items">{inc}</div>
</section>
<section class="sec frame" data-sec aria-labelledby="prac-h">
  <div class="sec-head"><h2 id="prac-h" data-rise>What it looks like</h2></div>
  <div class="cells two">{practice}</div>
</section>
{extra_html}
<section class="sec" data-sec aria-labelledby="how-h"><div class="fields short">{fields}</div></section>

<section class="sec frame" data-sec aria-labelledby="who-h"><div class="who">
  <div class="tile night" data-rise><h2 id="who-h">Who it is for</h2><p class="soft">Not sure this fits? <a href="/contact?need={need}">Tell us about your business</a> and we will say honestly whether we can help.</p></div>
  <div class="list">{who_html}</div>
</div></section>

{faq_block(faqs, f'{name}, answered')}

<section class="sec frame" data-sec aria-labelledby="more-h">
  <div class="sec-head"><h2 id="more-h" data-rise>Pairs well with</h2></div>
  <div class="h-row" style="grid-template-columns:repeat(3,minmax(0,1fr))">{others}</div>
</section>
{close_row()}
'''
    return page(path, title, desc, body, path, crumbs, [svc, faq_schema(faqs)])

MARKETING = dict(
    path='/ai-marketing', name='AI Marketing', need='marketing',
    title='AI Marketing & Social Media Management in India | Nxtlvl',
    desc='AI-driven social media management, marketing campaigns, Meta and Google Ads, SEO and AEO for brands in India. Planned with AI, run by strategists.',
    h1='AI marketing for growing brands',
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
    h1='AI automation for business',
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
          ('Will customers know it is automated?', ['We write replies in your brand voice and make it clear when a message is automated. Customers can reach a person at any point, and complex or sensitive conversations are handed over automatically.']),
          ('Do I need the WhatsApp Business API?', ['Not always. Simple setups work with the WhatsApp Business app; larger volumes, multiple team members and advanced flows need the WhatsApp Business Platform. We recommend the right option on the free call.']),
          ('Which CRM do you use?', ['We work with what you already have. If you have nothing yet, we set up a simple CRM or a Google Sheet that your team can use from day one.'])])

CREATIVE = dict(
    path='/creative-studio', name='Creative Studio', need='creative',
    title='Shoots, Reel Editing & Graphic Design Studio | Nxtlvl Social',
    desc='Product and brand shoots, reel and video editing, and graphic design for brands in India. AI-assisted production, finished by editors and designers.',
    h1='Shoots, edits and design',
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
    h1='Websites that rank and convert',
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
          ('Can the site connect to WhatsApp and my CRM?', ['Yes. Forms, WhatsApp buttons and booking tools can feed straight into your inbox, CRM or the automations we build in <a href="/ai-automation">AI automation</a>.']),
          ('Do you redesign existing websites?', ['Yes. We can redesign and rebuild an existing site, keeping the pages that already rank and redirecting old addresses so you keep your search traffic.'])])

# ---------------------------------------------------------------- about and contact
def about():
    crumbs = [('/', 'Home'), ('/about', 'About')]
    body = f'''
<section class="frame" data-sec aria-labelledby="ph-h"><div class="ph">
  <div class="tile main" data-rise>{crumbs_html(crumbs)}<h1 id="ph-h">Growth, built around AI</h1>
    <p class="lead soft">Nxtlvl Social (Next Level Social) gives businesses the marketing, automation and creative capacity of a full team, on one monthly subscription.</p></div>
  <aside class="tile night aside" data-rise aria-labelledby="glance-h"><h2 id="glance-h">In short</h2><dl>
    <div><dt>What we are</dt><dd>An AI-driven growth company in India</dd></div><div><dt>What we do</dt><dd>Marketing, automation, creative production and websites</dd></div>
    <div><dt>How we work</dt><dd>AI for speed, people for judgement</dd></div><div><dt>How you pay</dt><dd>A monthly subscription, no lock-in</dd></div></dl></aside>
</div></section>
<section class="sec frame" data-sec aria-labelledby="ab-h"><div class="about">
  <div class="prose" data-rise>
    <h2 id="ab-h" style="margin-top:0">Growth should not need a big team</h2>
    <p>Most growing businesses face the same choice: hire an expensive agency, build an in-house team they cannot yet afford, or try to do everything themselves. We started Nxtlvl Social to offer a better option.</p>
    <p>We work like a technology company. AI systems handle research, first drafts, repetitive tasks and round-the-clock customer replies. A small, senior team sets the strategy, directs the creative and checks every result. You get a partner that moves fast, costs less than a traditional agency and still feels personal.</p>
    <h2>What we do</h2>
    <ul><li><strong>Marketing:</strong> <a href="/ai-marketing">social media management, campaigns, paid ads, SEO and AEO</a>, for growth on social and beyond it.</li>
      <li><strong>Automation:</strong> <a href="/ai-automation">WhatsApp and Instagram automation, lead capture, CRM and follow-ups</a>.</li>
      <li><strong>Creativity:</strong> <a href="/creative-studio">shoots, reel and video editing, graphic design and brand identity</a>, plus <a href="/website-development">websites and landing pages</a>.</li></ul>
    <h2>How we work</h2>
    <ul><li><strong>AI for speed, people for judgement.</strong> Every output is reviewed by a person, and nothing goes live without your approval.</li>
      <li><strong>Subscriptions, not one-off projects.</strong> Growth compounds when the same team learns your business month after month.</li>
      <li><strong>Clear numbers.</strong> We agree on the metrics that matter and report on them every month.</li>
      <li><strong>You own everything.</strong> Files, accounts and systems belong to your business.</li></ul>
    <h2>What is next</h2>
    <p>We are building the Nxtlvl growth platform: an AI workspace that turns a brief into ideas, scripts and ready-to-post reels, with our team one message away. Today we deliver that work for clients with AI tools and our own hands; subscribers will be first to use the platform.</p>
  </div>
  <div class="facts">
    <div class="tile shot" style="padding:0;min-height:0" data-rise><img src="/img/ai-nxtlvl-profile.jpg" width="1320" height="1245" alt="The @ai.nxtlvl Instagram profile by Nxtlvl Social" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover;object-position:top left"></div>
    <div class="tile t2" data-rise><p class="small soft">Our own lab</p><p style="font-size:var(--step-lead);font-weight:600;letter-spacing:-0.02em;line-height:1.2">@ai.nxtlvl: nearly 10,000 followers in 31 posts</p></div>
    <div class="tile violet" data-rise><p style="font-size:var(--step-lead);font-weight:600;letter-spacing:-0.02em;line-height:1.2">Want to work with us?</p><div class="btns" style="margin-top:16px"><a class="btn btn-white" href="/contact">Book a free call</a></div></div>
  </div>
</div></section>
{close_row()}
'''
    return page('/about', 'About Nxtlvl Social: An AI-Driven Growth Company in India',
                'Nxtlvl Social is an AI-driven growth company providing marketing, automation and creative solutions for businesses in India on monthly subscriptions.',
                body, '/about', crumbs, page_type='AboutPage')

CONTACT_FAQ = [('What happens on the free call?', ['We spend about 20 minutes on your business, goals and current channels, answer your questions and suggest where AI, automation and creative work can help most. Afterwards we send a written scope and quote.']),
               ('Is the call really free?', ['Yes, with no obligation. If we are not the right fit, we will say so and point you in a better direction.']),
               ('How quickly do you reply?', ['We reply to every request by email within one business day.'])]

def contact():
    crumbs = [('/', 'Home'), ('/contact', 'Contact')]
    social = ''.join(f'<a class="link" href="{u}" rel="noopener" target="_blank">{e(t.split(" · ")[1])}</a> ' for t, u in INSTAGRAM)
    body = f'''
<section class="frame" data-sec aria-labelledby="ph-h"><div class="contact" style="padding-top:4px">
  <div class="tile form" data-rise>{crumbs_html(crumbs)}<h1 id="ph-h" style="font-size:clamp(2.5rem,1.2rem + 4.8vw,5rem);margin:20px 0 14px">Book a free growth call</h1>
    <p class="lead soft" style="max-width:44ch;margin-bottom:32px">Tell us about your brand and what you want to grow. We reply within one business day to set up a 20-minute call.</p>
    <h2 id="book-h" class="sr">Booking form</h2>{contact_form()}</div>
  <div class="aside">
    <div class="tile night" data-rise><p class="small soft">Email</p><p style="font-size:var(--step-lead);font-weight:600;letter-spacing:-0.02em;overflow-wrap:anywhere"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
    <div class="tile t2" data-rise><p class="small soft">Instagram</p><p style="font-size:18px;font-weight:500;display:grid;gap:4px">{social}</p></div>
    <div class="tile pale" data-rise><p class="small soft">Where we work</p><p style="font-size:18px;font-weight:500">Remote-first across India and abroad. Shoots on location.</p></div>
    <div class="tile" data-rise><p class="small soft">Response time</p><p style="font-size:18px;font-weight:500">Within one business day</p></div>
  </div>
</div></section>
{faq_block(CONTACT_FAQ, 'Before you book')}
'''
    return page('/contact', 'Contact Nxtlvl Social: Book a Free Growth Call',
                'Book a free 20-minute strategy call with Nxtlvl Social for AI marketing, automation, creative production or a new website. We reply within one business day.',
                body, '/contact', crumbs, [faq_schema(CONTACT_FAQ)], page_type='ContactPage')

def not_found():
    body = f'''<section class="frame" data-sec aria-labelledby="nf-h"><div class="ph"><div class="tile main" style="grid-column:1/-1"><h1 id="nf-h">This page took a different route</h1>
<p class="lead soft">The page you are looking for has moved or no longer exists.</p>
<div class="btns"><a class="btn btn-primary" href="/">Go to the home page</a><a class="btn btn-light" href="/contact">Contact us</a></div></div></div></section>'''
    return page('/404', 'Page not found | Nxtlvl Social', 'This page could not be found.', body, noindex=True)

# ---------------------------------------------------------------- industries and guides
INDUSTRIES = [
    ('Restaurants and cafés', 'Reels that fill tables, DM and WhatsApp replies for menus and bookings, festive campaigns.', ['Reels', 'Table booking', 'Festive offers'], '/creative-studio'),
    ('Clinics and wellness', 'Appointment booking on WhatsApp, treatment questions answered 24/7, content that builds trust.', ['Bookings', 'Reminders', 'Trust content'], '/ai-automation'),
    ('D2C and e-commerce', 'Product shoots, performance ads that scale, and order and delivery replies on autopilot.', ['Product shoots', 'Meta ads', 'Order replies'], '/ai-marketing'),
    ('Real estate', 'Lead qualification by budget and area, site-visit booking, project walkthrough videos.', ['Lead scoring', 'Site visits', 'Walkthroughs'], '/ai-automation'),
    ('Education and coaching', 'Admission enquiries answered instantly, demo-class bookings and student stories.', ['Admissions', 'Demo classes', 'Reels'], '/ai-marketing'),
    ('Creators and personal brands', 'Editing, a weekly content system, comment-to-DM links and collab enquiry routing.', ['Editing', 'Content system', 'DM links'], '/creative-studio'),
]
IND_IMG = [('cafe', 'Barista plating a latte while a phone films it for a reel'), ('clinic', 'Clinic receptionist checking appointments on a tablet'),
           ('d2c', 'Product shoot of skincare serum bottles in a studio'), ('realestate', 'Couple viewing a new apartment while an agent films a walkthrough'),
           ('coaching', 'Teacher explaining diagrams to students in a coaching class'), ('creator', 'Content creator reviewing a clip in her home studio')]
from guides import GUIDES

def guide_cards():
    return ''.join(f'<a class="tile guide" href="/guides/{g["slug"]}" data-rise><img src="/img/guide-{g["slug"]}-640.webp" width="640" height="360" loading="lazy" decoding="async" alt=""><span class="tag">{g["tag"]} · {g["read"]}</span><h3>{g["h1"]}</h3><p>{g["desc"]}</p><span class="go">Read the guide {icon("arrow")}</span></a>' for g in GUIDES)

def guide_page(g):
    path = f'/guides/{g["slug"]}'
    crumbs = [('/', 'Home'), ('/guides', 'Guides'), (path, g['h1'])]
    body_html = ''.join(f'<h2 id="s{i}">{t}</h2>' + ''.join(x if x.startswith('<') else f'<p>{x}</p>' for x in paras) for i, (t, paras) in enumerate(g['sections']))
    toc = ''.join(f'<li><a href="#s{i}">{t}</a></li>' for i, (t, _) in enumerate(g['sections']))
    art = {'@type': 'Article', '@id': SITE + path + '#article', 'headline': g['title'], 'description': g['desc'], 'image': f'{SITE}/img/og-{g["slug"]}.jpg',
           'author': {'@id': f'{SITE}/#org'}, 'publisher': {'@id': f'{SITE}/#org'}, 'datePublished': UPDATED, 'dateModified': UPDATED,
           'mainEntityOfPage': SITE + path, 'inLanguage': 'en-IN', 'about': g['tag']}
    body = f'''
<section class="frame" data-sec aria-labelledby="ph-h"><div class="ph" style="grid-template-columns:1fr">
  <div class="tile main" data-rise style="min-height:0">{crumbs_html(crumbs)}<h1 id="ph-h" style="max-width:20ch">{g["h1"]}</h1>
    <p class="meta"><span>{g["tag"]}</span><span>{g["read"]}</span><span>By the Nxtlvl Social team</span><span>Updated 20 November 2026</span></p></div>
</div></section>
<div class="frame cover" data-rise><img src="/img/guide-{g["slug"]}-1280.webp" srcset="/img/guide-{g["slug"]}-640.webp 640w, /img/guide-{g["slug"]}-1280.webp 1280w" sizes="(max-width: 1280px) 100vw, 1280px" width="1280" height="720" alt="{g["cover_alt"]}" fetchpriority="high"></div>
<section class="sec frame" style="padding-top:48px" data-sec><div class="article">
  <article class="body" data-rise><p class="answer">{g["answer"]}</p>{body_html}</article>
  <aside><div class="tile"><h2>On this page</h2><ol>{toc}</ol></div>
    <div class="tile violet"><p style="font-family:var(--display);font-weight:600;font-size:20px;letter-spacing:-0.02em;line-height:1.2">Want this done for you?</p><p class="soft" style="margin:10px 0 16px;font-size:15px">Our agents and team set it up and run it, on one monthly plan.</p><a class="btn btn-white" href="/contact?need={g["need"]}">Book a free call</a></div>
    <div class="tile t2"><p class="small soft">Related service</p><p style="margin-top:6px"><a href="{g["service"]}">{dict((u, n) for u, n, *_ in SERVICES)[g["service"]]}</a></p></div></aside>
</div></section>
{faq_block(g["faqs"], 'Questions, answered')}
{close_row()}
'''
    return page(path, g['title'] + ' | Nxtlvl Social', g['desc'], body, '/guides', crumbs, [art, faq_schema(g['faqs'])], og_image=f'/img/og-{g["slug"]}.jpg')

def guides_hub():
    crumbs = [('/', 'Home'), ('/guides', 'Guides')]
    body = f'''
<section class="frame" data-sec aria-labelledby="ph-h"><div class="ph">
  <div class="tile main" data-rise>{crumbs_html(crumbs)}<h1 id="ph-h">Guides to AI-driven growth</h1>
    <p class="lead">Practical, plain-language guides on AI marketing, WhatsApp and Instagram automation and content for businesses in India.</p></div>
  <aside class="tile night aside" data-rise><h2>Start here</h2><dl><div><dt>New to AI marketing?</dt><dd><a href="/guides/ai-marketing-for-small-business-india">AI marketing for small businesses</a></dd></div>
    <div><dt>Drowning in WhatsApp messages?</dt><dd><a href="/guides/whatsapp-automation-for-business">WhatsApp automation for business</a></dd></div>
    <div><dt>Too many DMs?</dt><dd><a href="/guides/instagram-dm-automation">Instagram DM automation</a></dd></div></dl></aside>
</div></section>
<section class="sec frame" data-sec aria-label="All guides"><div class="guides">{guide_cards()}</div></section>
{close_row()}
'''
    coll = {'@type': 'CollectionPage', '@id': f'{SITE}/guides#list', 'name': 'Guides to AI-driven growth', 'hasPart': [{'@type': 'Article', 'headline': g['title'], 'url': f'{SITE}/guides/{g["slug"]}'} for g in GUIDES]}
    return page('/guides', 'Guides: AI Marketing and Automation for Indian Businesses | Nxtlvl Social',
                'Practical guides on AI marketing, WhatsApp automation, Instagram DM automation and content for small businesses and brands in India.', body, '/guides', crumbs, [coll])

# ---------------------------------------------------------------- write
def main():
    pages = {'index.html': home(), 'about.html': about(), 'contact.html': contact(), '404.html': not_found(), 'guides.html': guides_hub()}
    os.makedirs(os.path.join(OUT, 'guides'), exist_ok=True)
    for g in GUIDES:
        pages[f'guides/{g["slug"]}.html'] = guide_page(g)
    for d in (MARKETING, AUTOMATION, CREATIVE, WEBSITES):
        pages[d['path'].strip('/') + '.html'] = service_page(**d)
    for name, content in pages.items():
        with open(os.path.join(OUT, name), 'w') as f:
            f.write(content)
    for asset in ('site.css', 'site.js'):
        shutil.copy(os.path.join(HERE, asset), os.path.join(OUT, asset))
    urls = ['/', '/ai-marketing', '/ai-automation', '/creative-studio', '/website-development', '/guides'] + [f'/guides/{g["slug"]}' for g in GUIDES] + ['/about', '/contact']
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

## Guides

- [WhatsApp automation for business]({SITE}/guides/whatsapp-automation-for-business)
- [Instagram DM automation]({SITE}/guides/instagram-dm-automation)
- [AI marketing for small businesses in India]({SITE}/guides/ai-marketing-for-small-business-india)

## Pages

- [Home]({SITE}/)
- [About]({SITE}/about)
- [Contact]({SITE}/contact)
"""

if __name__ == '__main__':
    main()
