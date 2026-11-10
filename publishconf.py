#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)

from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = "https://thomastartiere.com"

# Netlify deploy previews and branch deploys are served from their own URL.
# Point SITEURL there so they load their own CSS, images and links instead of
# the live site's. Netlify sets CONTEXT and DEPLOY_PRIME_URL during builds.
if os.environ.get("CONTEXT") in ("deploy-preview", "branch-deploy") and os.environ.get("DEPLOY_PRIME_URL"):
    SITEURL = os.environ["DEPLOY_PRIME_URL"].rstrip("/")
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""
