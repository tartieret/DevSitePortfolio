import pelicanconf
from conftest import page


def projects_soup(site):
    return page(site, "projects.html")


def test_project_grid(site):
    entries = projects_soup(site).select("article.project")
    assert len(entries) == len(pelicanconf.PROJECTS)
    for entry, project in zip(entries, pelicanconf.PROJECTS):
        assert entry.find("img")["src"].endswith(project["thumb"])
        assert entry.find("img").get("alt")
        heading = entry.find("h2")
        assert heading.get_text(strip=True) == project["title"]
        assert heading.find("a")["href"] == f"/projects/{project['slug']}.html"
        assert entry.select_one(".project-tech").get_text(strip=True) == " · ".join(project["technologies"])


def test_project_filters_markup(site):
    soup = projects_soup(site)
    buttons = soup.select("button[data-filter]")
    labels = [b.get_text(strip=True) for b in buttons]
    assert labels == ["All"] + [label for _, label in pelicanconf.PROJECT_FILTERS]
    assert all(b.get("type") == "button" for b in buttons)
    for entry, project in zip(soup.select("article.project"), pelicanconf.PROJECTS):
        assert entry["data-filters"].split() == project["filters"]
    assert soup.find("script", src=lambda s: s and s.endswith("theme/js/projects-filter.js"))


def test_no_badges(site):
    soup = projects_soup(site)
    assert not soup.select("[class*=badge]")


def test_project_data_is_valid():
    keys = {key for key, _ in pelicanconf.PROJECT_FILTERS}
    slugs = [p["slug"] for p in pelicanconf.PROJECTS]
    assert len(slugs) == len(set(slugs))
    for project in pelicanconf.PROJECTS:
        assert set(project["filters"]) <= keys, project["slug"]
        assert project["summary"] and not project["summary"].endswith("!")


def test_peak_alert_removed(site):
    assert "Peak Alert" not in (site / "projects.html").read_text(encoding="utf-8")
    assert all(p["slug"] for p in pelicanconf.PROJECTS)
