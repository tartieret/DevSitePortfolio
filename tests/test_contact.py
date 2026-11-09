import pelicanconf
from conftest import page


def contact(site):
    return page(site, "contact.html")


def test_contact_form(site):
    form = contact(site).find("form")
    assert form["method"].lower() == "post"
    assert form["action"] == pelicanconf.EMAIL_ACTION
    name = form.find("input", attrs={"name": "name"})
    email = form.find("input", attrs={"name": "_replyto"})
    message = form.find("textarea", attrs={"name": "message"})
    assert name.has_attr("required") and email.has_attr("required") and message.has_attr("required")
    assert email["type"] == "email"
    for field in (name, email, message):
        label = form.find("label", attrs={"for": field["id"]})
        assert label is not None and label.get_text(strip=True)
    assert form.find("input", attrs={"name": "_subject"})["value"] == pelicanconf.EMAIL_SUBJECT
    assert form.find("input", attrs={"name": "_gotcha"}) is not None
    assert "btn-primary" in form.find("button", type="submit")["class"]


def test_contact_links(site):
    soup = contact(site)
    linkedin = dict(pelicanconf.SOCIAL)["linkedin"]
    assert soup.find("main").find("a", href=linkedin) is not None
    assert "mailto:" not in (site / "contact.html").read_text(encoding="utf-8")
    assert soup.find("h1").get_text(strip=True) == "Contact"


def test_honeypot_not_rendered(site):
    honeypot = contact(site).find("input", attrs={"name": "_gotcha"})
    assert honeypot.has_attr("hidden") or "display:none" in honeypot.get("style", "").replace(" ", "")
