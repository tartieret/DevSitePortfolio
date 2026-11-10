from pathlib import Path

import pytest

import pelicanconf
from conftest import page

PAGES = [
    "index.html",
    "blog.html",
    "resume.html",
    "projects.html",
    "contact.html",
    "projects/a320expert.html",
    "a-senior-developer-playbook.html",
]

NAV = {"/blog.html": "Writing", "/projects.html": "Projects", "/resume.html": "Resume", "/contact.html": "Contact"}
CURRENT = {"blog.html": "/blog.html", "projects.html": "/projects.html", "resume.html": "/resume.html", "contact.html": "/contact.html"}

LEGACY = ("bootstrap", "jquery", "fontawesome", "font-awesome", "isotope", "share-bar", "Roboto", "3rdwavemedia")


@pytest.mark.parametrize("rel", PAGES)
def test_no_legacy_assets(site, rel):
    source = (site / rel).read_text(encoding="utf-8")
    found = [needle for needle in LEGACY if needle.lower() in source.lower()]
    assert not found, f"{rel} still references {found}"


@pytest.mark.parametrize("rel", PAGES)
def test_nav(site, rel):
    nav = page(site, rel).find("nav")
    assert nav is not None
    links = {a["href"]: a.get_text(strip=True) for a in nav.find_all("a")}
    for href, text in NAV.items():
        assert links.get(href) == text, f"{rel}: nav link {href} -> {links.get(href)!r}"
    assert links.get("/") == pelicanconf.AUTHOR
    if rel in CURRENT:
        current = nav.find("a", attrs={"aria-current": "page"})
        assert current is not None and current["href"] == CURRENT[rel]


@pytest.mark.parametrize("rel", PAGES)
def test_fonts_and_css(site, rel):
    soup = page(site, rel)
    hrefs = [link.get("href", "") for link in soup.find_all("link", rel="stylesheet")]
    assert any("Hanken+Grotesk" in h for h in hrefs)
    assert any(h.endswith("theme/css/site.css") for h in hrefs)


@pytest.mark.parametrize("rel", PAGES)
def test_footer(site, rel):
    footer = page(site, rel).find("footer")
    assert footer is not None
    for name, url in pelicanconf.SOCIAL:
        link = footer.find("a", href=url)
        assert link is not None, f"missing footer link {name}"
        assert link.find("svg") is not None
        assert link.get("aria-label")
    assert "Thomas Tartière" in footer.get_text()


def test_favicon_and_theme_color(site):
    soup = page(site, "index.html")
    assert soup.find("link", rel="icon", type="image/svg+xml") is not None
    assert soup.find("meta", attrs={"name": "theme-color"})["content"] == "#0d1b2a"
    assert soup.find("meta", property="og:image")["content"].endswith("/images/portrait.jpg")


@pytest.mark.parametrize("rel", PAGES)
def test_skip_link(site, rel):
    soup = page(site, rel)
    first_link = soup.body.find("a")
    assert first_link["href"] == "#main" and "skip" in first_link.get("class", [])
    assert soup.find("main", id="main") is not None


@pytest.mark.parametrize(
    "rel,href,expected",
    [
        ("projects.html", "/projects.html", "page"),
        ("blog.html", "/blog.html", "page"),
        ("projects/a320expert.html", "/projects.html", "true"),
        ("a-senior-developer-playbook.html", "/blog.html", "true"),
        ("tag/django.html", "/blog.html", "true"),
    ],
)
def test_aria_current_distinguishes_child_pages(site, rel, href, expected):
    link = page(site, rel).find("nav").find("a", href=href, attrs={"aria-current": True})
    assert link is not None and link["aria-current"] == expected


def test_mobile_menu_script(site):
    soup = page(site, "index.html")
    assert soup.find("script", src=lambda s: s and s.endswith("theme/js/nav.js"))
    script = (site / "theme" / "js" / "nav.js").read_text()
    assert "Escape" in script and "click" in script


def test_print_wraps_code():
    css = (Path(__file__).resolve().parent.parent / "themes/Custom/static/css/site.css").read_text()
    print_block = css[css.index("@media print"):]
    assert ".prose pre code" in print_block and "pre-wrap" in print_block
