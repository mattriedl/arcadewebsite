# ArcadeWebsite — multi-page redesign

## Status: source build, not a completed production deployment

The redesign is a static website with 1,562 game pages, 12 category pages, an All Games page, client-side search, and a publisher-inspired storefront. Every game card is a normal link, not a popup. No server, framework, database, or admin backend is required.

**The original game files are not in this repository.** The supplied local games directory was empty. At the time of checks, the public website displayed a Coming Soon page; public game URLs for 2048, Slope, and Tetris returned 404. The cPanel hostname did not resolve and its supplied server IP timed out. No server backup or production overwrite was performed. Do not interpret this repository or the shell validation as confirmation that games are playable.

## Files and rebuild

`site/` is the web root. `build.py` generates the HTML and search index from `site/assets/games-data.json`. Existing generated thumbnails are retained in `site/thumbnails/`. Duplicate titles have stable ID suffixes so all catalog entries receive distinct pages. There are no invented popularity figures or ratings; Trending and New sections are explicitly labeled editorial/library selections because the catalog has no reliable trend or release-date data.

Run with Python 3:

```sh
python3 build.py
python3 validate.py
python3 package.py
python3 -m http.server 3000 --directory site
```

Open `http://localhost:3000` on the computer running that command. Games will not play until the original files and their dependencies are restored under `site/games/`. Do not create replacement game files merely to make tests pass. `validate.py` reports missing originals separately from broken shell links.

## URL structure and SEO

Game pages live at `/game/<slug>/index.html`, categories at `/category/<slug>/index.html`, the complete catalog at `/all-games/`, and search at `/search/?q=2048`. Iframes point to `/games/<encoded-filename>` with literal percent signs encoded again. This distinguishes a real space from a filename containing the literal characters `%20`. Unicode, spaces, hashes and question marks are URL encoded rather than treated as path syntax.

Each page includes unique title and description text, canonical, Open Graph, Twitter metadata, and one semantic H1. Game pages have VideoGame and BreadcrumbList JSON-LD, category pages have CollectionPage and BreadcrumbList, and All Games has CollectionPage. The sitemap lists 1,576 indexable URLs. Search is noindex/follow and excluded from the sitemap. Category and All Games grids render all entries statically and lazy-load thumbnails.

## Ads: one central configuration

Edit `site/assets/ads.js`. Empty entries show labeled placeholders; no ads or tracker IDs are active by default. The game page IDs are `top-leaderboard` (728×90), `left-sidebar` and `right-sidebar` (160×600), `below-game` (728×90), and `related-infeed` (300×250). Sidebars are hidden at widths up to 1,100px. At widths up to 650px, leaderboard space becomes 320×100; choose responsive or appropriately sized mobile ad units. Homepage uses `home-leaderboard` and `home-infeed`; category and All Games use `category-leaderboard` and `category-infeed`.

For AdSense, replace the publisher and unit IDs in the following example. Put the SDK URL into `networkScript`, set `adsense: true`, and paste each unit's **ins element only** into the matching `slots` string:

```js
networkScript: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_ID',
adsense: true,
slots: {
  'top-leaderboard': '<ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px" data-ad-client="ca-pub-YOUR_ID" data-ad-slot="YOUR_UNIT_ID"></ins>',
  // Keep the other existing slot keys; fill each with its own unit HTML.
}
```

This fixed-size example is desktop-only; configure a responsive ad unit for slots shown on mobile. The loader initializes AdSense units centrally and skips hidden sidebars. Script tags pasted into slot HTML are inert; other ad networks requiring JavaScript initialization need their SDK and initialization integrated into this same central file. Do not load the SDK separately on every page or every slot. Check ad spacing, accidental-click rules and publisher policy before enabling ads around interactive game controls.

Approval and revenue are not guaranteed. Confirm distribution rights for every game, implement any required privacy disclosures and consent controls, and add the network's genuine ads.txt entry when supplied. There is no fabricated ads.txt or consent claim in this build.

## Google Analytics

Change only `GA_MEASUREMENT_ID` in `site/assets/analytics.js` from `G-XXXXXXXXXX` to your GA4 ID. Every page includes this file; with the placeholder, no Analytics request is sent. Configure consent and privacy requirements before activating tracking.

## Safe cPanel deployment — still pending

Use the downloaded `arcadewebsite-redesign.tar.gz`, or regenerate it with `python3 package.py`. The overlay contains the generated HTML, assets, favicon, sitemap, robots.txt and .htaccess; it deliberately contains **neither games nor thumbnails**. The thumbnails must already be in the actual document root, or you can upload them separately from `site/thumbnails/` only if missing. Never delete or relocate the existing games or thumbnails.

Before overwriting anything, use cPanel File Manager to confirm the domain's document root is `/home/hardwaremec/public_html/arcadewebsite.com/`. Enable Show Hidden Files. Select the current `index.html`, `assets/`, `sitemap.xml`, `.htaccess`, and, if present, `robots.txt`, `game/`, `category/`, `all-games/`, and `search/`. Compress them to a timestamped backup stored outside the public document root, and confirm the backup exists and opens before continuing. The earlier reported backup is not a substitute for a fresh backup, and was not verified in this run.

Upload the overlay archive into the confirmed document root, extract **there**, and check `game/2048/index.html` exists directly under it, not inside an extra `site/` or repository folder. Review overwrite prompts before approving. No automatic extraction or server-side backup was attempted during this run because cPanel was unreachable. A GitHub push alone does not deploy to cPanel.

The supplied .htaccess uses DirectoryIndex plus real directories, gzip and caching. It deliberately does not redirect HTTP to HTTPS because Cloudflare Flexible connects to the origin over HTTP; an unconditional redirect can loop. Do not change DNS as part of this overlay deployment. If necessary, purge the existing HTML/assets cache in Cloudflare after extraction.

Confirm the production domain actually serves this document root; the observed Coming Soon page and missing assets may mean routing, vhost configuration or deployment state differs from the earlier context. This is a hypothesis, not a confirmed root cause. Restore the original game files and dependencies from a verified backup if they are genuinely missing, and inspect filename encoding against the server's real file names.

After deployment, verify `/`, `/game/2048/`, `/game/tetris/`, `/game/slope/`, `/category/puzzle/`, `/category/racing/`, `/all-games/`, `/search/?q=2048`, `/sitemap.xml` and `/robots.txt` through HTTPS. Check that all three games actually render and respond inside their iframe, fullscreen enters/exits, related links and share links work, and mobile pages fit at 390px. Also sample literal-percent, Unicode and space-containing game filenames on the origin. Until those checks pass, production playability remains unverified.

## Verification performed

Static shell validation found 1,577 HTML pages, 1,577 unique titles and descriptions, 1,562 iframe paths and no broken generated shell links or thumbnail references. All 1,562 original game files were absent locally and were explicitly reported, not hidden. JavaScript syntax checks passed. The local homepage, three game-page shells, two categories and sitemap responded 200; the local carousel changed its destination and the fullscreen button entered the player container. Search for 2048 displayed 2048 and 2048 Cupcakes with dedicated game-page links. Embedded 390px viewport checks of home, game, category and All Games found no horizontal overflow; sidebars were hidden on the game page. These are local checks, not production acceptance.
