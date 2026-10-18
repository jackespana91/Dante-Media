# Dante Media — Integration brief for Codex / existing website

**Target:** https://www.dante-media.io/ (including the non-www domain redirect)
**Scope:** Parent-group repositioning, connected-brand architecture and Broken Homes as a central group-wide commitment.
**Status:** Staged replacement assets and editorial copy supplied; **not deployed**. Review the existing site's source and preserve its highest-quality design and content before integrating changes. **Do not publish without explicit approval.**

## 1. Primary mandate

- Make Dante Media a confident international entrepreneurial group spanning gaming, technology, media, entertainment, sport and community initiatives, not merely a consultancy.
- Place Broken Homes at the heart of the group's identity, homepage, nav, About, Approach, Partnerships, business directory, and footer.
- Explain that Broken Homes is a **foundation planned for launch** with an **ambition** to change thousands of lives, *not* an existing registered charity or a service currently offering support.
- State the group-wide goal: **every group brand and joint venture has an appropriate role in contributing** via funding, talent, time, employment, education, sport, creative opportunity, access or specialist partnerships. The mechanism needs to be agreed and documented for each venture; do not present undocumented percentages or binding promises as already signed.
- Retain the strongest existing branding, animation, films, typography and portfolio material, and improve navigation, accessibility and responsive performance. The supplied static design is a reference/usable rebuild, not proof of the existing stack.

## 2. Suggested information architecture

Home · Our Businesses · Our Approach · Gaming & Technology · Media & Entertainment · Sport & Community · Broken Homes · Partnerships · Our Work · About · News & Updates · Contact.

## 3. Source package

- `content.py`: central brand database and status text; confirm all statuses, domains and group relationships.
- `templates/`: fully authored pages including repeated nav and footer.
- `assets/`: CSS, mobile navigation, interactive portfolio filters, brand SVG and social preview image.
- `build.py`: compiles to `dist/`; run `python build.py`.
- `dist/`: directly deployable HTML/CSS/JS **after approval/go-live checklist**, or use content as a source to port into current framework.

## 4. Actual site integration requirements

1. Inspect the real repository, hosting platform, content management system, route table, SEO setup, styling tokens and any analytics/cookie management before making edits.
2. Add the homepage position and prominently link the foundation. Do not bury it within unrelated venture cards.
3. Implement a filterable portfolio with accurate status and separate legal/commercial relationships. Do not infer ownership from inclusion.
4. Add meaningful cross-links to PlayBeSpoke (`https://playbespoke.com`), Futpal (`https://futpal.io`) and IGW³ (`https://igamingandweb3.com`), subject to verification of production domains and statuses. Don't invent URLs for other initiatives.
5. Include proper page-level meta title/description/canonical, Open Graph, robots and XML sitemap; use organization and webpage schema without pretending all partner ventures are wholly owned subsidiaries.
6. Make the site responsive, semantic, keyboard accessible and suitable for reduced-motion preferences. Test links, focus, forms, mobile nav, performance and semantic markup.
7. Integrate **existing consent-compliant analytics** only if configured; do not insert tracking IDs or implement cookie banners that are fake or untested.
8. Contact: the staging package points group and prospective foundation-partnership enquiries to `info@dante-media.io`, the group's previously supplied address. **Verify delivery, mailbox access and response ownership before go-live**; this address is not a beneficiary intake, crisis or safeguarding service. See `GROUP_EMAIL` in `content.py`.
9. News: only publish announcements and case studies with approved evidence. No fabricated metrics, awards, offices, launches, clients, or impact figures.
10. Implement an internal reporting flow (e.g. Twenty CRM + approved analytics and project sources) later **behind authentication and separately from the public site**. Do not expose commercial, personal or foundation beneficiary information.
11. Do not publish any public donation button, request sensitive case histories, enable direct AI counselling, or imply a safeguarding service is operating until governance, eligibility, qualified escalation routes and privacy have been approved.
12. Review cookie consent, privacy/cookie notices, regulatory requirements in relevant jurisdictions and gambling-content restrictions before release. Keep youth-focused foundation content free of gambling advertisements, lead-generation targeting, gaming/marketing cookies and beneficiary profiling.
13. Preserve existing routes and backlinks with a **tested redirect map**. Avoid redirect chains, canonical inconsistencies and broken rich media.
14. Produce screenshots (desktop/mobile), an accessible page inventory, a list of factual claims needing approval and a rollback plan. Stage first, test fully, **do not automatically publish**.

## 5. Broken Homes — final editorial principle

**Core proposition:** “Where you start shouldn't decide where you finish.”

**Framing:** Some people grow up with instability, financial pressure, social exclusion, unsafe environments or limited opportunity. Broken Homes aims to connect young people and families with trusted people, qualified local support and practical pathways into education, jobs, sport, music, creative opportunities and mentorship.

**Operating model:** Artists and brands can raise awareness; the foundation connects and supports; suitable qualified local specialist organisations deliver professional services. Respect local partner identities, programme safeguards and independent governance.

**Funding/accountability:** Group brands and joint ventures are expected to agree a contribution model appropriate to their involvement. Before any financial amount/percentage is published, obtain signed terms and independent financial/governance review. Future reporting must distinguish targets, commitments, actual contributions and independently verified outcomes.

**Safeguarding:** Design for vulnerable people and minors from the start. No false 24/7 human/AI support promise, no crisis-response claims, no sharing identifiable beneficiary stories without valid consent and safeguarding checks, no advertising gambling to minors, and no reuse of support/beneficiary data in commercial CRM/marketing systems.

## 6. Go-live blockers

- Confirm ownership and exact affiliation language for every listed business, plus status of upcoming ventures.
- Verify legal nature of Broken Homes and whether/how it may publicly call itself a foundation in each jurisdiction.
- Verify and wire a group contact address and handling/response policy.
- Prepare and approve a jurisdiction-appropriate privacy policy, cookie policy/consent and accessibility review.
- Approve all outward-facing status, case study and partner claims.
- Confirm whether the existing site needs to retain pages for previous consulting/advisory services.
- Test staged URL routes, redirects, links, DNS, cross-brand assets and original domain behaviour.

**Publication:** hold changes on staging or a feature branch until the group approves them.
