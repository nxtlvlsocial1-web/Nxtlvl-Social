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

def star_svg(uid='s', dark=False):
    main = '#0B0816' if dark else '#FFFFFF'
    g = lambda gid, col, x1, y1, x2, y2: (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
        f'<stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".55" stop-color="{col}" stop-opacity=".9"/><stop offset="1" stop-color="{col}"/></linearGradient>')
    return (f'<svg viewBox="20.6 31.6 147.8 147.8" aria-hidden="true"><defs>{g(uid + "a", main, 28.3, 171.7, 121.6, 78.4)}{g(uid + "b", "#A95CFF", 69.3, 164.7, 121.6, 112.3)}'
            f'{g(uid + "c", "#7D18FC" if dark else "#B98AFF", 43.8, 122.2, 82.0, 84.0)}</defs><path d="{STAR["t0"]}" fill="url(#{uid}a)"/><path d="{STAR["t1"]}" fill="url(#{uid}b)"/>'
            f'<path d="{STAR["t2"]}" fill="url(#{uid}c)"/><path d="{STAR["s"]}" fill="{main}"/></svg>')

# ---------------------------------------------------------------- shared blocks
NAV = [('/ai-marketing', 'Marketing'), ('/ai-automation', 'Automation'), ('/creative-studio', 'Creative'), ('/website-development', 'Websites'), ('/about', 'About')]
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
<header class="bar frame">
  <div class="in">
    <a class="logo" href="/" aria-label="Nxtlvl Social home">{star_svg("lg", dark=True)}<b>nxtlvl<span>social</span></b></a>
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
    return f'''<footer class="frame" data-sec>
  <div class="bigmark" aria-hidden="true" data-rise>{star_svg("ft")}<b>nxtlvl<span>social</span></b></div>
  <div class="fcols">
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Company</h2><ul><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li><li><a href="/#faq">Questions</a></li></ul></div>
    <div><h2>Follow</h2><ul>{social}</ul></div>
    <div><h2>Write to us</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
    <div><p>Nxtlvl Social is an AI-driven growth company in India. Marketing, automation and creative production on one monthly subscription, made with AI and finished by people.</p></div>
  </div>
  <div class="legal"><span>© 2026 Nxtlvl Social · AI-driven marketing, automation and creative services, India</span><a class="btn btn-white" href="/contact">Book a free call</a></div>
</footer>'''

def faq_block(items, title='Questions, answered'):
    bands = ''.join(f'<div class="band" data-rise><h3>{e(q)}</h3><div class="a">{"".join(f"<p>{x}</p>" for x in a)}</div></div>' for q, a in items)
    return f'''<section class="faq" id="faq" data-sec aria-labelledby="faq-h"><div class="band head"><h2 id="faq-h">{title}</h2></div>{bands}</section>'''

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

def close_row(title='Let us plan your growth', sub='Leave your email and we will set up a free 20-minute strategy call. You get a written plan, whether or not you work with us.'):
    return f'''<section class="sec frame" data-sec aria-labelledby="close-h"><div class="close">
  <div class="side-a" data-rise></div>
  <div class="main" data-rise><h2 id="close-h">{title}</h2><p>{sub}</p>
    <form action="/contact" method="get" aria-label="Start with your email"><label class="sr" for="close-email">Work email</label><input id="close-email" name="email" type="email" placeholder="you@company.com" autocomplete="email"><input type="hidden" name="need" value="unsure"><button class="btn btn-dark" type="submit">Book a free call {icon("arrow")}</button></form></div>
  <div class="side-b" data-rise>{star_svg("cl")}</div>
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
<meta name="theme-color" content="#F7F6FB">
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
<link rel="preload" href="/fonts/general-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/general-sans-600.woff2" as="font" type="font/woff2" crossorigin>
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
    a = icon('arrow'); ne = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
    eng_bg = ['', 't2', 'pale', 't3']
    engines = ''.join(f'<a class="tile engine {eng_bg[i]}" href="{u}" data-rise><b>{n}</b><span>{s}</span></a>' for i, (u, n, s, _, _) in enumerate(SERVICES))
    star_sep = star_svg('mq', dark=True)
    phrase = f'<span>AI for speed. People for judgement. {star_sep}</span>'
    caps = [('Social media management', 'Instagram, Facebook, LinkedIn and YouTube'), ('Performance marketing', 'Meta and Google Ads, set up and optimised weekly'),
            ('SEO and AEO', 'Rank on Google, get named by AI assistants'), ('Content strategy', 'A monthly calendar built on research'),
            ('Reels and short video', 'Hooks, subtitles, motion graphics, covers'), ('Product and brand shoots', 'Photo and video, on location'),
            ('Graphic design', 'Posts, carousels, ads, menus, print'), ('Brand identity', 'Logo, palette, templates, brand kit'),
            ('WhatsApp automation', 'Catalogue, FAQs, bookings, broadcasts'), ('Instagram DM automation', 'Instant replies to comments and messages'),
            ('Lead capture and CRM', 'Every enquiry logged and followed up'), ('Websites and landing pages', 'Fast, mobile-first, ready for search')]
    caps_html = ''.join(f'<div data-rise><b>{x}</b><span>{y}</span></div>' for x, y in caps)
    biz = [('cafe', 'Café or restaurant'), ('clinic', 'Clinic or wellness'), ('d2c', 'D2C or e-commerce brand'), ('realestate', 'Real estate'), ('education', 'Education'), ('creator', 'Creator or personal brand')]
    goals = [('leads', 'Leads'), ('sales', 'Sales'), ('bookings', 'Bookings'), ('awareness', 'Awareness')]
    chans = [('ch_ig', 'Instagram', True), ('ch_wa', 'WhatsApp', True), ('ch_meta', 'Meta ads', True), ('ch_google', 'Google ads', False), ('ch_web', 'Website', True)]
    seg = ''.join(f'<label><input type="radio" name="goal" value="{v}"' + (' checked' if v == 'leads' else '') + f'><span>{l}</span></label>' for v, l in goals)
    chips = ''.join(f'<label><input type="checkbox" name="{n}"' + (' checked' if c else '') + f'><span>{l}</span></label>' for n, l, c in chans)
    body = f'''
<section class="hero frame" data-sec aria-labelledby="hero-h">
  <div class="board">
    <div class="tile h-main" data-rise>
      <div><h1 id="hero-h">Your AI growth team</h1>
        <p class="lead">Nxtlvl Social is an AI-driven growth company in India. We run your marketing, automation and creative production on one monthly subscription, and people check every result.</p></div>
      <div class="btns"><a class="btn btn-primary" href="/contact">Book a free strategy call {a}</a><a class="btn btn-light" href="#planner">Build your month</a></div>
    </div>
    <div class="tile night h-live" data-rise>
      <div class="cap"><b>A table booked while the owner slept</b><span data-ist>11:42 pm IST</span></div>
      <div class="chat" data-ui role="img" aria-label="Example WhatsApp conversation: a customer asks for a table for four at 8 pm, the automation confirms the booking and logs the lead.">
        <div class="chat-top"><span class="av">CA</span><div><b>Café Aroma · example</b><small>Auto-replies on</small></div></div>
        <div class="chat-body">
          <div class="msg in" data-step>Hi! Are you open tonight? Table for 4 at 8?<small data-time>11:42 pm</small></div>
          <div class="msg out" data-step>Hi Priya, yes, we are open till 11. I can hold a table for 4 at 8:00 pm. Shall I book it?<small data-time>11:42 pm</small></div>
          <div class="msg in" data-step>Yes please<small data-time>11:43 pm</small></div>
          <div class="msg out" data-step>Booked: table for 4, tonight at 8:00 pm. See you soon!<small data-time>11:43 pm</small></div>
          <div class="note" data-step>Lead saved · owner notified on WhatsApp</div>
          <div class="typing" aria-hidden="true"><i></i><i></i><i></i></div>
        </div>
      </div>
    </div>
    <div class="h-row">{engines}</div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{phrase * 6}</div></div>

<section class="sec frame" id="build" data-sec aria-labelledby="plan-h">
  <div class="sec-head"><h2 id="plan-h" data-rise>Build your month</h2>
    <p class="soft" data-rise>Pick your business, goal and channels. This is the plan our team would start you on, and it changes as you do.</p></div>
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

<section class="sec frame" data-sec aria-labelledby="eng-h">
  <div class="sec-head"><h2 id="eng-h" data-rise>Four engines, one team</h2>
    <p class="soft" data-rise>Each engine runs on AI systems we built and tuned for Indian businesses. A strategist ties them together into one plan and one report.</p></div>
  <div class="cells">
    <a class="cell" href="/ai-marketing" data-rise><div class="txt"><b>AI Marketing</b><span>Social media, campaigns and ads, planned on research and optimised every week.</span></div>
      {FRAG["ads"]}</a>
    <a class="cell rev" href="/ai-automation" data-rise><div class="txt"><b>AI Automation</b><span>Replies, lead capture and follow-ups on WhatsApp and Instagram, around the clock.</span></div>
      {FRAG["flow"]}</a>
    <a class="cell" href="/creative-studio" data-rise><div class="txt"><b>Creative Studio</b><span>Shoots, reel and video editing, and design that look like your brand.</span></div>
      {FRAG["reel"]}</a>
    <a class="cell rev" href="/website-development" data-rise><div class="txt"><b>Websites</b><span>Fast landing pages and websites that rank and turn visitors into enquiries.</span></div>
      {FRAG["web"]}</a>
    <a class="cell" href="/ai-marketing#included" data-rise><div class="txt"><b>SEO and AEO</b><span>Be found on Google, and named when buyers ask ChatGPT, Gemini or Perplexity.</span></div>
      {FRAG["seo"]}</a>
    <a class="cell rev" href="/ai-marketing" data-rise><div class="txt"><b>One monthly report</b><span>What worked, what did not, and what we will change next month, in plain words.</span></div>
      {FRAG["report"]}</a>
  </div>
</section>

<section class="sec" data-sec aria-labelledby="how-h">
  <div class="fields">
    <div class="field" data-rise><h2 id="how-h">How it works</h2>
      <div class="req" data-ui><span class="t">Festive offer campaign</span><div class="m"><span class="pillx">New</span><span class="pillx">From: owner</span></div><ul><li class="todo">Brief</li><li class="todo">Drafts</li><li class="todo">Approval</li></ul></div>
      <div class="clause"><p>First it lands with us.</p><p>Send a goal, a photo or a voice note. We turn it into a brief.</p></div></div>
    <div class="field" data-rise><span></span>
      <div class="req" data-ui><span class="t">Festive offer campaign</span><div class="m"><span class="pillx">Strategist assigned</span><span class="pillx">Due Fri</span></div><ul><li class="done">Brief and research</li><li class="done">3 hook options</li><li class="todo">Edit and design</li></ul></div>
      <div class="clause"><p>Then AI drafts it.</p><p>Research, hooks, scripts and designs in hours instead of weeks.</p></div></div>
    <div class="field" data-rise><span></span>
      <div class="req" data-ui><span class="t">Festive offer campaign</span><div class="m"><span class="pillx v">In review</span></div><ul><li class="done">Brief and research</li><li class="done">Hook B chosen</li><li class="done">Reel and 4 creatives</li><li class="todo">Your approval</li></ul></div>
      <div class="clause"><p>Then people finish it.</p><p>Editors and designers polish it. Nothing ships without your yes.</p></div></div>
    <div class="field" data-rise><span></span>
      <div class="req" data-ui><span class="t">Festive offer campaign</span><div class="m"><span class="pillx ok">Live</span><span class="pillx">Ads running</span></div><div class="fig"><span>Enquiries, week 1</span><span>39</span></div></div>
      <div class="clause"><p>Then it goes live.</p><p>We publish, run the ads, switch on replies and report back.</p></div></div>
  </div>
</section>

<section class="sec frame" data-sec aria-labelledby="proof-h">
  <div class="sec-head"><h2 id="proof-h" data-rise>We grow our own page first</h2>
    <p class="soft" data-rise>Our Instagram, @ai.nxtlvl, is where every format, hook and automation is tested before it reaches a client.</p></div>
  <div class="proof">
    <div class="tile shot" data-rise><img src="/img/ai-nxtlvl-profile.jpg" width="1320" height="1245" alt="The @ai.nxtlvl Instagram profile by Nxtlvl Social: 31 posts, 9,924 followers and 1.0M views in the last 30 days" loading="lazy">
      <p class="over">Nearly 10,000 followers and 1M views in 30 days from 31 posts, built with the same mix of AI research, fast editing and human taste we bring to every client. <a href="https://www.instagram.com/ai.nxtlvl/" rel="noopener" target="_blank">See the page</a></p></div>
    <div class="facts">
      <div class="tile t2" data-rise><span>Where we work</span><b>Across India, remote-first, shoots on location</b></div>
      <div class="tile pale" data-rise><span>How plans work</span><b>Monthly scope, no lock-in, pause any month</b></div>
      <div class="tile" data-rise><span>What you own</span><b>Every file, account and system we set up</b></div>
    </div>
  </div>
</section>

<section class="sec frame" data-sec aria-labelledby="caps-h">
  <div class="sec-head"><h2 id="caps-h" data-rise>Everything a growth team does</h2>
    <p class="soft" data-rise>One partner from being discovered to being chosen.</p></div>
  <div class="caps">{caps_html}</div>
</section>
<section class="sec frame" data-sec aria-labelledby="plat-h">
  <div class="tile night" style="display:grid;gap:18px;padding:clamp(28px,4vw,56px)" data-rise>
    <h2 id="plat-h" style="max-width:18ch">Next: the Nxtlvl growth platform</h2>
    <p class="soft" style="max-width:60ch">We are building an AI workspace that turns a short brief into content ideas, scripts and ready-to-post reels, with our team one message away. Subscribers get early access.</p>
    <div class="btns"><a class="btn btn-white" href="/contact?need=platform">Ask about early access {a}</a></div>
  </div>
</section>

{faq_block(HOME_FAQ)}
{close_row()}
'''
    return page('/index', 'AI-Driven Marketing, Automation & Creative | Nxtlvl Social',
                'Nxtlvl Social is an AI-driven growth company in India. Marketing, WhatsApp and DM automation, shoots, edits, design and websites on one monthly plan.',
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
