#!/usr/bin/env python3
"""Compile the editable Dante Media site into deployable, dependency-free HTML.
Run: python build.py
"""
from __future__ import annotations
from datetime import date
from pathlib import Path
from urllib.parse import urljoin
import html, json, os, re, shutil
import tempfile
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
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


def normalize_base_path(base_path: str) -> str:
    """Accept a root or simple URL path, without URL queries or dot segments."""
    if base_path in {'', '/'}:
        return ''
    normalized = base_path.rstrip('/')
    if (not re.fullmatch(r'/[A-Za-z0-9._~/-]+', base_path)
            or '//' in base_path
            or any(part in {'.', '..'} for part in normalized.split('/'))):
        raise ValueError('DANTE_BASE_PATH must be empty or a URL subpath such as /Dante-Media')
    return normalized


def build_site(output_dir: Path = DIST, *, staging: bool = False, base_path: str = '') -> None:
    """Render a complete release before replacing the previous generated site."""
    base_path = normalize_base_path(base_path)
    output_dir = Path(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)),
                      autoescape=select_autoescape(['html', 'xml']),
                      undefined=StrictUndefined)
    # A bad setting or template must not erase a working preview/release.
    with tempfile.TemporaryDirectory(prefix='.dante-build-', dir=output_dir.parent) as temporary:
        release = Path(temporary) / 'site'
        release.mkdir()
        shutil.copytree(ROOT / 'assets', release / 'assets')
        render_pages(env, release, staging=staging, base_path=base_path)
        if output_dir.exists():
            shutil.rmtree(output_dir)
        release.replace(output_dir)


def render_pages(env: Environment, release: Path, *, staging: bool, base_path: str) -> None:
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
        out = release / path.lstrip('/') / 'index.html' if path != '/' else release / 'index.html'
        out.parent.mkdir(parents=True,exist_ok=True)
        markup = env.get_template(template).render(**context)
        if base_path:
            markup = re.sub(r'((?:href|src)=["\'])/(?!/)', lambda m: m.group(1)+base_path+'/', markup)
        out.write_text(markup, encoding='utf-8')
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in PAGES:
        sitemap.append('  <url><loc>'+html.escape(urljoin(SITE_URL+'/',path.lstrip('/')) )+'</loc></url>')
    sitemap.append('</urlset>')
    (release/'sitemap.xml').write_text('\n'.join(sitemap)+'\n',encoding='utf-8')
    robots = 'User-agent: *\nDisallow: /\n' if staging else 'User-agent: *\nAllow: /\nSitemap: '+SITE_URL+'/sitemap.xml\n'
    (release/'robots.txt').write_text(robots, encoding='utf-8')


def main() -> None:
    staging = os.environ.get('DANTE_STAGING', '').strip().lower() in {'1', 'true', 'yes'}
    build_site(DIST, staging=staging, base_path=os.environ.get('DANTE_BASE_PATH', ''))
    print(f'Built {len(PAGES)} pages to {DIST}')

if __name__ == '__main__': main()
