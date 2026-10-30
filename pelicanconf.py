#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
from datetime import datetime

# ----------------------------------
# General site settings

AUTHOR = "Thomas Tartière"
SITENAME = "Thomas Tartière's blog"
SITEURL = ""
SITETITLE = AUTHOR
SITESUBTITLE = "Product-minded CTO building data platforms"
SITEDESCRIPTION = (
    "Thomas Tartière is a product-minded CTO who builds and scales "
    "data-intensive platforms for industrial and enterprise applications. "
    "Articles on AI, Django and software engineering, projects and resume."
)
BROWSER_COLOR = "#333"

SITELOGO = "/images/logo.png"
FAVICON = "/images/favicon.png"

AUTHOR_PROFILE_IMAGE = "/images/profile.png"
AUTHOR_JOB_TITLE = "Chief Technology Officer"
AUTHOR_EMPLOYER = "Panevo"
TWITTER_USERNAME = "thomas_tartiere"

INDEX_SAVE_AS = "blog.html"

ROBOTS = "index, follow"

THEME = os.path.join("themes", "Custom")
PATH = "content"
TIMEZONE = "America/Vancouver"

DATE_FORMATS = {
    "en": "%B %d, %Y",
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Resume", "/"),
    ("Articles", "/"),
)

# Social widget
SOCIAL = (
    ("linkedin", "https://www.linkedin.com/in/thomastartiere/"),
    ("github", "https://github.com/tartieret"),
    ("twitter", "https://x.com/thomas_tartiere"),
    ("medium", "https://medium.com/@thomas.tartiere"),
)

CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa",
}

COPYRIGHT_YEAR = 2018
CURRENT_YEAR = datetime.now().year

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ["./pelican-plugins"]
PLUGINS = ["sitemap", "post_stats"]  # 'i18n_subsites']

# JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.6,
        "indexes": 0.6,
        "pages": 0.5,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    },
    # Keep the sitemap focused on real content, not listing pages
    "exclude": [
        r"^author/",
        r"^authors\.html$",
        r"^category/",
        r"^categories\.html$",
        r"^tag/",
        r"^tags\.html$",
        r"^archives\.html$",
        r"^llms\.txt$",
    ],
}

# Markdown summary of the site for AI agents (https://llmstxt.org)
TEMPLATE_PAGES = {"llms.txt": "llms.txt"}

STATIC_PATHS = ["images", "extra", "docs"]

EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": os.path.join("extra", "custom.css")},
    "extra/robots.txt": {"path": "robots.txt"},
}
CUSTOM_CSS = os.path.join("extra", "custom.css")

USE_LESS = True

# DISQUS
DISQUS_SITENAME = "thomastartiere"

# Code Syntax highlighting using Pygments
PYGMENTS_STYLE = "github"
# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {"linenos": "table"}

# Formspree email settings
EMAIL_SUBJECT = "Contact from Thomas Tartiere's blog"
EMAIL_ACTION = "https://formspree.io/thomas.tartiere@gmail.com"

# ----------------------------------
# SKILLS OVERVIEW

SKILLS_OVERVIEW = (
    {
        "title": "Technology & Product Leadership",
        "icon": "/images/web-icon.svg",
        "skills": [
            "Technology strategy",
            "Product leadership",
            "Platform architecture",
            "Team building & mentoring",
            "Security and compliance",
            "Agile delivery and scaling teams",
            "Customer and executive engagement",
            "Business development",
        ],
    },
    {
        "title": "Data Platforms & Software Engineering",
        "icon": "/images/data-icon.svg",
        "skills": [
            "Python, Django",
            "Distributed systems and real-time data pipelines",
            "API design",
            "Databases",
            "Cloud platforms",
            "Data Streaming",
            "Infrastructure as Code",
            "Containers & Orchestration",
                            ],
    },
    {
        "title": "Analytics & Industrial Systems",
        "icon": "/images/other-skills-icon.svg",
        "skills": [
            "Advanced analytics and time-series analysis",
            "Machine learning and optimization",
            "Industrial IoT and manufacturing systems",
            "Energy system modeling",
            "Thermodynamics and heat transfer",
        ],
    },
)
