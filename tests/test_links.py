from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from conftest import all_html, page

SITEURL = "https://thomastartiere.com"


def internal_targets(soup):
    for tag, attr in (("a", "href"), ("link", "href"), ("img", "src"), ("script", "src")):
        for el in soup.find_all(tag):
            value = el.get(attr)
            if value is None:
                continue
            yield value


def resolve(site: Path, html_file: Path, url: str) -> Path | None:
    """Return the file a site-internal URL points to, or None if the URL is external."""
    if url.startswith(SITEURL):
        url = url[len(SITEURL):] or "/"
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    if not parts.path:
        return None
    # Resolve like a browser would (".." never climbs above the site root).
    page_url = "http://site/" + html_file.relative_to(site).as_posix()
    path = unquote(urlsplit(urljoin(page_url, url)).path)
    target = site / path.lstrip("/")
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


import pytest


@pytest.mark.parametrize("build_name", ["site", "publish_site"])
def test_internal_links_resolve(build_name, request):
    site = request.getfixturevalue(build_name)
    broken = []
    for html_file in all_html(site):
        soup = page(site, str(html_file.relative_to(site)))
        for url in internal_targets(soup):
            if "\\" in url:
                broken.append(f"{html_file.relative_to(site)}: backslash in {url}")
                continue
            target = resolve(site, html_file, url)
            if target is not None and not target.exists():
                broken.append(f"{html_file.relative_to(site)}: {url}")
    assert not broken, "\n".join(sorted(set(broken)))


def test_no_empty_images_or_links(site):
    problems = []
    for html_file in all_html(site):
        soup = page(site, str(html_file.relative_to(site)))
        rel = html_file.relative_to(site)
        for img in soup.find_all("img"):
            src = (img.get("src") or "").strip()
            if not src or src.endswith("/"):
                problems.append(f"{rel}: img src={src!r}")
        for a in soup.find_all("a"):
            if a.has_attr("href") and not a["href"].strip():
                problems.append(f"{rel}: empty href ({a.get_text(strip=True)!r})")
    assert not problems, "\n".join(problems)


def test_no_mailto_or_pdf_resume(site):
    offenders = []
    for html_file in all_html(site):
        text = html_file.read_text(encoding="utf-8")
        for needle in ("mailto:", "resume_tartieret.pdf"):
            if needle in text:
                offenders.append(f"{html_file.relative_to(site)}: {needle}")
    assert not offenders, "\n".join(offenders)
