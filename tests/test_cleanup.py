LEGACY_THEME_FILES = [
    "css/resume.css",
    "css/base_theme.css",
    "css/custom_theme.css",
    "css/pygments",
    "js/main.js",
    "js/isotope-custom.js",
    "js/social-share-bar.js",
    "js/plugins",
]


def test_no_unused_theme_assets(site):
    leftovers = [rel for rel in LEGACY_THEME_FILES if (site / "theme" / rel).exists()]
    assert not leftovers


def test_no_unused_legacy_images(site):
    images = site / "images"
    leftovers = [name for name in ("webdev-icons", "web-icon.svg", "data-icon.svg", "other-skills-icon.svg") if (images / name).exists()]
    assert not leftovers
