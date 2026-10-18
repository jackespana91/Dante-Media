#!/usr/bin/env python3
"""Compile the editable Dante Media site into deployable, dependency-free HTML.
Run: python build.py
"""
from __future__ import annotations
from datetime import date
from pathlib import Path
from urllib.parse import urljoin
import html, json, os, re, shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape
from content import BRANDS, GROUP_EMAIL, NAV, PAGE_META, SITE_URL

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
TEMPLATES = ROOT / 'templates'
PAGES = {
    '/': ('home', 'home.html'),
    '/businesses/': ('businesses', 'businesses.html'),
    '/approach/': ('approach', 'approach.html'),
    '/gaming/': ('gaming', 'gaming.html'),
    '/media/': ('media', 'media.html'),
    '/sport/': ('sport', 'sport.html'),
    '/broken-homes/': ('broken-homes', 'broken-homes.html'),
    '/partnerships/': ('partnerships', 'partnerships.html'),
    '/work/': ('work', 'work.html'),
    '/about/': ('about', 'about.html'),
    '/news/': ('news', 'news.html'),
    '/contact/': ('contact', 'contact.html'),
}


def schema_for(path: str, title: str, description: str) -> dict:
    canonical = urljoin(SITE_URL + '/', path.lstrip('/'))
    graph = [
        {'@type': 'Organization', '@id': SITE_URL + '/#organization', 'name': 'Dante Media', 'url': SITE_URL + '/', 'description': 'An entrepreneurial group connecting ventures across gaming, technology, media, sport and entertainment.'},
        {'@type': 'WebSite', '@id': SITE_URL + '/#website', 'name': 'Dante Media', 'url': SITE_URL + '/', 'publisher': {'@id': SITE_URL + '/#organization'}},
        {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': title, 'description': description, 'isPartOf': {'@id': SITE_URL + '/#website'}},
    ]
    if path != '/':
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem','position': 1, 'name':'Home', 'item': SITE_URL + '/'},
            {'@type': 'ListItem','position': 2, 'name': title.split('|')[0].strip(), 'item':canonical},
        ]})
    return {'@context': 'https://schema.org', '@graph': graph}


def main() -> None:
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(ROOT / 'assets', DIST / 'assets')
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=select_autoescape(['html','xml']))
    staging = os.environ.get('DANTE_STAGING', '').lower() in {'1', 'true', 'yes'}
    base_path = os.environ.get('DANTE_BASE_PATH', '').rstrip('/')
    if base_path and (not base_path.startswith('/') or '//' in base_path):
        raise ValueError('DANTE_BASE_PATH must be empty or a site subpath beginning with /')
    featured_names = {'PlayBeSpoke','IGW³','Futpal','Broken Homes','Lucky Bastards','The Plug TV'}
    for path,(page_key, template) in PAGES.items():
        title, desc = PAGE_META[path]
        canonical = urljoin(SITE_URL + '/', path.lstrip('/'))
        context = {
            'title': title, 'description': desc, 'site_url':SITE_URL,
            'canonical_url':canonical, 'path':path, 'page_key':page_key,
            'nav':NAV, 'brands':BRANDS,
            'featured':[b for b in BRANDS if b['name'] in featured_names],
            'gaming_brands':[b for b in BRANDS if b['category']=='gaming'],
            'media_brands':[b for b in BRANDS if b['category']=='media'],
            'group_email':GROUP_EMAIL, 'year':date.today().year, 'is_staging':staging,
            'schema_json':json.dumps(schema_for(path,title,desc),ensure_ascii=False).replace('<','\\u003c'),
        }
        out = DIST / path.lstrip('/') / 'index.html' if path != '/' else DIST / 'index.html'
        out.parent.mkdir(parents=True,exist_ok=True)
        markup = env.get_template(template).render(**context)
        if base_path:
            markup = re.sub(r'((?:href|src)=["\'])/(?!/)', lambda m: m.group(1)+base_path+'/', markup)
        out.write_text(markup, encoding='utf-8')
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in PAGES:
        sitemap.append('  <url><loc>'+html.escape(urljoin(SITE_URL+'/',path.lstrip('/')) )+'</loc></url>')
    sitemap.append('</urlset>')
    (DIST/'sitemap.xml').write_text('\n'.join(sitemap)+'\n',encoding='utf-8')
    robots = 'User-agent: *\nDisallow: /\n' if staging else 'User-agent: *\nAllow: /\nSitemap: '+SITE_URL+'/sitemap.xml\n'
    (DIST/'robots.txt').write_text(robots, encoding='utf-8')
    print(f'Built {len(PAGES)} pages to {DIST}')

if __name__ == '__main__': main()
