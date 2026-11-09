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
BROWSER_COLOR = "#0d1b2a"

SITELOGO = "/images/logo.png"
FAVICON = "/images/favicon.svg"

# Full-size portrait for Open Graph and JSON-LD; smaller copy for on-page display
AUTHOR_PROFILE_IMAGE = "/images/portrait.jpg"
AUTHOR_PHOTO = "/images/portrait-600.jpg"
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

# ----------------------------------
# PROJECTS
# Shared by the Projects page and the homepage "Selected projects" list.
# A project with slug None has no detail page and renders without a link.

PROJECT_FILTERS = (
    ("web", "Web"),
    ("data", "Data"),
    ("machine-learning", "Machine Learning"),
    ("energy", "Energy Sciences"),
)

PROJECTS = (
    {
        "slug": "iotorq-lean",
        "title": "ioTORQ LEAN",
        "summary": "A data platform for lean manufacturing and live production monitoring",
        "thumb": "/images/projects/lean-thumb.png",
        "filters": ["web", "data", "machine-learning"],
        "technologies": ["Python/Django", "Kafka", "MS Azure", "B2B"],
    },
    {
        "slug": "iotorq",
        "title": "ioTORQ EMIS",
        "summary": "A data platform for industrial energy management",
        "thumb": "/images/projects/iotorq-saas-thumb.png",
        "filters": ["web", "data", "machine-learning"],
        "technologies": ["Python/Django", "VueJS", "MS Azure", "B2B"],
    },
    {
        "slug": "jetlagcoach",
        "title": "Jet Lag Coach",
        "summary": "A mobile app that builds personalized plans to beat jet lag",
        "thumb": "/images/projects/jetlagcoach-thumb.png",
        "filters": ["web"],
        "technologies": ["TypeScript/VueJS", "Capacitor", "Supabase", "B2C"],
    },
    {
        "slug": "quakeimpact",
        "title": "QuakeImpact",
        "summary": "What a major earthquake does to the Lower Mainland, and for how long",
        "thumb": "/images/projects/quakeimpact-thumb.png",
        "filters": ["web", "data"],
        "technologies": ["Next.js", "TypeScript", "Claude Code", "Codex"],
    },
    {
        "slug": "a320expert",
        "title": "A320 Expert",
        "summary": "A training platform for Airbus A320 pilots",
        "thumb": "/images/projects/a320expert-thumb.png",
        "filters": ["web"],
        "technologies": ["Python/Django", "Digital Ocean", "Stripe", "B2C"],
    },
    {
        "slug": "brick-by-brick",
        "title": "Brick by Brick 2024",
        "summary": "Automating building data classification",
        "thumb": "/images/projects/brick-thumb.png",
        "filters": ["data", "energy", "machine-learning"],
        "technologies": ["Machine Learning", "Time-series"],
    },
    {
        "slug": "orc-world-map",
        "title": "ORC World Map",
        "summary": "The first complete database of ORC projects, giving an overview of the market",
        "thumb": "/images/projects/orc-thumb.png",
        "filters": ["web", "data", "energy"],
        "technologies": ["VueJS", "Python", "Google Map API"],
    },
    {
        "slug": "iotorq-exporter",
        "title": "ioTORQ Data Exporter",
        "summary": "ETL software to stream data out of industrial facilities",
        "thumb": "/images/projects/iotorq-etl-thumb.png",
        "filters": ["data", "web"],
        "technologies": ["Python", "Desktop", "Qt"],
    },
    {
        "slug": "breed-detector",
        "title": "Dog Breed Detector",
        "summary": "Using transfer learning to classify dog breeds in images",
        "thumb": "/images/projects/dogbreed-thumb.png",
        "filters": ["machine-learning"],
        "technologies": ["Python", "Keras", "Flask", "Transfer Learning"],
    },
    {
        "slug": "behavioral-cloning",
        "title": "Self-Driving Car: Behavioural Cloning",
        "summary": "Training a neural network to drive a car in a simulator",
        "thumb": "/images/projects/cloning-thumb.png",
        "filters": ["machine-learning"],
        "technologies": ["Deep Learning", "Keras"],
    },
    {
        "slug": "lane-finding",
        "title": "Self-Driving Car: Lane Finding",
        "summary": "Identifying lane boundaries in video from a front-facing car camera",
        "thumb": "/images/projects/lanes-thumb.png",
        "filters": ["machine-learning"],
        "technologies": ["Deep Learning", "Keras", "OpenCV"],
    },
    {
        "slug": "vehicle-detection",
        "title": "Vehicle Detection",
        "summary": "A vehicle detection system for self-driving cars",
        "thumb": "/images/projects/vehicle-thumb.png",
        "filters": ["machine-learning"],
        "technologies": ["Python", "Keras", "OpenCV"],
    },
    {
        "slug": "sanfrancisco",
        "title": "San Francisco Incidents",
        "summary": "Analyzing criminal incidents in San Francisco using real data from summer 2014",
        "thumb": "/images/projects/sanfrancisco-thumb.png",
        "filters": ["data"],
        "technologies": ["Python", "Pandas", "Matplotlib"],
    },
    {
        "slug": "seleco2",
        "title": "SeleCO2",
        "summary": "Large-scale thermo-electric energy storage using ground heat exchangers (R&D project)",
        "thumb": "/images/projects/seleco2-thumb.png",
        "filters": ["energy"],
        "technologies": ["Python", "C++", "R&D"],
    },
    {
        "slug": None,
        "title": "Peak Alert",
        "summary": "SMS alerts for electricity peaks in Ontario",
        "thumb": "/images/projects/peakalert-thumb.png",
        "filters": ["web"],
        "technologies": ["Python", "Twilio", "Azure Function"],
    },
)

_slugs = [p["slug"] for p in PROJECTS if p["slug"]]
assert len(_slugs) == len(set(_slugs)), "duplicate project slug"
