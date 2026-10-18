"""Tests for generated static pages, navigation, and public claims."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import unittest
import os, shutil, subprocess, sys, tempfile

from build import DIST, PAGES


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        for key in ('href', 'src'):
            if key in props:
                self.links.append(props[key])


class SiteTests(unittest.TestCase):
    def test_all_pages_exist(self):
        self.assertEqual(len(PAGES), 12)
        for route in PAGES:
            path = DIST / ('index.html' if route == '/' else route.strip('/') + '/index.html')
            with self.subTest(route=route):
                self.assertTrue(path.is_file(), f'Missing {path}')
                self.assertIn('<title>', path.read_text(encoding='utf-8'))

    def test_internal_links_resolve(self):
        for page in DIST.rglob('*.html'):
            parser = Links()
            parser.feed(page.read_text(encoding='utf-8'))
            for link in parser.links:
                if not link or link.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
                    continue
                parts = urlsplit(link)
                if parts.netloc or parts.scheme:
                    continue
                if parts.path.startswith('/'):
                    relative = unquote(parts.path).lstrip('/')
                    resolved = DIST / relative
                else:
                    resolved = page.parent / unquote(parts.path)
                if not resolved.suffix:
                    resolved = resolved / 'index.html'
                with self.subTest(page=page.relative_to(DIST), link=link):
                    self.assertTrue(resolved.is_file(), f'{link} not found from {page}')

    def test_broken_homes_is_central_but_not_misrepresented(self):
        home = (DIST / 'index.html').read_text(encoding='utf-8').lower()
        foundation = (DIST / 'broken-homes/index.html').read_text(encoding='utf-8').lower()
        self.assertIn('broken homes', home)
        self.assertIn('planned', foundation)
        self.assertIn('not yet an active support service', foundation)
        self.assertIn('safeguard', foundation)

    def test_contact_route_does_not_imply_support_service(self):
        contact = (DIST / 'contact/index.html').read_text(encoding='utf-8').lower()
        self.assertIn('mailto:info@dante-media.io', contact)
        self.assertIn('not an emergency or crisis service', contact)

    def test_noindex_preview_build_uses_project_path(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            shutil.copytree(root / 'assets', project / 'assets')
            shutil.copytree(root / 'templates', project / 'templates')
            for filename in ('build.py', 'content.py'):
                shutil.copy2(root / filename, project / filename)
            env = os.environ.copy()
            env.update(DANTE_STAGING='1', DANTE_BASE_PATH='/Dante-Media')
            subprocess.run([sys.executable, 'build.py'], cwd=project, env=env,
                           check=True, capture_output=True, text=True)
            home = (project / 'dist/index.html').read_text(encoding='utf-8')
            robots = (project / 'dist/robots.txt').read_text(encoding='utf-8')
            self.assertIn('content="noindex,nofollow"', home)
            self.assertIn('href="/Dante-Media/businesses/"', home)
            self.assertIn('src="/Dante-Media/assets/site.js"', home)
            self.assertIn('Disallow: /', robots)

    def test_sitemap_and_robots(self):
        sitemap = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
        self.assertEqual(sitemap.count('<loc>'), len(PAGES))
        self.assertIn('Sitemap:', (DIST / 'robots.txt').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
