from conftest import ROOT, all_html, page

ARTICLE = "a-senior-developer-playbook.html"
ARTICLE_COUNT = len(list((ROOT / "content" / "articles").glob("*.md")))


def test_blog_list(site):
    soup = page(site, "blog.html")
    assert soup.find("h1").get_text(strip=True) == "Writing"
    items = soup.select("ol.article-list > li")
    assert len(items) == ARTICLE_COUNT
    for item in items:
        assert "min read" in item.get_text()
    assert "Read more" not in soup.get_text()


def test_pagination_links(paginated_site):
    first = page(paginated_site, "blog.html")
    older = first.find("a", string=lambda s: s and "Older" in s)
    assert older is not None and older["href"] == "/blog2.html"
    second = page(paginated_site, "blog2.html")
    newer = second.find("a", string=lambda s: s and "Newer" in s)
    assert newer is not None and newer["href"] == "/blog.html"


def test_article_page(site):
    soup = page(site, ARTICLE)
    title = soup.find("h1").get_text(strip=True)
    assert title == "A Senior Developer Playbook"
    meta = soup.select_one(".article-meta").get_text(" ", strip=True)
    assert "January" in meta and "2026" in meta and "min read" in meta
    assert soup.select_one("div.prose") is not None
    card = soup.select_one(".author-card")
    assert card.find("img")["src"].endswith("portrait-600.jpg")
    assert card.find("a", href="/") is not None
    more = soup.select(".more-writing li a")
    assert 2 <= len(more) <= 3
    assert all(a["href"] != f"/{ARTICLE}" for a in more)
    source = (site / ARTICLE).read_text(encoding="utf-8")
    assert "disqus" not in source.lower() and "share-bar" not in source


def test_code_blocks_styled(site):
    soup = page(site, "avoiding-lost-updates-in-web-applications.html")
    assert soup.select_one(".prose .highlight pre") is not None
    css = (site / "theme" / "css" / "site.css").read_text()
    assert ".prose pre" in css and "overflow-x: auto" in css


def test_archive_templates_render(site):
    tag_page = next((site / "tag").glob("*.html")).relative_to(site)
    category_page = next((site / "category").glob("*.html")).relative_to(site)
    for rel in ("tags.html", "categories.html", "archives.html", str(tag_page), str(category_page)):
        soup = page(site, rel)
        assert soup.find("nav") is not None, rel
        assert soup.find("h1") is not None, rel
        main = soup.find("main")
        assert main.select("a[href$='.html']"), rel


def test_custom_css_removed(site):
    for html_file in all_html(site):
        assert "extra/custom.css" not in html_file.read_text(encoding="utf-8"), html_file
