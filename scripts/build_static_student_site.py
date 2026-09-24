from pathlib import Path
import re, subprocess, html, json, shutil
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[1]
site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)

chapters = [
    'index.qmd',
    '01-inquiry.qmd',
    '02-system-understanding.qmd',
    '03-measurement.qmd',
    '04-variability-uncertainty.qmd',
    '05-sampling-replication.qmd',
    '06-space.qmd',
    '07-time.qmd',
    '08-mobile-organisms.qmd',
    '09-experiments.qmd',
    'references.qmd',
]

def get_title(path):
    text = path.read_text(encoding='utf-8')
    m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', text, re.M)
    return m.group(1).strip() if m else path.stem

entries = []
for fn in chapters:
    p = root / fn
    outname = 'index.html' if fn == 'index.qmd' else p.with_suffix('.html').name
    entries.append((fn, outname, get_title(p)))

nav_items = []
for fn, outname, title in entries:
    short = title
    nav_items.append((outname, short))

# Copy assets used by rendered site
shutil.copytree(root / 'figures', site / 'figures')
if (root / 'media').exists():
    shutil.copytree(root / 'media', site / 'media')
shutil.copy2(root / 'styles.css', site / 'styles.css')

# Extract glossary JS body from file; retain complete script tag as-is.
glossary_js = (root / 'glossary.js').read_text(encoding='utf-8')

book_title = 'ENV2301: Methods & Techniques for Environmental Studies'
book_subtitle = 'Classroom draft · 24 September 2026'

for idx, (fn, outname, title) in enumerate(entries):
    src = root / fn
    # Render only the document body. MathML avoids external JS requirements.
    cmd = [
        'pandoc', str(src),
        '--from=markdown+raw_html+fenced_divs+bracketed_spans+superscript',
        '--to=html5', '--mathml',
    ]
    body = subprocess.check_output(cmd, cwd=root, text=True)
    # Convert source links for the static site.
    body = re.sub(r'href="([^"]+)\.qmd(#[^"]*)?"', lambda m: f'href="{Path(m.group(1)).with_suffix(".html").name if Path(m.group(1)).name != "index.qmd" else "index.html"}{m.group(2) or ""}"', body)
    # index.qmd can appear explicitly.
    body = body.replace('href="index.html"', 'href="index.html"')

    soup = BeautifulSoup(body, 'html.parser')
    # Quarto's fig-alt attribute is not interpreted by raw Pandoc; transfer it to alt.
    for img in soup.find_all('img'):
        if img.has_attr('fig-alt'):
            img['alt'] = img['fig-alt']
            del img['fig-alt']
        if img.has_attr('data-fig-alt'):
            img['alt'] = img['data-fig-alt']
            del img['data-fig-alt']
    # Build a compact on-page TOC from h2/h3 headings.
    toc_items = []
    for h in soup.find_all(['h2','h3']):
        hid = h.get('id')
        if not hid:
            # Pandoc normally supplies ids, but keep a fallback.
            hid = re.sub(r'[^a-z0-9]+','-', h.get_text(' ', strip=True).lower()).strip('-')
            h['id'] = hid
        toc_items.append((h.name, hid, h.get_text(' ', strip=True)))
    toc_html = ''
    if toc_items:
        lis = []
        for tag, hid, txt in toc_items:
            cls = ' class="toc-sub"' if tag == 'h3' else ''
            lis.append(f'<li{cls}><a href="#{html.escape(hid)}">{html.escape(txt)}</a></li>')
        toc_html = '<details class="page-toc"><summary>On this page</summary><ul>' + ''.join(lis) + '</ul></details>'

    nav_html = ['<ul class="book-nav">']
    for link, label in nav_items:
        active = ' class="active" aria-current="page"' if link == outname else ''
        nav_html.append(f'<li><a{active} href="{html.escape(link)}">{html.escape(label)}</a></li>')
    nav_html.append('</ul>')
    nav_html = ''.join(nav_html)

    prev_html = ''
    next_html = ''
    if idx > 0:
        plink, ptitle = entries[idx-1][1], entries[idx-1][2]
        prev_html = f'<a class="prev" href="{html.escape(plink)}">← {html.escape(ptitle)}</a>'
    if idx + 1 < len(entries):
        nlink, ntitle = entries[idx+1][1], entries[idx+1][2]
        next_html = f'<a class="next" href="{html.escape(nlink)}">{html.escape(ntitle)} →</a>'

    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · ENV2301</title>
<link rel="stylesheet" href="styles.css">
</head>
<body class="student-book">
<div class="book-shell">
<aside class="book-sidebar" aria-label="Book navigation">
<div class="book-title">{html.escape(book_title)}</div>
<div class="book-subtitle">{html.escape(book_subtitle)}</div>
{nav_html}
</aside>
<main class="book-main">
<div class="book-topbar"><span>{html.escape(title)}</span><span class="draft-label">ENV2301 classroom draft</span></div>
<article class="content student-content">
<h1>{html.escape(title)}</h1>
{toc_html}
{str(soup)}
</article>
<nav class="page-nav" aria-label="Previous and next chapters">{prev_html}{next_html}</nav>
</main>
</div>
{glossary_js}
</body>
</html>'''
    (site / outname).write_text(page, encoding='utf-8')

# Search index for possible later use / QA.
index_records=[]
for fn, outname, title in entries:
    doc = BeautifulSoup((site/outname).read_text(encoding='utf-8'), 'html.parser')
    art = doc.select_one('article.student-content')
    text = art.get_text(' ', strip=True) if art else ''
    index_records.append({'url': outname, 'title': title, 'text': text})
(site/'search-index.json').write_text(json.dumps(index_records, ensure_ascii=False), encoding='utf-8')
