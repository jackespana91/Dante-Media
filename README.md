# Dante Media — group website rebuild (staging package)

This is a responsive, editable, multi-page **static-site implementation** of the new Dante Media parent-group positioning. Broken Homes is central to the site, clearly labelled as a foundation planned for launch.

**Not deployed to dante-media.io.** Access to that live site's editor/repository could not be verified in this session, and the current site's code/framework was not available. This is a working replacement/reference implementation for Codex to port, review, and stage.

## Preview locally

```bash
python -m pip install -r requirements.txt
python build.py
cd dist && python -m http.server 8080
```
Open `http://localhost:8080/`. Static generated HTML in `dist` needs no server dependencies and can be hosted by any static host when configured for directory index routes.

## What's included
- 12 interconnected pages and responsive nav/footer.
- Filterable 12-entry business directory with editorial status and accurately cautious relationship language.
- Dedicated, extensive Broken Homes section and the foundation as a group-wide commitment on every page.
- SEO metadata, canonicals, Open Graph/Twitter metadata, JSON-LD Organization/WebPage/Breadcrumbs, sitemap, robots.
- Keyboard-accessible nav, reduced-motion support, responsive layouts, no marketing trackers or unrelated brand cookies.
- `docs/CODEX_IMPLEMENTATION_BRIEF.md` for integration into the **real** site, plus `docs/BROKEN_HOMES_OPERATING_STANDARD.md`.

## Build a review preview without touching the domain

GitHub Actions includes a **manual**, crawler-excluded Pages preview. It requires setting this repository's **Settings > Pages > Build and deployment > GitHub Actions** once; then run **Actions > Publish manual staging preview (not live domain)**. No production domain or DNS changes are made. See [Hosting and publishing](docs/HOSTING_AND_PUBLISHING.md).

You can also create a local project-path preview with:

```bash
DANTE_STAGING=1 DANTE_BASE_PATH=/Dante-Media python build.py
```

## The necessary human approvals
1. Validate brand legal ownership, names, exact relationships, launch/operating statuses and domains. The directory uses cautious public language; it should still be approved by the group.
2. Verify Broken Homes' legal status and review language with charity/safeguarding counsel.
3. The group contact route is configured as `info@dante-media.io` in `content.py` based on the group's existing address. **Test delivery, mailbox access and response ownership before launch.** PlayBeSpoke enquiries still route to its own email.
4. Set up a real contact management route; do not deploy pretend email forms or collect beneficiary information.
5. Approve privacy/cookie/consent/legal disclosures before public launch. These are **not** fabricated in this package.
6. Port into the existing website and compare/retain its valuable current film, original assets, advisory content and established SEO URLs.
7. Test staged pages including mobile navigation, performance, structured data, redirects and accessibility; publish only after approval.

© 2026 Dante Media. Website source delivered for the site's authorised owner.
