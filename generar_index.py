#!/usr/bin/env python3
import re
from pathlib import Path
from html import escape
from datetime import datetime

POSTS_DIR = Path("posts")
BASE_URL = "https://aletec1313.github.io/luigi-blog"

def detect_author(folder):
    if folder.startswith('mario-') or '-mario-' in folder:
        return 'mario'
    return 'luigi'

def get_all_posts():
    posts = []
    for post_dir in POSTS_DIR.iterdir():
        if not post_dir.is_dir():
            continue
        index_file = post_dir / "index.html"
        if not index_file.exists():
            continue
        folder = post_dir.name
        content = index_file.read_text(encoding='utf-8')
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        else:
            title = folder.replace('-', ' ').title()
        p_match = re.search(r'<p>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        if p_match:
            excerpt = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            if len(excerpt) > 180:
                excerpt = excerpt[:177] + '...'
        else:
            excerpt = '¡Mamma mia!'
        date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', folder)
        if date_match:
            y, m, d = date_match.groups()
            date_sort = f"{y}-{m}-{d}"
            months = {'01':'Ene','02':'Feb','03':'Mar','04':'Abr','05':'May','06':'Jun',
                      '07':'Jul','08':'Ago','09':'Sep','10':'Oct','11':'Nov','12':'Dic'}
            date_display = f"{d} {months.get(m,'???')} {y}"
        else:
            date_sort = "2026-01-01"
            date_display = "Ene 2026"
        author = detect_author(folder)
        author_badges = {'mario': '🔴 Mario', 'luigi': '🍄 Luigi'}
        posts.append({
            'folder': folder,
            'title': escape(title),
            'excerpt': escape(excerpt),
            'date_sort': date_sort,
            'date_display': date_display,
            'author': author,
            'author_badge': author_badges[author],
            'url': f"{BASE_URL}/posts/{folder}/",
        })
    posts.sort(key=lambda x: x['date_sort'], reverse=True)
    return posts

def generate_html(posts):
    articles = []
    for p in posts:
        articles.append(f'''<article class="post-card {p['author']}"><div class="post-card-inner"><div class="post-meta"><span class="post-date">{p['date_display']}</span><span class="author-badge author-{p['author']}">{p['author_badge']}</span></div><h2><a href="posts/{p['folder']}/">{p['title']}</a></h2><div class="post-excerpt"><p>{p['excerpt']}</p></div><a href="posts/{p['folder']}/" class="read-more">Leer más →</a></div></article>''')
    articles_html = '\n'.join(articles)
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mario, Luigi & Alex</title>
<link rel="stylesheet" href="css/style.css">
<link rel="alternate" type="application/rss+xml" href="rss.xml">
</head>
<body>
<header><div class="header-inner"><a href="/" class="site-title">MARIO, LUIGI & ALEX</a><nav><a href="index.html">Inicio</a><a href="sobre-nosotros.html">Sobre Nosotros</a><a href="#suscribirse">Suscribirse</a></nav></div></header>
<main class="container"><div class="posts-section"><div class="section-title">TODOS LOS POSTS ({len(posts)})</div>{articles_html}</div></main>
<footer><p>© 2026 Mario, Luigi & Alex</p></footer>
</body></html>'''

def main():
    posts = get_all_posts()
    Path("index.html").write_text(generate_html(posts), encoding='utf-8')
    mario_count = sum(1 for p in posts if p['author'] == 'mario')
    print(f"Generados {len(posts)} posts ({mario_count} Mario, {len(posts)-mario_count} Luigi)")

if __name__ == "__main__":
    main()
