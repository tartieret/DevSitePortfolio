import re

from conftest import page

SECTIONS = ["Summary", "Work Experience", "Education", "Certifications", "Core Skills", "Languages", "Awards", "Interests"]


def test_resume_sections(site):
    soup = page(site, "resume.html")
    assert soup.find("h1").get_text(strip=True) == "Thomas Tartière"
    headings = [h.get_text(strip=True) for h in soup.select("main .section-head h2")]
    assert headings == SECTIONS
    jobs = soup.select(".resume-job")
    assert len(jobs) == 4
    first = jobs[0].get_text(" ", strip=True)
    assert "Chief Technology Officer" in first and "Jan 2022 - Present" in first and "SOC 2 Type II" in first
    assert "Ecole Centrale Paris" in jobs[3].get_text()


def test_resume_tech_is_text(site):
    soup = page(site, "resume.html")
    assert not soup.select("[class*=badge]")
    tech = soup.select(".resume-job .resume-tech")
    assert tech and "Python · Django · Azure" in tech[0].get_text(strip=True)


def test_resume_no_email_phone_or_pdf(site):
    source = (site / "resume.html").read_text(encoding="utf-8")
    assert "gmail" not in source
    assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", page(site, "resume.html").get_text())
    assert "604" not in source
    assert ".pdf" not in source
    assert "resume.css" not in source


def test_resume_print_styles(site):
    css = (site / "theme" / "css" / "site.css").read_text()
    assert "@media print" in css


def test_llms_txt_no_pdf(site):
    assert "resume_tartieret.pdf" not in (site / "llms.txt").read_text(encoding="utf-8")
