"""Build isolated production/staging releases and validate their public output."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree
import json
import os
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

from jinja2 import UndefinedError

import build
from build import PAGES, build_site, normalize_base_path
from content import PAGE_META, SITE_URL


PREVIEW_ORIGIN = 'https://preview.invalid'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.meta = {}
        self.canonicals = []
        self.h1s = 0
        self.schemas = []
        self._schema = None

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if 'id' in props:
            self.ids.append(props['id'])
        for key in ('href', 'src'):
            if props.get(key):
                self.links.append(props[key])
        if tag == 'meta':
            self.meta[props.get('name') or props.get('property')] = props.get('content')
        if tag == 'link' and props.get('rel') == 'canonical':
            self.canonicals.append(props.get('href'))
        if tag == 'h1':
            self.h1s += 1
        if tag == 'script' and props.get('type') == 'application/ld+json':
            self._schema = []

    def handle_data(self, data):
        if self._schema is not None:
            self._schema.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self._schema is not None:
            self.schemas.append(json.loads(''.join(self._schema)))
            self._schema = None


def parse_page(path):
    page = Page()
    page.feed(path.read_text(encoding='utf-8'))
    return page


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.project = Path(cls.temporary.name)
        cls.production = cls.project / 'production'
        cls.staging = cls.project / 'staging'
        build_site(cls.production)
        build_site(cls.staging, staging=True, base_path='/Dante-Media/')

    def resolve_local(self, output, source, link, base_path=''):
        """Resolve like a browser, including project-hosted CSS relative URLs."""
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc:
            return None
        source_url = PREVIEW_ORIGIN + base_path + '/' + source.relative_to(output).as_posix()
        target = urlsplit(urljoin(source_url, link))
        if base_path:
            self.assertTrue(target.path.startswith(base_path + '/'),
                            f'{link} escapes staging path in {source.name}')
            path = target.path[len(base_path):]
        else:
            path = target.path
        resolved = (output / unquote(path).lstrip('/')).resolve()
        self.assertTrue(resolved.is_relative_to(output.resolve()), f'{link} escapes output')
        if resolved.is_dir() or not resolved.suffix:
            resolved /= 'index.html'
        self.assertTrue(resolved.is_file(), f'{link} not found from {source.relative_to(output)}')
        if target.fragment and resolved.suffix == '.html':
            self.assertIn(unquote(target.fragment), parse_page(resolved).ids,
                          f'Missing fragment {link} from {source.relative_to(output)}')
        return resolved

    def test_expected_routes_and_metadata(self):
        self.assertEqual(set(PAGES), set(PAGE_META))
        for output in (self.production, self.staging):
            self.assertEqual(len(list(output.rglob('*.html'))), len(PAGES))
            for route in PAGES:
                path = output / route.lstrip('/') / 'index.html'
                with self.subTest(output=output.name, route=route):
                    self.assertTrue(path.is_file(), f'Missing {path}')
                    markup = path.read_text(encoding='utf-8')
                    page = parse_page(path)
                    title, description = PAGE_META[route]
                    canonical = urljoin(SITE_URL + '/', route.lstrip('/'))
                    self.assertIn('<title>' + title.replace('&', '&amp;') + '</title>', markup)
                    self.assertEqual(page.meta['description'], description)
                    self.assertEqual(page.canonicals, [canonical])
                    self.assertEqual(page.meta['og:url'], canonical)
                    self.assertEqual(page.meta['og:title'], title)
                    self.assertEqual(page.meta['og:description'], description)
                    image = urlsplit(page.meta['og:image'])
                    self.assertEqual(image.netloc, urlsplit(SITE_URL).netloc)
                    self.assertTrue((output / image.path.lstrip('/')).is_file())
                    self.assertEqual(page.h1s, 1)
                    self.assertEqual(len(page.ids), len(set(page.ids)), 'Duplicate HTML IDs')
                    self.assertEqual(len(page.schemas), 1)
                    graph = page.schemas[0]['@graph']
                    webpages = [item for item in graph if item['@type'] == 'WebPage']
                    self.assertEqual(len(webpages), 1)
                    self.assertEqual(webpages[0]['url'], canonical)
                    self.assertEqual(webpages[0]['name'], title)
                    self.assertEqual(webpages[0]['description'], description)

    def test_links_and_fragments_resolve_in_both_builds(self):
        for output, base_path in ((self.production, ''), (self.staging, '/Dante-Media')):
            for source in output.rglob('*.html'):
                for link in parse_page(source).links:
                    with self.subTest(output=output.name, source=source.relative_to(output), link=link):
                        self.resolve_local(output, source, link, base_path)

    def test_css_assets_resolve_in_both_builds(self):
        for output, base_path in ((self.production, ''), (self.staging, '/Dante-Media')):
            for source in output.rglob('*.css'):
                for match in re.finditer(r'url\(\s*([\'"]?)(.*?)\1\s*\)', source.read_text(encoding='utf-8')):
                    link = match.group(2).strip()
                    if not link or link.startswith('#'):
                        continue
                    with self.subTest(output=output.name, source=source.relative_to(output), link=link):
                        self.resolve_local(output, source, link, base_path)

    def test_broken_homes_is_central_but_not_misrepresented(self):
        home = (self.production / 'index.html').read_text(encoding='utf-8').lower()
        foundation = (self.production / 'broken-homes/index.html').read_text(encoding='utf-8').lower()
        self.assertIn('broken homes', home)
        self.assertIn('planned', foundation)
        self.assertIn('not yet delivering services', foundation)
        self.assertIn('beneficiary intake is not open', foundation)
        self.assertIn('safeguard', foundation)

    def test_contact_route_does_not_imply_support_service(self):
        contact = (self.production / 'contact/index.html').read_text(encoding='utf-8').lower()
        self.assertIn('mailto:info@dante-media.io', contact)
        self.assertIn('business and partnership contact', contact)
        self.assertIn('support services and beneficiary referrals are not open', contact)

    def test_staging_excludes_search_indexing(self):
        for page in self.staging.rglob('*.html'):
            self.assertEqual(parse_page(page).meta.get('robots'), 'noindex,nofollow')
        for page in self.production.rglob('*.html'):
            self.assertNotIn('noindex', parse_page(page).meta.get('robots', ''))
        home = (self.staging / 'index.html').read_text(encoding='utf-8')
        self.assertIn('href="/Dante-Media/businesses/"', home)
        self.assertIn('src="/Dante-Media/assets/site.js"', home)
        self.assertEqual((self.staging / 'robots.txt').read_text(encoding='utf-8'),
                         'User-agent: *\nDisallow: /\n')

    def test_environment_selects_staging_and_project_path(self):
        output = self.project / 'environment-build'
        with patch.object(build, 'DIST', output), patch.dict(
                os.environ, {'DANTE_STAGING': ' true ', 'DANTE_BASE_PATH': '/Dante-Media/'}):
            build.main()
        home = parse_page(output / 'index.html')
        self.assertEqual(home.meta['robots'], 'noindex,nofollow')
        self.assertIn('/Dante-Media/assets/site.js', home.links)
        self.assertIn('/Dante-Media/businesses/', home.links)

    def test_sitemap_and_production_robots(self):
        namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        expected = {urljoin(SITE_URL + '/', route.lstrip('/')) for route in PAGES}
        for output in (self.production, self.staging):
            tree = ElementTree.parse(output / 'sitemap.xml')
            urls = [element.text for element in tree.findall('s:url/s:loc', namespace)]
            self.assertEqual(set(urls), expected)
            self.assertEqual(len(urls), len(expected))
        self.assertEqual((self.production / 'robots.txt').read_text(encoding='utf-8'),
                         f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')

    def test_base_path_validation_preserves_previous_release(self):
        for valid, expected in (('', ''), ('/', ''), ('/Dante-Media/', '/Dante-Media'),
                                ('/preview/Dante-Media', '/preview/Dante-Media')):
            self.assertEqual(normalize_base_path(valid), expected)
        for invalid in ('relative', '//elsewhere', '/a//b', '/a/../b', '/./b',
                        '/preview?secret=1', '/preview#fragment', '/a\\b', '/a b'):
            with self.subTest(base_path=invalid):
                with self.assertRaises(ValueError):
                    build_site(self.production, base_path=invalid)
                self.assertTrue((self.production / 'index.html').is_file())

    def test_template_errors_preserve_previous_release(self):
        templates = self.project / 'broken-templates'
        shutil.copytree(build.TEMPLATES, templates)
        with (templates / 'base.html').open('a', encoding='utf-8') as template:
            template.write('\n{{ missing_required_content }}\n')
        previous_home = (self.production / 'index.html').read_bytes()
        with patch.object(build, 'TEMPLATES', templates):
            with self.assertRaises(UndefinedError):
                build_site(self.production)
        self.assertEqual((self.production / 'index.html').read_bytes(), previous_home)
        self.assertFalse(list(self.project.glob('.dante-build-*')))


if __name__ == '__main__':
    unittest.main()
