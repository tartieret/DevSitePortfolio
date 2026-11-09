import re
from datetime import datetime

import pelicanconf
from conftest import ROOT, json_ld, page

HEADLINE = "I build and scale data-intensive platforms for industrial and enterprise applications."


def home(site):
    return page(site, "index.html")


def latest_articles(n=3):
    articles = []
    for path in (ROOT / "content" / "articles").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        title = re.search(r"^Title:\s*(.+)$", text, re.M).group(1).strip()
        date = datetime.strptime(re.search(r"^Date:\s*(.+)$", text, re.M).group(1).strip(), "%Y-%m-%d %H:%M")
        articles.append((date, title))
    return sorted(articles, reverse=True)[:n]


def test_hero(site):
    soup = home(site)
    h1s = soup.find_all("h1")
    assert len(h1s) == 1 and h1s[0].get_text(strip=True) == HEADLINE
    hero = soup.select_one(".hero")
    assert hero.select_one(".hero-intro").get_text(strip=True).startswith("Over 14 years in software and systems engineering")
    assert hero.select_one(".credentials").get_text(" ", strip=True) == "CTO, Panevo · P.Eng. · Vancouver"
    photo = hero.find("img")
    assert photo["src"].endswith("portrait-600.jpg") and photo.get("alt")
    buttons = {a["href"]: a.get_text(strip=True) for a in hero.select("a.btn")}
    assert buttons == {"/resume.html": "View resume", "/projects.html": "Selected projects"}


def test_career_ledger(site):
    section = home(site).select_one("section.career")
    head = section.select_one(".section-head")
    assert head.find("h2").get_text(strip=True) == "Career"
    assert head.find("a")["href"] == "/resume.html"
    rows = section.select(".career-row")
    assert len(rows) == len(pelicanconf.CAREER) == 3
    for row, job in zip(rows, pelicanconf.CAREER):
        assert row.select_one(".career-years").get_text(strip=True) == job["years"]
        assert row.select_one(".career-role").get_text(" ", strip=True) == f"{job['role']} {job['company']}"
        assert row.select_one(".career-summary").get_text(strip=True) == job["summary"]


def test_selected_projects(site):
    links = home(site).select("section.selected-projects li a")
    assert [a["href"] for a in links] == [
        "/projects/iotorq.html",
        "/projects/iotorq-lean.html",
        "/projects/a320expert.html",
    ]
    titles = {p["slug"]: p["title"] for p in pelicanconf.PROJECTS}
    assert [a.find("strong").get_text(strip=True) for a in links] == [titles[s] for s in pelicanconf.SELECTED_PROJECTS]


def test_recent_writing(site):
    items = home(site).select("section.recent-writing li")
    expected = latest_articles()
    assert len(items) == 3
    for item, (date, title) in zip(items, expected):
        assert item.find("strong").get_text(strip=True) == title
        assert date.strftime("%B %Y") in item.get_text(" ", strip=True)


def test_no_skill_cards(site):
    soup = home(site)
    assert "Overview" not in [h.get_text(strip=True) for h in soup.find_all(["h2", "h3"])]
    assert not soup.select("[class*=skills-]")
    person = next(n for n in json_ld(soup) if n["@type"] == "Person")
    assert person["knowsAbout"]
