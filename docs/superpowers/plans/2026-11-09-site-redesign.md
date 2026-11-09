# Site Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the 2018 Bootstrap "Pillar" theme with a light, executive, hand-written design across every page of the Pelican site, without changing URLs, content structure or SEO output.

**Architecture:** Rewrite the templates of `themes/Custom` in place on top of one new stylesheet (`static/css/site.css`, CSS custom properties) and no third-party CSS/JS. Homepage and projects data move into `pelicanconf.py` lists so the homepage and the Projects page share them. A pytest suite builds the site into a temp dir and asserts on the generated HTML with BeautifulSoup; it is written first and guards SEO output and internal links throughout.

**Tech Stack:** Pelican 4.11 (Jinja2), Markdown, plain CSS, vanilla JS (project filters only), pytest + beautifulsoup4, ffmpeg (image resizing), Playwright (visual checks, favicon rasterizing).

**Spec:** `docs/superpowers/specs/2026-11-09-site-redesign-design.md`. Read it before starting any task; it holds the exact colors, type, layout and copy.

## Global Constraints

- Work on a branch `site-redesign` (never commit to `master`).
- Install deps into the existing venv first: `.venv/bin/pip install -r requirements.txt -r requirements-dev.txt` (the venv currently has Pelican 4.10.1; requirements pin 4.11.0).
- Fonts: Hanken Grotesk 400/500/600/700 everywhere; Source Serif 4 for article body text only. Loaded from Google Fonts with `display=swap`. Never Inter or Roboto.
- Colors (copy exactly): ink `#0d1b2a`, body `#445063`, muted `#556070`, rule `#e6e9ee`, border `#c9d0d9`, accent `#0b5563`, tint `#f6f8f9`, page `#ffffff`. One accent only. No dark mode.
- Buttons: `border-radius: 4px`, 15px, weight 600, padding `11px 20px`. Photos: `border-radius: 4px`.
- Forbidden (anti-goals): pill badges, stat boxes, gradients, grid-pattern backgrounds, symmetric icon cards, monospace decoration, emoji, Font Awesome, Bootstrap, jQuery.
- No visible email address and no `mailto:` anywhere in the output. No link to `docs/resume_tartieret.pdf`.
- All existing output URLs keep working. Canonical, Open Graph, Twitter, JSON-LD, sitemap, robots.txt, llms.txt and the Google Analytics tag (`G-PPQKSCH1B2`) stay.
- Internal links and asset URLs in templates are absolute from site root (`{{ SITEURL }}/...`), never relative (`blog.html`) or backslashed.
- Whenever `content/pages/about.md` is edited, set its `Modified:` to the current date and time (CLAUDE.md).
- No em dashes in user-facing copy.

## Review Focus

1. **Nested pages** (`projects/*.html`, `tag/*.html`, `category/*.html`, `author/*.html`): nav, CSS, images and links must resolve; today's `href="blog.html"` breaks there. Pinned by `test_internal_links_resolve` (Task 1).
2. **Missing optional metadata**: articles without `PreviewImage`, project pages with empty `Images:` (e.g. ioTORQ Data Exporter) or no `website`/`repository`. Expect no empty `<img src>` and no empty links. Pinned by `test_no_empty_images_or_links` (Task 1) and `test_project_without_images` (Task 6).
3. **Mobile width (375px)** with long titles and long code lines: page must not scroll horizontally; code blocks scroll inside themselves. Pinned by the Playwright check in Task 9.
4. **Pagination** once there are more than `DEFAULT_PAGINATION` articles: `blog2.html` must render with working Newer/Older links. Pinned by `test_pagination_links` (Task 5), using a build with `DEFAULT_PAGINATION=2`.
5. **Publish build** (`publishconf.py`: absolute `SITEURL`, Atom feeds on): canonical and `og:url` absolute, feed `<link>` present. Pinned by `test_publish_build_absolute_urls` (Task 1).

---

### Task 1: Test harness, SEO baseline and housekeeping

**Files:**
- Create: `requirements-dev.txt` (`pytest`)
- Create: `tests/conftest.py`, `tests/test_seo.py`, `tests/test_links.py`
- Modify: `.gitignore` (add `.superpowers/`)
- Delete: `founder.jpg:Zone.Identifier` (keep `founder.jpg` for Task 2)

**Interfaces:**
- Produces fixtures in `tests/conftest.py`:
  - `site() -> pathlib.Path` (session scope): runs `[sys.executable, "-m", "pelican", "content", "-o", <tmp>, "-s", "pelicanconf.py"]` from repo root, asserts exit code 0, returns the output dir.
  - `publish_site() -> Path`: same with `-s publishconf.py`.
  - `paginated_site() -> Path`: same as `site` plus `-e DEFAULT_PAGINATION=2`.
  - `page(site_dir: Path, rel: str) -> bs4.BeautifulSoup` helper (plain function, importable as `from conftest import page`).
  - `all_html(site_dir: Path) -> list[Path]` helper.

- [ ] **Step 1: Create branch** `git checkout -b site-redesign`; install deps per Global Constraints.
- [ ] **Step 2: Write SEO baseline tests** in `tests/test_seo.py` that pass on the current theme:
  - `test_homepage_seo`: `index.html` has `<link rel=canonical>`, `og:title`, `og:description`, `og:image`, `twitter:card == "summary_large_image"`, a `application/ld+json` script whose `@graph` contains `@type` `Person` and `WebSite`, and the GA script `googletagmanager.com/gtag/js?id=G-PPQKSCH1B2`.
  - `test_article_seo`: `a-senior-developer-playbook.html` has canonical, `og:type == "article"` (or current value; read it first and pin it), and JSON-LD `@type` `BlogPosting` (pin the current type) with `headline`.
  - `test_sitemap_and_robots`: `sitemap.xml`, `robots.txt`, `llms.txt` exist; sitemap contains `resume.html` and `projects.html`.
  - `test_publish_build_absolute_urls(publish_site)`: canonical and `og:url` on `index.html` and one article start with `https://thomastartiere.com`; a `<link type="application/atom+xml">` is present.
- [ ] **Step 3: Write link tests** in `tests/test_links.py`:
  - `test_internal_links_resolve`: for every output HTML file, every `href`/`src` that is site-internal (relative, or starts with `/`, or with `SITEURL`; skip `#`, `http(s)://` external, `mailto:`) and has no backslash, resolves to an existing file in the output dir (resolve relative to the page's own directory; strip query/fragment; directory `/` maps to `index.html`). Also assert no `href` contains `\`.
  - `test_no_empty_images_or_links`: no `<img>` with empty `src` or `src` ending in `/`; no `<a>` with empty `href`.
  - `test_no_mailto_or_pdf_resume`: no `mailto:` and no `resume_tartieret.pdf` in any HTML file.
- [ ] **Step 4: Run** `.venv/bin/python -m pytest -q`. Expected: SEO tests PASS; link tests FAIL on the current theme (relative `blog.html` on nested pages, backslash project links, the resume Gmail). Record the failures in the commit message; they are fixed by later tasks.
- [ ] **Step 5: Housekeeping**: add `.superpowers/` to `.gitignore`, delete `founder.jpg:Zone.Identifier`.
- [ ] **Step 6: Commit** `test: add site build test harness and SEO baseline` (include tests, requirements-dev.txt, .gitignore, spec and this plan).

### Task 2: Base layout and design system

**Files:**
- Create: `themes/Custom/static/css/site.css`
- Create: `content/images/portrait.jpg` (1200px wide, from `founder.jpg`), `content/images/portrait-600.jpg` (600px wide)
- Create: `content/images/favicon.svg`, `content/images/favicon-32.png`, `content/images/apple-touch-icon.png` (180px)
- Modify: `themes/Custom/templates/base.html`, `pelicanconf.py`
- Delete: `founder.jpg` (after resizing)
- Test: `tests/test_base.py`

**Interfaces:**
- Produces settings: `AUTHOR_PROFILE_IMAGE = "/images/portrait.jpg"` (og:image, JSON-LD), `AUTHOR_PHOTO = "/images/portrait-600.jpg"` (on-page display), `FAVICON = "/images/favicon.svg"`, `BROWSER_COLOR = "#0d1b2a"`.
- Produces in `site.css`: the tokens as `--ink --body --muted --rule --border --accent --tint --page`, font vars `--sans`, `--serif`; layout classes later tasks use: `.container` (max-width 1120px, padding 64px desktop / 20px mobile), `.btn`, `.btn-primary`, `.btn-secondary`, `.section-head` (2px ink top rule, uppercase label left, accent link right), `.ruled-list > li` (1px `--rule` bottom border), `.label` (13px uppercase, letter-spacing .06em), `.muted`, `.tint-band`.
- Produces `base.html` blocks (keep all existing ones: `head`, `title`, `description`, `meta`, `og_type`, `og_image`, `structured_data`, `page_specific_css`, `content`, `page_specific_js`); `header_intro` is removed. Body gets `class="{% block body_class %}{% endblock %}"`.

- [ ] **Step 1: Write failing tests** in `tests/test_base.py`, parametrized over `index.html`, `blog.html`, `resume.html`, `projects.html`, `contact.html`, `projects/a320expert.html`, one article:
  - `test_no_legacy_assets`: page source contains none of `bootstrap`, `jquery`, `fontawesome`, `font-awesome`, `isotope`, `share-bar`, `Roboto`, `3rdwavemedia`.
  - `test_nav`: a `<nav>` with links whose paths are exactly `/`, `/blog.html`, `/projects.html`, `/resume.html`, `/contact.html` (with `SITEURL` prefix), text Writing/Projects/Resume/Contact plus the name linking home; the current page's link has `aria-current="page"`.
  - `test_fonts_and_css`: a stylesheet link containing `Hanken+Grotesk` and one to `theme/css/site.css`.
  - `test_footer`: footer has links to the four `SOCIAL` URLs, each with an inline `<svg>` and an `aria-label`; copyright text contains `Thomas Tartière`.
  - `test_favicon_and_theme_color`: `<link rel="icon" type="image/svg+xml">` present; `meta[name=theme-color]` content `#0d1b2a`; `og:image` ends with `/images/portrait.jpg`.
- [ ] **Step 2: Run** `pytest tests/test_base.py -q`. Expected: FAIL.
- [ ] **Step 3: Images**: `ffmpeg -i founder.jpg -vf scale=1200:-1 -q:v 3 content/images/portrait.jpg` and `scale=600:-1` for `portrait-600.jpg`; delete `founder.jpg`. Favicon: an SVG with "TT" in ink on white, weight 700, rounded 4px square; rasterize 32px and 180px PNGs with Playwright (screenshot the SVG at that size).
- [ ] **Step 4: Rewrite `base.html`**: keep the whole `<head>` meta/SEO/GA logic; replace Bootstrap/FA/jQuery/theme CSS with Google Fonts + `site.css`; nav per spec (name left weight 700, links right, Contact darkest, 1px rule below) with mobile menu as a `<details>` disclosure below 720px (no JS); footer per spec with inline SVG icons from `SOCIAL`; drop template credit, share bar and all script tags except GA and `page_specific_js`. Remove `CUSTOM_CSS` loading here only after Task 5 folds it in (keep the `{% if CUSTOM_CSS %}` link until then).
- [ ] **Step 5: Write `site.css`** base: tokens, reset, typography (Hanken; headings weight 600, display tracking `-0.03em`, line-height 1.1), links (accent underline), the shared classes listed in Interfaces, `:focus-visible` outline in accent, and `img { max-width: 100% }`.
- [ ] **Step 6: Run** `pytest -q`. Expected: `test_base.py` PASS, Task 1 SEO tests still PASS. Other pages look unstyled until their task; that is expected on this branch.
- [ ] **Step 7: Commit** `feat: new base layout, design tokens and portrait`.

### Task 3: Projects data and Projects page

**Files:**
- Modify: `pelicanconf.py` (add `PROJECTS`, `PROJECT_FILTERS`)
- Modify: `themes/Custom/templates/projects.html`
- Create: `themes/Custom/static/js/projects-filter.js`
- Test: `tests/test_projects.py`

**Interfaces:**
- Produces `PROJECT_FILTERS = (("web", "Web"), ("data", "Data"), ("machine-learning", "Machine Learning"), ("energy", "Energy Sciences"))`.
- Produces `PROJECTS`: tuple of dicts, one per card in the current `projects.html`, in the same order, keys `slug: str` (output is `projects/{slug}.html`), `title: str`, `summary: str` (the card's overlay sentence, rewritten as a plain sentence without "!"), `thumb: str` (path under `/images/projects/`), `filters: list[str]` (keys from `PROJECT_FILTERS`, taken from the card's isotope classes), `technologies: list[str]` (the card's badges). Add a module-level assert that slugs are unique.
- Produces in templates: `{% set by_slug = PROJECTS|... %}` is not needed; Task 4 looks projects up with `selectattr("slug", "equalto", s)`.

- [ ] **Step 1: Write failing tests** in `tests/test_projects.py`:
  - `test_project_grid`: `projects.html` has one `article.project` per `PROJECTS` entry (import `pelicanconf` to count), each with an `<img>` whose `src` ends with its `thumb`, an `<h2>` link to `/projects/{slug}.html`, and a technologies line equal to `" · ".join(technologies)`.
  - `test_project_filters_markup`: filter buttons for "All" plus each `PROJECT_FILTERS` label, each `<button type="button" data-filter=...>`; each project has `data-filters` containing its keys; script `theme/js/projects-filter.js` included.
  - `test_no_badges`: no element with class containing `badge` on the page.
- [ ] **Step 2: Run** `pytest tests/test_projects.py -q`. Expected: FAIL.
- [ ] **Step 3: Move card data** from `projects.html` into `PROJECTS` / `PROJECT_FILTERS`.
- [ ] **Step 4: Rewrite `projects.html`**: page heading "Projects" + one-line intro, filter buttons, 2-column grid (1 column under 720px) of `article.project` entries: thumbnail (4px radius, 1px `--rule` border, no overlay/shadow), title, summary, technologies as muted text joined by " · ".
- [ ] **Step 5: Write `projects-filter.js`**: clicking a button sets `aria-pressed` on it and toggles `hidden` on projects whose `data-filters` (space-separated) lacks the key; "All" shows all. No dependencies.
- [ ] **Step 6: Run** `pytest -q`. Expected: projects tests PASS; the backslash-link failure from Task 1 is gone.
- [ ] **Step 7: Commit** `feat: data-driven projects page with vanilla filters`.

### Task 4: Homepage

**Files:**
- Modify: `pelicanconf.py` (add `HERO_CREDENTIALS`, `CAREER`, `SELECTED_PROJECTS`)
- Modify: `content/pages/about.md`, `themes/Custom/templates/about.html`
- Test: `tests/test_home.py`

**Interfaces:**
- Consumes: `PROJECTS` (Task 3), `AUTHOR_PHOTO`, shared CSS classes (Task 2).
- Produces settings:
  - `HERO_CREDENTIALS = ("CTO, Panevo", "P.Eng.", "Vancouver")` (first item rendered in accent, joined by " · ").
  - `CAREER = ({"years": "2022 to now", "role": "Chief Technology Officer", "company": "Panevo", "summary": "End-to-end ownership of technology, product, security and operations across two enterprise platforms."}, {"years": "2017 to 2021", "role": "Lead Developer", "company": "Panevo", "summary": "First architect and developer. Built the real-time energy data platform and the lean manufacturing platform."}, {"years": "2012 to 2017", "role": "R&D Engineer", "company": "Enertime", "summary": "Multi-million-dollar energy R&D projects across software, modeling and hardware."})`
  - `SELECTED_PROJECTS = ("iotorq", "iotorq-lean", "a320expert")`
- Produces `about.md` front matter: new `headline:` field; `intro:` replaced. Exact copy from the spec's Homepage "Copy" section. Body paragraphs removed. `Modified:` updated.

- [ ] **Step 1: Write failing tests** in `tests/test_home.py`:
  - `test_hero`: `index.html` has exactly one `<h1>` with text "I build and scale data-intensive platforms for industrial and enterprise applications."; the paragraph after it starts with "Over 14 years in software and systems engineering"; credentials line text equals "CTO, Panevo · P.Eng. · Vancouver"; an `<img>` with `src` ending `portrait-600.jpg` and non-empty `alt`; buttons linking to `/resume.html` ("View resume") and `/projects.html` ("Selected projects").
  - `test_career_ledger`: a section headed "Career" with a "Full resume" link to `/resume.html` and 3 rows whose years/role/company match `CAREER` in order.
  - `test_selected_projects`: 3 links in order to `/projects/iotorq.html`, `/projects/iotorq-lean.html`, `/projects/a320expert.html`, with titles from `PROJECTS`.
  - `test_recent_writing`: 3 links to the 3 most recent articles by date (compute from `content/articles/*.md` `Date:` headers), each with "Month YYYY".
  - `test_no_skill_cards`: no text "Overview" heading and no `skills-` classes; JSON-LD `knowsAbout` still non-empty.
- [ ] **Step 2: Run** `pytest tests/test_home.py -q`. Expected: FAIL.
- [ ] **Step 3: Add settings**, then update `about.md` (headline, intro, remove body, `Modified:` now).
- [ ] **Step 4: Rewrite `about.html`** (keep `title`, `og_type`, `structured_data` blocks unchanged): hero grid `1fr 240px`, gap 72px, text aligned to photo bottom, photo 4:5 `object-fit: cover; object-position: center 30%`; career ledger rows `140px 230px 1fr`; tint band with two columns (Selected projects, Recent writing, each with section-head and "All →"). Under 720px: photo 160px wide above the credentials line, ledger rows stacked, columns stacked. Page-specific CSS goes in `site.css` under a `.home` body class.
- [ ] **Step 5: Run** `pytest -q`. Expected: PASS (except failures owned by later tasks).
- [ ] **Step 6: Commit** `feat: new homepage with career ledger and selected work`.

### Task 5: Writing pages (blog list, article, archive templates)

**Files:**
- Modify: `themes/Custom/templates/index.html`, `article.html`, `pagination.html`, `archives.html`, `period_archives.html`, `tags.html`, `tag.html`, `categories.html`, `category.html`, `authors.html`, `author.html`, `page.html`
- Create: `themes/Custom/templates/partial/article_list.html` (shared ruled list)
- Modify: `site.css` (fold in `content/extra/custom.css`), `pelicanconf.py` (remove `CUSTOM_CSS` and its `EXTRA_PATH_METADATA` entry)
- Delete: `content/extra/custom.css`, `themes/Custom/templates/partial/disqus.html`
- Test: `tests/test_writing.py`

**Interfaces:**
- Consumes: shared classes (Task 2), `AUTHOR_PHOTO`.
- Produces: `partial/article_list.html` expecting a variable `articles_list` (iterable of articles); renders `ol.ruled-list` items with title link, date · `{{ a.stats.read_mins }} min read`, summary, optional thumbnail (`a.previewimage`, only if set).

- [ ] **Step 1: Write failing tests** in `tests/test_writing.py`:
  - `test_blog_list`: `blog.html` `<h1>` "Writing"; one list item per article (7 today; count `content/articles/*.md`); each shows "min read"; no "Read more" buttons.
  - `test_pagination_links(paginated_site)`: `blog.html` has an "Older" link to `/blog2.html`; `blog2.html` has a "Newer" link back.
  - `test_article_page`: on `a-senior-developer-playbook.html`, `<h1>` equals the article title; meta line contains the date and "min read"; the body container has class `prose` (serif applied via CSS); an author card with `<img src` ending `portrait-600.jpg>` and a link to `/`; a "More writing" section with 2 or 3 links to other articles (not itself); no `disqus` and no `share-bar` in source.
  - `test_code_blocks_styled`: on `avoiding-lost-updates-in-web-applications.html` (has code), a `.highlight pre` exists; `site.css` contains `.prose pre` with `overflow-x: auto`.
  - `test_archive_templates_render`: `tags.html`, `categories.html`, `archives.html`, one `tag/*.html`, one `category/*.html` each contain the nav and at least one article link.
  - `test_custom_css_removed`: no output page references `extra/custom.css`.
- [ ] **Step 2: Run** `pytest tests/test_writing.py -q`. Expected: FAIL.
- [ ] **Step 3: Implement** the list partial and templates per spec (blog heading "Writing" + one-line intro; "← Newer" / "Older →" pagination). Article: title Hanken 600 large; meta muted; `.prose` column max 68ch, Source Serif 4 ~19px / 1.7, headings in Hanken; author card; "More writing" from `articles` excluding current. Keep `meta` and `structured_data` blocks as they are.
- [ ] **Step 4: Fold** the reading styles of `content/extra/custom.css` into `site.css` under `.prose`, re-colored with tokens (drop `#5a67d8` heading bars; h2 gets a top hairline, h3 plain); keep the dark code theme but set its background to ink `#0d1b2a`; remove `CUSTOM_CSS` from config and `base.html`; delete the old file.
- [ ] **Step 5: Run** `pytest -q`. Expected: PASS for this task's tests and all earlier ones.
- [ ] **Step 6: Commit** `feat: restyle blog, articles and archive pages`.

### Task 6: Project detail pages

**Files:**
- Modify: `themes/Custom/templates/project_detail.html`, `site.css`
- Test: `tests/test_project_detail.py`

**Interfaces:**
- Consumes: page metadata `title`, `summary`, `technologies` (comma string), `images` (comma string, may be empty, uses `\` separators in some files), `website`, `repository` (both optional).

- [ ] **Step 1: Write failing tests**:
  - `test_project_detail_header`: `projects/a320expert.html` `<h1>` "A320 Expert"; summary text present; technologies rendered as text "python · django · vuejs · postgresql · stripe · digitalocean"; a link to `https://a320expert.com/`.
  - `test_project_images_stacked`: same page has 4 `<img>` in the content column, `src` using forward slashes, all resolving (covered by the link test); no `carousel` in source; no `webdev-icons` in source.
  - `test_project_without_images`: `projects/iotorq-exporter.html` renders with no `<img>` in the content column and no empty link for missing `website`/`repository`.
- [ ] **Step 2: Run**, expect FAIL.
- [ ] **Step 3: Implement**: header (name, summary, technologies text, website/repository links if set); images stacked full content width with 4px radius, first one as lead; normalize `\` to `/` in image paths with Jinja `replace('\\', '/')`; skip empty entries.
- [ ] **Step 4: Run** `pytest -q`, expect PASS.
- [ ] **Step 5: Commit** `feat: restyle project detail pages`.

### Task 7: Resume page and llms.txt

**Files:**
- Modify: `themes/Custom/templates/resume.html`, `site.css`, `content/llms.txt`
- Test: `tests/test_resume.py`

- [ ] **Step 1: Write failing tests**:
  - `test_resume_sections`: `resume.html` has an `<h1>` with the author name and headings for Experience, Education, Certifications, Skills, Awards (match the existing section names exactly; read them first); experience rows include "Chief Technology Officer" and "Jan 2022 - Present" text (keep current wording).
  - `test_resume_no_email_no_pdf`: no `gmail`, no `@` email text, no `.pdf` link.
  - `test_llms_txt_no_pdf`: `llms.txt` does not contain `resume_tartieret.pdf`.
- [ ] **Step 2: Run**, expect FAIL.
- [ ] **Step 3: Implement**: same content, ledger style (years column | role + company | description and bullets), ruled sections with `.section-head`; header with name, title, LinkedIn/GitHub links; technologies as muted " · " text; `@media print` rules (hide nav/footer, black text, no tint). Remove the PDF line from `llms.txt`.
- [ ] **Step 4: Run** `pytest -q`, expect PASS (including `test_no_mailto_or_pdf_resume` from Task 1).
- [ ] **Step 5: Commit** `feat: restyle resume, drop email and PDF link`.

### Task 8: Contact page

**Files:**
- Modify: `themes/Custom/templates/contact.html`, `site.css`
- Test: `tests/test_contact.py`

- [ ] **Step 1: Write failing tests**:
  - `test_contact_form`: form `method=post`, `action` equals `pelicanconf.EMAIL_ACTION`; inputs `name` (required), `_replyto` type email (required), `message` textarea (required), hidden `_subject` equal to `EMAIL_SUBJECT`, hidden `_gotcha`; each field has a `<label for>`; submit button with class `btn-primary`.
  - `test_contact_links`: a link to the LinkedIn URL from `SOCIAL`; no `mailto:`.
- [ ] **Step 2: Run**, expect FAIL.
- [ ] **Step 3: Implement**: heading, one-line intro, form (1px `--border` inputs, 4px radius, `padding: 12px 14px`, accent focus ring) beside a short column with photo-free text and the LinkedIn link; stacks under 720px.
- [ ] **Step 4: Run** `pytest -q`, expect PASS.
- [ ] **Step 5: Commit** `feat: restyle contact page`.

### Task 9: Cleanup and visual verification

**Files:**
- Delete: `themes/Custom/static/css/resume.css`, `base_theme.css`, `custom_theme.css`, `themes/Custom/static/js/` (all except `projects-filter.js`), unused `static/css/pygments/*` (keep none; Pygments CSS lives in `site.css`), `themes/Custom/templates/gosquared.html` if unreferenced, skill icons `content/images/*-icon.svg` and `content/images/webdev-icons/` if no template or content references them (grep first), old `content/images/profile.png` only if unreferenced.
- Test: `tests/test_cleanup.py`

- [ ] **Step 1: Write test** `test_no_unused_theme_assets`: the deleted theme files above do not exist in the output `theme/` dir.
- [ ] **Step 2: Delete** the files (grep `content/` and `themes/` for each before deleting); run `pytest -q`, expect all PASS.
- [ ] **Step 3: Visual check** with Playwright against `make html` output served by `make serve PORT=8000`: screenshot home, blog, one article with code, projects (click a filter), one project detail, resume, contact, one tag page at 1280px and 375px. On every page at 375px assert `document.documentElement.scrollWidth <= window.innerWidth`. Open the mobile `<details>` nav and confirm links show. Compare home with the approved mockup (`.superpowers/brainstorm/55777-1794261954/content/mix-v4.html`).
- [ ] **Step 4: Contrast check**: confirm body `#445063`, muted `#556070` and accent `#0b5563` on `#ffffff` and `#f6f8f9` meet WCAG AA (4.5:1) with a quick computation; adjust nothing unless one fails.
- [ ] **Step 5: Full build** `make html` and `make publish` with no errors; `pytest -q` all PASS.
- [ ] **Step 6: Commit** `chore: remove legacy theme assets`.
