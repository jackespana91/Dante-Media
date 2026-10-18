# Dante Media

The editable Dante Media website: twelve connected pages covering the group, its ventures, approach, partnerships and the planned Broken Homes foundation. The site builds to dependency-free HTML, CSS, JavaScript, fonts and images for static hosting.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py
.venv/bin/python -m http.server 8765 --directory dist
```

Open `http://127.0.0.1:8765/`.

## Source

- `content.py` — venture profiles, statuses, contacts, navigation and page metadata.
- `templates/` — page content and shared components.
- `assets/` — responsive styles, interactions, compressed artwork and self-hosted fonts. Font licences are included under `assets/fonts/`.
- `build.py` — production compiler. Generated output goes to `dist/`.
- `tests/test_site.py` — isolated production and staging regression checks.

## Verify

```sh
.venv/bin/python -m unittest discover -s tests -v
```

See [the completion checkpoint](docs/VERIFICATION.md) for the build results and browser review. CI runs the build and tests for pull requests and saves a static review artifact.

## Preview on a project path

```sh
DANTE_STAGING=1 DANTE_BASE_PATH=/Dante-Media .venv/bin/python build.py
```

Staging includes `noindex,nofollow` and crawler exclusion. The optional `staging-pages.yml` workflow publishes a GitHub Pages preview only when manually triggered. See [Hosting and publishing](docs/HOSTING_AND_PUBLISHING.md).

## Content and publication

Changes remain in the review branch until publication is authorised. Broken Homes is a foundation planned for launch; services and beneficiary referrals are not open. Venture profiles distinguish current development stages and collaborations without implying common ownership.

Before the production domain is connected, confirm the existing host and redirect requirements, business relationships, legal disclosures and ownership of the configured contact mailbox. The detailed handoff is in [the implementation brief](docs/CODEX_IMPLEMENTATION_BRIEF.md), [hosting notes](docs/HOSTING_AND_PUBLISHING.md) and [Broken Homes operating standard](docs/BROKEN_HOMES_OPERATING_STANDARD.md).

Existing parent and venture imagery used in the visual system is documented in [the visual asset register](docs/VISUAL_ASSETS.md).
