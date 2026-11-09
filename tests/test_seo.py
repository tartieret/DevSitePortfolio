from conftest import json_ld, page

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
    assert "resume.html" in sitemap
    assert "projects.html" in sitemap


def test_publish_build_absolute_urls(publish_site):
    for rel in ("index.html", ARTICLE):
        soup = page(publish_site, rel)
        assert soup.find("link", rel="canonical")["href"].startswith("https://thomastartiere.com")
        assert meta(soup, property="og:url").startswith("https://thomastartiere.com")
    assert page(publish_site, "index.html").find("link", type="application/atom+xml") is not None
