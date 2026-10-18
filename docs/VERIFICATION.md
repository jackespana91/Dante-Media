# Website implementation checkpoint — 18 October 2026

The editable website is available in PR #2 and the local preview. This record describes the modern aperture visual revision.

## Current visual system

- Twelve authored routes sharing near-white surfaces, graphite typography, a controlled lime accent and self-hosted DM Sans / Space Grotesk.
- Original 800 × 900 native SVG aperture artwork: a sculptural silver doorway with lime interior reveals. The header uses a small flat interpretation; supplied brand artwork remains preserved.
- A three-line display hero with concise copy, one primary action and a mobile composition that keeps the sculpture visible.
- An asymmetric selected-venture feature: PlayBeSpoke gameplay leads, with separately composed Futpal and IGW³ panels. Development stages remain readable and explicit.
- Refined rounded actions, circular arrow details, sector hover states, matching inner-page image treatments, pale aperture crops on editorial heroes and a large typographic footer.
- A community-room illustration for Broken Homes, with its planned status retained. Source notes and the earlier image generation prompt are in `VISUAL_ASSETS.md`.
- Existing responsive navigation and shareable portfolio filters retained. Motion is limited to a brief aperture entrance and hover transitions; reduced-motion preferences disable these effects.

## Current build and visual review

`.venv/bin/python build.py` compiled all 12 pages after the visual changes.

Rendered review covered the 1440px homepage, directory, About, Work and Contact, plus the homepage at 390px and 320px. Refinements included action styling, hero proportions, the Futpal crop, narrow-screen typography, secondary colours and aperture/wordmark consistency. No new automated test suite was added or manually run for this visual revision.

## Earlier automated checkpoint

The previous committed revision (`5464e52`) passed the existing GitHub validation workflow. Its regression suite covers production and `/Dante-Media/` staging builds, routes, links/fragments, CSS assets/fonts, metadata, JSON-LD, sitemap, robots, planned foundation status and preservation of prior output when configuration or templates fail. Current-commit CI results are recorded by GitHub separately.

## Publication

The live domain has not been changed. Hosting integration remains in `HOSTING_AND_PUBLISHING.md`. Broken Homes is planned, does not yet deliver services and does not accept beneficiary referrals. No invented launch dates, customer metrics or delivered impact outcomes have been added.
