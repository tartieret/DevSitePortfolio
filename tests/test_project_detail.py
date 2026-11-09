from conftest import page


def test_project_detail_header(site):
    soup = page(site, "projects/a320expert.html")
    head = soup.select_one(".project-head")
    assert head.find("h1").get_text(strip=True) == "A320 Expert"
    assert "B2C training platform for Airbus A320 pilots" in head.get_text()
    assert head.select_one(".project-tech").get_text(strip=True) == "python · django · vuejs · postgresql · stripe · digitalocean"
    assert head.find("a", href="https://a320expert.com/") is not None


def test_project_images_stacked(site):
    soup = page(site, "projects/a320expert.html")
    images = soup.select(".project-images img")
    assert len(images) == 4
    assert all("\\" not in img["src"] and img.get("alt") is not None for img in images)
    source = (site / "projects" / "a320expert.html").read_text(encoding="utf-8")
    assert "carousel" not in source
    assert "webdev-icons" not in source


def test_project_without_images(site):
    soup = page(site, "projects/iotorq-exporter.html")
    assert soup.select_one(".project-images") is None
    head = soup.select_one(".project-head")
    assert all(a.get("href") for a in head.find_all("a"))


def test_repository_link(site):
    head = page(site, "projects/orc-world-map.html").select_one(".project-head")
    assert head.find("a", href="https://github.com/tartieret/ORC-World-Map") is not None
