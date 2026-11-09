# Site redesign: executive, modern, unmistakably personal

Date: 2026-11-09
Status: draft for approval

## Intent

The site structure (About as homepage, Blog, Projects, Resume, Contact) works. The look does not: it is the 2018 "Pillar" Bootstrap 4 resume template by 3rd Wave Media, with a saturated blue hero band, "Hello, my name is", Roboto everywhere, and skill cards with checkmark lists. It reads as dated and as a stock template.

The goal is a site that feels **professional, polished and precise**, with an **executive** tone, and that does **not** feel AI-generated.

### Audience

- **Recruiters and hiring executives** skim for about ten seconds. They need role, seniority, credentials and career at a glance.
- **Peers** come to read articles and look at projects. They need a comfortable long-form reading experience and a reason to keep going.

Every page has to serve both: a scannable top, and depth below.

## Goals

1. A light, modern, executive look with a single coherent visual system across all pages.
2. A homepage that communicates "senior, credible, executive" in one screen, using concrete facts instead of slogans.
3. A long-form article experience that peers enjoy reading.
4. Replace the template's foundations (Bootstrap 4, jQuery, Font Awesome 5, isotope, share bar) with a small hand-written stylesheet and minimal vanilla JS.

## Non-goals

- Changing site structure, page set, URLs or article content. All existing URLs must keep working (SEO).
- Dark mode. The owner judged the dark direction "less executive"; it is out of scope.
- A CMS, a JS framework, or a build pipeline beyond Pelican.
- Comments. Disqus is already disabled in `publishconf.py`; the new article template drops the include.

## Anti-goals (failure even if it technically works)

The site must not look AI-generated. Specifically avoid:

- centered hero with a pill/badge above a slogan headline
- rows of three symmetric rounded cards with icons
- stat boxes / KPI strips, gradient backgrounds, grid-pattern backgrounds, glassmorphism
- monospace "// comment" decoration, emoji, decorative icon sets
- generic interchangeable copy ("turning data into decisions", "passionate about...")
- Inter as the typeface (the default of generated sites)

Credibility comes from **specific facts**: real roles, years, platforms, numbers, real screenshots.

## Visual system (decided)

Decided with the owner through mockups (final homepage mockup: `.superpowers/brainstorm/55777-1794261954/content/mix-v4.html`, local only). It combines the layout of the "Executive editorial" direction with the type and polish of the "Executive modern" direction.

### Typography

- **Hanken Grotesk** (Google Fonts, weights 400/500/600/700) for everything except article body text.
- Headlines: weight 600, tight tracking (about `-0.03em` at display sizes), line-height about 1.1.
- Small labels: 13px, uppercase, `letter-spacing: 0.06–0.08em`, weight 500–600.
- Years and dates use `font-variant-numeric: tabular-nums`.
- **Source Serif 4** for article body text only (see Article page). *Claude's call, approved in principle by the owner as part of the recommendations.*

### Color

| Token | Value | Use |
|---|---|---|
| ink | `#0d1b2a` | headings, primary text, primary button, heavy rules |
| body | `#445063` | paragraph text |
| muted | `#556070` | secondary text, nav links, captions |
| rule | `#e6e9ee` | hairline dividers |
| border | `#c9d0d9` | secondary button border |
| accent | `#0b5563` (deep teal) | **small details only**: years, "see all" links, credential title, link underlines |
| tint | very light neutral, e.g. `#f6f8f9` | one band behind the projects/writing section *(Claude's call)* |
| page | `#ffffff` | background |

One accent color. No second accent. Text and link colors must meet WCAG AA contrast.

### Shape and detail

- Buttons: rectangular, `border-radius: 4px`, 15px, weight 600, padding about `11px 20px`. Primary = ink fill, white text. Secondary = 1px border, ink text.
- Section headers: a 2px ink rule on top, an uppercase label on the left, an accent "All →" / "Full resume →" link on the right.
- Lists are separated by 1px hairline rules, not boxed in cards or shadows.
- Photo corners: `border-radius: 4px`. No circles except the small author avatar on articles.

### Layout

- Content max width about 1120px with generous side padding (64px desktop, 16–20px mobile).
- Nav: name on the left (weight 700), links on the right (Writing, Projects, Resume, Contact). Contact is the darkest link. 1px rule under the nav. On mobile, a simple disclosure menu (vanilla JS or `<details>`).
- Footer: copyright line and social links (LinkedIn, GitHub, X, Medium) as inline SVG icons. Remove the template credit.

## Homepage (`about.html`, decided)

Top to bottom:

1. **Nav** as above.
2. **Hero**, two columns: text left (fluid), portrait right (fixed **240px** wide, 4:5 crop, `object-position` about `center 30%`). Text block aligned to the bottom of the photo.
   - Credentials line: `CTO, Panevo · P.Eng. · Vancouver` (title in accent).
   - Headline (first person, concrete), e.g. "I build and run enterprise data platforms for industrial and energy companies."
   - Paragraph: first developer at Panevo, built both platforms from scratch, now owns technology, product and operations; six years of energy R&D before software.
   - Optional **proof line** about scale/customers (see Open items).
   - Buttons: **View resume** (primary), **Selected projects** (secondary).
3. **Career ledger**: section header "Career" + "Full resume →". Three rows, each a grid of `years | role + company | one-line summary`:
   - 2022 to now · Chief Technology Officer · Panevo
   - 2017 to 2021 · Lead Developer · Panevo
   - 2012 to 2017 · R&D Engineer · Enertime
4. **Two columns on the tint band**: "Selected projects" (ioTORQ EMIS, ioTORQ LEAN, A320 Expert; name + one line, each linking to its existing project page. A320 Expert is the owner's choice: one of the biggest projects outside Panevo, a B2C training platform for Airbus A320 pilots) and "Recent writing" (latest 3 articles, title + month/year), each with "All →".

The current "Overview" skill cards are removed from the page. `SKILLS_OVERVIEW` stays in `pelicanconf.py` because it feeds the JSON-LD `knowsAbout`.

Mobile: photo stacks above the credentials line (smaller, e.g. 160px), ledger rows collapse to stacked lines, the two columns stack.

**Copy** (owner's direction: reuse and reword the current `about.md` text; do not list skills). Use this, replacing the example headline and paragraph above:

- Headline: "I build and scale data-intensive platforms for industrial and enterprise applications."
- Paragraph: "Over 14 years in software and systems engineering, I've led teams, set technology strategy, and taken products from zero to one through to enterprise adoption, with a focus on reliability, real-time performance and security. I've built industrial IoT platforms for energy management and lean manufacturing, and training tools used directly by professional pilots."

The three current body paragraphs of `about.md` are folded into this copy and removed. Hero text should continue to come from `content/pages/about.md` so it stays editable as content: a new `headline` front-matter field for the headline, the existing `intro` field for the paragraph *(Claude's call on the field mapping)*. Editing `about.md` triggers the `Modified:` rule in `CLAUDE.md`.

**Data**: career rows and selected projects become lists in `pelicanconf.py` (like `SKILLS_OVERVIEW`) *(Claude's call)*. Recent writing uses the latest 3 entries of `articles`.

**Photo**: new portrait supplied by the owner at repo root, `founder.jpg` (1200×1799). Move it to `content/images/`, export a web-sized version (e.g. 600px wide for 2x display at 240px, plus a JPEG/WebP pair if convenient), and use it for `AUTHOR_PROFILE_IMAGE` / `og:image`. Delete the stray `founder.jpg:Zone.Identifier`.

## Other pages (Claude's calls, same system)

### Blog index (`index.html` → `blog.html`)

- Page heading "Writing" with a one-line intro (replace "Some thoughts and lessons learned...").
- Articles as a ruled list: title (Hanken 600, about 22px), date + reading time (from the `post_stats` plugin) in muted text, summary in body color, small preview thumbnail on the right on desktop (articles already have `previewimage`), hidden on mobile.
- Restyled pagination: plain "← Newer" / "Older →" links.

### Article page (`article.html`)

- Header: title (Hanken 600, large), then date · reading time · category in muted text. No colored hero band.
- Body: **Source Serif 4**, about 19px, line-height about 1.7, max width about 68ch, centered column. Headings in Hanken Grotesk. Keep current good decisions from `content/extra/custom.css` (left-aligned text, list spacing, dark code blocks) but restyle with the new tokens; the indigo `#5a67d8` heading bars go away (accent becomes teal or plain rules).
- Code blocks: keep a dark theme; align colors to the palette.
- Footer of article: short author card (small round photo, name, one-line bio, link to About), then "More writing" (2–3 other articles).
- Remove the jQuery social share bar and the Disqus include.

### Projects (`projects.html`)

- Keep the category filters (All, Web, Data, Machine Learning, Energy Sciences), rewritten in vanilla JS (toggle a class / `hidden`) instead of isotope.
- Projects in a 2-column (desktop) grid of image-led entries: the existing real thumbnail (`images/projects/*-thumb.png`), name, one-line description, technologies as a plain muted text list separated by " · " (no pill badges). No hover overlays or shadows; a subtle border or rule is fine.
- Projects currently hardcoded in the template may stay hardcoded or move to data; builder's choice, but fix the backslash links (`projects\iotorq.html`).

### Project detail (`project_detail.html`)

- Header: name, one-line summary, technologies as text, repository link if present.
- Replace the Bootstrap carousel with images stacked in the content column (first image as lead image), each full content width with 4px radius.
- Replace the technology logo grid (`/images/webdev-icons/*.svg`) with the text list in the header.

### Resume (`resume.html`)

- Same content, restyled in the ledger style: experience as rows (years | role + company | description and bullets), then education, certifications, skills, awards in the same ruled-section pattern.
- **No PDF download.** The owner decided the online resume is the canonical version; `docs/resume_tartieret.pdf` (2021) stays unlinked.
- **No visible email address** (remove the Gmail line from the resume header). LinkedIn and GitHub links are fine.
- Print stylesheet so the HTML resume prints cleanly *(nice-to-have)*.

### Contact (`contact.html`)

- Keep the Formspree form (`EMAIL_ACTION`, `_gotcha`, `_subject`). Restyle inputs: 1px border, 4px radius, generous padding, visible focus ring in accent.
- **No visible email address anywhere on the site** (owner's decision); the form is the only email channel. A LinkedIn link beside the form is fine.

### Remaining generic templates

`archives`, `tags`, `tag`, `categories`, `category`, `author(s)`, `period_archives`, `page`: inherit the new base and reuse the blog list styling. Low priority, but must not break.

## Technical approach

- Stay on **Pelican 4.11** with the existing `themes/Custom` theme; rewrite templates in place.
- Remove from `base.html`: Bootstrap CSS/JS (CDN), the bundled `resume.css` (8.7k lines incl. Bootstrap), jQuery, Popper, Font Awesome, `main.js`, isotope, imagesloaded, social-share-bar, back-to-top.
- One new stylesheet (e.g. `static/css/site.css`) with CSS custom properties for the tokens above. Fold the useful parts of `content/extra/custom.css` into it and drop the `CUSTOM_CSS` / `EXTRA_PATH_METADATA` entry for it (or keep the file empty), *builder's choice*.
- Minimal vanilla JS only for: mobile nav, project filters.
- Social icons as inline SVG.
- Favicon: simple "TT" monogram (SVG + PNG fallback) *(Claude's call)*.
- `BROWSER_COLOR` → ink `#0d1b2a`.

### Must keep working

- Google Analytics tag, canonical URLs, Open Graph / Twitter meta, JSON-LD (Person, WebSite, articles), `sitemap.xml` (homepage `lastmod` from `about.md` `Modified:`), `robots.txt`, `llms.txt`, all existing URLs, PDFs under `docs/`.
- Per `CLAUDE.md`: when `content/pages/about.md` is edited, update its `Modified:` date and time.

### Housekeeping

- Add `.superpowers/` to `.gitignore`.
- Unused theme assets (pygments variants, isotope, old JS) can be deleted.

## Verification

- `make html` builds without errors or new warnings.
- Visual check of every page type (home, blog, article with code, projects + filter, project detail, resume, contact, tag/category) at desktop (about 1280px) and mobile (about 375px) widths, e.g. with Playwright screenshots.
- No horizontal scroll on mobile; nav menu works; filters work.
- Lighthouse (or equivalent) accessibility and SEO checks do not regress; color contrast passes AA.
- Spot-check that canonical, OG and JSON-LD output is unchanged except for the new image.

## Open items (owner)

1. **Proof line**: a concrete scale or customer line for the hero, if shareable. Ship without it if not available.

## Left to the builder

Exact spacing scale, breakpoints, font loading strategy (Google Fonts vs self-hosting), file/partial organization, and whether project and career data live in templates or `pelicanconf.py`, as long as the decisions above hold.
