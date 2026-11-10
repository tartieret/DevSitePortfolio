"""Netlify builds with publishconf.py. Deploy previews must reference their own assets."""
from conftest import build, page

PREVIEW = "https://deploy-preview-21--thomastartiere.netlify.app"


def stylesheet(soup):
    return next(l["href"] for l in soup.find_all("link", rel="stylesheet") if l["href"].endswith("site.css"))


def test_deploy_preview_uses_its_own_url(tmp_path):
    out = build(tmp_path, "publishconf.py", env={"CONTEXT": "deploy-preview", "DEPLOY_PRIME_URL": PREVIEW})
    soup = page(out, "index.html")
    assert stylesheet(soup) == f"{PREVIEW}/theme/css/site.css"
    assert soup.select_one(".hero-photo")["src"].startswith(PREVIEW)


def test_branch_deploy_uses_its_own_url(tmp_path):
    url = "https://site-redesign--thomastartiere.netlify.app"
    out = build(tmp_path, "publishconf.py", env={"CONTEXT": "branch-deploy", "DEPLOY_PRIME_URL": url})
    assert stylesheet(page(out, "index.html")) == f"{url}/theme/css/site.css"


def test_production_keeps_the_real_domain(tmp_path):
    out = build(tmp_path, "publishconf.py", env={"CONTEXT": "production", "DEPLOY_PRIME_URL": PREVIEW})
    soup = page(out, "index.html")
    assert stylesheet(soup) == "https://thomastartiere.com/theme/css/site.css"
    assert soup.find("link", rel="canonical")["href"] == "https://thomastartiere.com/"
