from pathlib import Path
p=Path(__file__).resolve().parents[2] / 'context/scripts/build_wilmington_site.py'
s=p.read_text()
start=s.index('service_details = {')
end=s.index("sitemap_urls =", start)
new = r'''service_details = {
    'free-websites-wilmington-nc': {
        'focus': 'The free website is the foundation, not the finish line.',
        'bullets': ['No upfront design bill for qualified service businesses', 'A clean, mobile-first website that makes the business easier to trust', 'Core service pages, local structure, FAQs, schema, and conversion paths built in from the start'],
        'value': 'A website by itself does not magically bring leads. It gives the marketing somewhere credible to send people, gives Google and AI systems clearer information to understand, and gives buyers a reason to call instead of bouncing. The real growth comes from improving that foundation every month with local SEO, Google Business Profile work, content expansion, citation cleanup, AI-search readiness, and paid traffic when it makes sense.',
        'process': ['Map the offer, service area, and best-fit customer before design starts', 'Build the site around trust, calls, texts, and AI-readable clarity', 'Launch with a structure that can support SEO, GBP, ads, and future service pages', 'Use the six-month growth partnership to keep expanding visibility instead of stopping at launch'],
        'outcome': 'The business gets a stronger online base layer first, then monthly marketing turns that base into a growing visibility system.'
    },
    'web-design-wilmington-nc': {
        'focus': 'The website should make the business easier to trust before someone calls.',
        'bullets': ['Mobile-first layouts for fast Wilmington-area comparison', 'Service pages written around buyer questions, objections, and local proof', 'Clear calls, texts, quote paths, and trust signals on every important page'],
        'value': 'Most service-business websites fail because they look fine at a glance but do not explain enough, answer enough, or guide the buyer clearly. We design around the moment someone is deciding whether the business feels credible, local, current, and easy to contact.',
        'process': ['Clarify the offer and the primary services people search for', 'Structure pages around real buyer decisions, not filler sections', 'Make the mobile experience quick, readable, and CTA-forward', 'Add schema, FAQs, and internal links so the site can support search and AI visibility'],
        'outcome': 'A sharper site that supports calls, local SEO, Google Business Profile traffic, paid ads, and AI-search understanding.'
    },
    'seo-ai-ranking-wilmington-nc': {
        'focus': 'Local SEO now has to support maps, organic search, and AI-shaped answers.',
        'bullets': ['Google Business Profile alignment and local entity clarity', 'FAQ and service content written for human decisions and answer engines', 'Citation cleanup, location relevance, and conservative schema'],
        'value': 'AI search does not replace local SEO. It raises the bar for clarity. Search engines and answer systems need to understand what the business does, where it works, who it helps, and why it is trustworthy. That means the website, GBP, citations, FAQs, and service content need to reinforce each other.',
        'process': ['Strengthen the local website structure and service-area signals', 'Tune Google Business Profile categories, services, posts, and conversion paths', 'Build useful FAQ and service content that answers real buying questions', 'Keep citations and business details consistent so the entity is easier to trust'],
        'outcome': 'Better local clarity across Google, maps, organic results, and AI-influenced discovery.'
    },
    'google-ads-wilmington-nc': {
        'focus': 'Paid traffic works better when the landing page already earns trust.',
        'bullets': ['Search campaigns pointed at focused service intent', 'Landing pages that match the offer, city, and buyer urgency', 'Call/text conversion paths and practical lead-quality feedback loops'],
        'value': 'Google Ads can create traffic quickly, but traffic is expensive when the page does not convert. We pair ads with clearer landing pages, stronger local proof, and better offer alignment so clicks have a better chance of becoming calls or quote requests.',
        'process': ['Choose the service searches most likely to produce real leads', 'Send visitors to pages that match the exact intent of the search', 'Track calls, texts, form starts, and lead quality signals', 'Use results to adjust the page, offer, and campaign instead of only changing bids'],
        'outcome': 'A paid-search setup that is connected to the website, local visibility, and real conversion path instead of isolated ad spend.'
    },
}
for name, slug, desc in services:
    d = service_details[slug]
    bullet_html = ''.join(f'<li>{b}</li>' for b in d['bullets'])
    process_html = ''.join(f'<article class="card"><span class="eyebrow">Step {i}</span><h3>{step}</h3></article>' for i, step in enumerate(d['process'], 1))
    p = f"""<section class="hero"><div class="wrap"><p class="eyebrow">{name} in Wilmington</p><h1>{name} for Wilmington businesses that need to be found, trusted, and understood by AI search.</h1><p class="lead">{desc} {BRAND} keeps the work practical: stronger pages, clearer offers, local proof, structured FAQs, Google Business Profile alignment, and conversion paths that make the next step obvious.</p><div class="actions"><a class="btn" href="/contact.html">Ask about this service</a><a class="btn ghost" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div></div></section><section class="section"><div class="two"><article class="card"><p class="eyebrow">Service focus</p><h2>{d['focus']}</h2><ul>{bullet_html}</ul></article><article class="card"><p class="eyebrow">Why it matters</p><h2>What this actually does for the business</h2><p>{d['value']}</p></article></div></section><section class="section dark"><div><p class="eyebrow">How we approach it</p><h2>Built as part of a connected growth system, not a one-off tactic.</h2><div class="cards">{process_html}</div></div></section><section class="section"><div class="two"><article class="card"><p class="eyebrow">Expected outcome</p><h2>{d['outcome']}</h2><p>The goal is not to make the business sound bigger than it is. The goal is to make it easier to find, easier to understand, easier to trust, and easier to contact.</p></article><article class="card"><p class="eyebrow">Next step</p><h2>Start with the foundation, then keep improving it.</h2><p>We look at the website, local search presence, Google Business Profile, service pages, and lead path together so each month of work compounds instead of feeling random.</p><a class="btn" href="/contact.html">Talk through the growth plan</a></article></div></section>"""
    ROOT.joinpath('services', f'{slug}.html').write_text(layout(f'{name} in Wilmington, NC | {BRAND}', f'{desc} Wilmington, NC support from {BRAND}.', p, service_link(slug)))

'''
s=s[:start]+new+s[end:]
p.write_text(s)
print('expanded service page template')
