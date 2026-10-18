# Dante Media — hosting & launch handoff

## What is ready
- Editable 12-page site in this repository, with Broken Homes positioned throughout as a **planned** initiative.
- Production build: `python build.py` creates `dist/`.
- CI checks on the main branch.
- No-index GitHub Pages staging workflow `staging-pages.yml`, **manual trigger only**.

## A preview that will not replace the live website
1. In GitHub, open **Settings > Pages**, and choose **GitHub Actions** as the build/deployment source. This is a repository setting, not a DNS change.
2. Open **Actions > Publish manual staging preview (not live domain) > Run workflow**.
3. On success, review the Pages environment URL for this public repository. Its project path is `/Dante-Media/`. This staging build includes `noindex,nofollow` and blocks crawlers via robots.txt, although those directives do not make the preview private.
4. Share that preview internally to review brand accuracy and visuals. **Do not configure `dante-media.io` or a custom domain during this preview stage.**

## Who currently hosts the real dante-media.io domain?
**Unverified as of 18 October 2026.** A previous separate Dante Media site was published through Design.com in 2025, and an AWS hosting arrangement was once proposed. Neither establishes the current web host of `dante-media.io`.

To confirm the current live hosting location, inspect the existing domain's GoDaddy DNS zone (A, AAAA, CNAME, NS records) and website management subscriptions, or the handover details from the current site developer. **Do not change DNS before capturing/confirming existing configuration.** The domain's MX, SPF, DKIM, DMARC and other email TXT records must be left intact.

## What is required for a safe live launch
- Identify current hosting and take a recoverable backup of existing pages, film, images, scripts, redirects, analytics and SEO metadata.
- Choose to integrate the rebuild into that provider or migrate to an approved new host.
- Verify portfolio relationships, business statuses and factual claims.
- Agree Broken Homes governance, registration language, safeguarding policy and each venture's contribution arrangements. It must not collect beneficiary/referral data or imply that crisis support is available at launch.
- Verify `info@dante-media.io` receives mail and agree who monitors it.
- Publish appropriate legal, privacy and cookie information after approval.
- Take and verify a final production snapshot, launch, then verify both `www` and apex domain responses, mobile behaviour, redirects and SEO.

## Rollback
Keep a complete original-site backup and a record of any DNS records modified. If production errors appear, redeploy the previous known-good release or restore the former DNS target after confirming email records are unchanged. Never assume simply reverting GitHub will change a website hosted outside GitHub.
