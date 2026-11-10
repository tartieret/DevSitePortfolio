import re
from urllib.parse import urlsplit

import pytest

from conftest import all_html, json_ld, page

ARTICLE = "a-senior-developer-playbook.html"


def meta(soup, **attrs):
    tag = soup.find("meta", attrs=attrs)
    assert tag is not None, f"missing meta {attrs}"
    return tag["content"]


def test_homepage_seo(site):
    soup = page(site, "index.html")
    assert soup.find("link", rel="canonical") is not None
    assert meta(soup, property="og:title")
    assert meta(soup, property="og:description")
    assert meta(soup, property="og:image")
    assert meta(soup, name="twitter:card") == "summary_large_image"
    types = {node["@type"] for node in json_ld(soup)}
    assert {"Person", "WebSite"} <= types
    assert soup.find("script", src=lambda s: s and "googletagmanager.com/gtag/js?id=G-PPQKSCH1B2" in s)


def test_article_seo(site):
    soup = page(site, ARTICLE)
    assert soup.find("link", rel="canonical") is not None
    assert meta(soup, property="og:type") == "article"
    posts = [n for n in json_ld(soup) if n["@type"] == "BlogPosting"]
    assert posts and posts[0]["headline"]


def test_sitemap_and_robots(site):
    for name in ("sitemap.xml", "robots.txt", "llms.txt"):
        assert (site / name).exists(), name
    sitemap = (site / "sitemap.xml").read_text()
    assert "/resume</loc>" in sitemap
    assert "/projects</loc>" in sitemap
    assert "/blog</loc>" in sitemap
    assert ".html</loc>" not in sitemap
    assert "_redirects" not in sitemap


def test_publish_build_absolute_urls(publish_site):
    for rel in ("index.html", ARTICLE):
        soup = page(publish_site, rel)
        assert soup.find("link", rel="canonical")["href"].startswith("https://thomastartiere.com")
        assert not soup.find("link", rel="canonical")["href"].endswith(".html")
        assert meta(soup, property="og:url").startswith("https://thomastartiere.com")
    assert page(publish_site, "index.html").find("link", type="application/atom+xml") is not None


# One URL per page: links, canonicals, sitemap, feeds and llms.txt all use the
# extensionless form that Netlify serves, and _redirects retires the .html form.


@pytest.mark.parametrize(
    "rel,canonical",
    [
        ("index.html", "https://thomastartiere.com/"),
        ("resume.html", "https://thomastartiere.com/resume"),
        ("blog.html", "https://thomastartiere.com/blog"),
        ("projects/iotorq.html", "https://thomastartiere.com/projects/iotorq"),
        (ARTICLE, "https://thomastartiere.com/a-senior-developer-playbook"),
    ],
)
def test_canonical_urls_are_extensionless(publish_site, rel, canonical):
    soup = page(publish_site, rel)
    assert soup.find("link", rel="canonical")["href"] == canonical
    assert meta(soup, property="og:url") == canonical


def test_no_internal_links_to_html_pages(publish_site):
    offenders = []
    for html_file in all_html(publish_site):
        soup = page(publish_site, str(html_file.relative_to(publish_site)))
        for a in soup.find_all("a", href=True):
            href = a["href"]
            internal = href.startswith(("/", "https://thomastartiere.com"))
            if internal and urlsplit(href).path.endswith(".html"):
                offenders.append(f"{html_file.relative_to(publish_site)}: {href}")
    assert not offenders, "\n".join(sorted(set(offenders)))


def test_llms_txt_and_feed_use_clean_urls(publish_site):
    for name in ("llms.txt", "feeds/all.atom.xml"):
        text = (publish_site / name).read_text()
        assert not re.findall(r"https://thomastartiere\.com/[^\s\"<>)]*\.html", text), name


def test_redirects_retire_html_urls(publish_site):
    rules = {
        tuple(line.split()[:2]): line.split()[2]
        for line in (publish_site / "_redirects").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }
    assert rules[("/resume.html", "/resume")] == "301!"
    assert rules[("/projects/iotorq.html", "/projects/iotorq")] == "301!"
    assert rules[("/a-senior-developer-playbook.html", "/a-senior-developer-playbook")] == "301!"
    assert rules[("/blog.html", "/blog")] == "301!"
    assert rules[("/docs/resume_tartieret.pdf", "/resume")] == "301"
    assert not (publish_site / "docs" / "resume_tartieret.pdf").exists()


def test_machine_files_are_not_indexed(publish_site):
    headers = (publish_site / "_headers").read_text()
    for path in ("/sitemap.xml", "/llms.txt", "/feeds/*"):
        assert f"{path}\n  X-Robots-Tag: noindex" in headers


@pytest.mark.parametrize("rel", ["tags.html", "categories.html", "archives.html", "authors.html", "tag/django.html", "category/ai.html", "author/thomas-tartiere.html"])
def test_listing_pages_are_noindex(site, rel):
    assert meta(page(site, rel), name="robots") == "noindex, follow"


@pytest.mark.parametrize("rel", ["index.html", "blog.html", "resume.html", "projects/iotorq.html", ARTICLE])
def test_content_pages_are_indexable(site, rel):
    assert meta(page(site, rel), name="robots") == "index, follow"


def test_homepage_description_fits_search_results(site):
    assert len(meta(page(site, "index.html"), name="description")) <= 155


def test_person_structured_data(publish_site):
    nodes = {n["@type"]: n for n in json_ld(page(publish_site, "index.html"))}
    person = nodes["Person"]
    assert person["worksFor"]["url"] == "https://panevo.com/"
    assert person["homeLocation"]["name"].startswith("Vancouver")
    assert "P.Eng." in person["hasCredential"]["name"]
    assert {a["name"] for a in person["alumniOf"]} == {"Stanford University", "Ecole Centrale Paris"}
    assert nodes["ProfilePage"]["mainEntity"]["@id"] == person["@id"]
    assert nodes["WebSite"]["name"] == "Thomas Tartière"


def test_other_pages_structured_data(publish_site):
    resume = json_ld(page(publish_site, "resume.html"))
    assert resume[0]["mainEntity"]["@id"] == "https://thomastartiere.com/#person"

    project = {n["@type"]: n for n in json_ld(page(publish_site, "projects/iotorq.html"))}
    assert project["CreativeWork"]["url"] == "https://thomastartiere.com/projects/iotorq"
    assert "Django" in project["CreativeWork"]["keywords"]
    crumbs = [i["item"] for i in project["BreadcrumbList"]["itemListElement"]]
    assert crumbs == ["https://thomastartiere.com/projects", "https://thomastartiere.com/projects/iotorq"]

    blog = json_ld(page(publish_site, "blog.html"))[0]
    assert blog["@type"] == "Blog" and blog["blogPost"]
    assert all(not p["url"].endswith(".html") for p in blog["blogPost"])
    assert not json_ld(page(publish_site, "tag/django.html"))


def test_pages_have_recent_lastmod(site):
    sitemap = (site / "sitemap.xml").read_text()
    entries = dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sitemap))
    stale = [loc for loc, lastmod in entries.items() if "/projects" in loc or loc.endswith(("/resume", "/contact")) if lastmod < "2026"]
    assert not stale, stale


def test_single_h1_per_page(site):
    multiple = [str(f.relative_to(site)) for f in all_html(site) if len(page(site, str(f.relative_to(site))).find_all("h1")) != 1]
    assert not multiple, multiple
