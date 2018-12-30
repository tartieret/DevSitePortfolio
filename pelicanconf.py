#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

# ----------------------------------
# General site settings

AUTHOR = 'Thomas Tartière'
SITENAME = "Thomas Tartière's blog"
SITEURL = ''
SITETITLE = AUTHOR
SITESUBTITLE = 'Full stack developper and machine learning engineer'
SITEDESCRIPTION = 'Thoughts and Writings'
BROWSER_COLOR = '#333'

SITELOGO = '/images/logo.png'
FAVICON = '/images/favicon.png'

AUTHOR_PROFILE_IMAGE = '/images/profile.png'

INDEX_SAVE_AS = 'blog.html'

ROBOTS = 'index, follow'

THEME = os.path.join('themes', 'Custom')
PATH = 'content'
TIMEZONE = 'America/Vancouver'

I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'en'
OG_LOCALE = 'en_US'
LOCALE = 'en_US'

DATE_FORMATS = {
    'en': '%B %d, %Y',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Resume', '/'),
    ('Articles', '/'),
)

# Social widget
SOCIAL = (
    ('linkedin', 'https://www.linkedin.com/in/thomastartiere/'),
    ('github', 'https://github.com/tartieret'),
    ('twitter', 'https://twitter.com/thomas_tartiere'),
    ('medium', 'https://medium.com/@thomas.tartiere'),
)

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}

COPYRIGHT_YEAR = 2018

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', 'post_stats']# 'i18n_subsites']

# JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}

STATIC_PATHS = ['images', 'extra']

EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': os.path.join('extra', 'custom.css')},
}
CUSTOM_CSS = os.path.join('extra', 'custom.css')

USE_LESS = True

# DISQUS
DISQUS_SITENAME = "thomastartiere"

# Code Syntax highlighting using Pygments
PYGMENTS_STYLE = 'github'
# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# Formspree email settings
EMAIL_SUBJECT = "Contact from Thomas Tartiere's blog"
EMAIL_ACTION = "https://formspree.io/thomas.tartiere@gmail.com"

# ----------------------------------
# SKILLS OVERVIEW

SKILLS_OVERVIEW = (
    {
        'title': 'Web Development',
        'icon': '/images/web-icon.svg',
        'skills': ['Python/Django', 'MS SQL/PostgreSQL', 'Microsoft Azure', 'VueJS', 'HTML/CSS/SASS', 'Docker']
    },
    {
        'title': 'Data Science',
        'icon': '/images/data-icon.svg',
        'skills': ['Data visualization', 'Machine Learning', 'Deep learning', 'Time-serie Analysis']
    },
    {
        'title': 'Other',
        'icon': '/images/other-skills-icon.svg',
        'skills': ['Project Management','Product Development', 'Business Development', 'Numerical Simulation',  'Renewable Energy', ]
    },
)