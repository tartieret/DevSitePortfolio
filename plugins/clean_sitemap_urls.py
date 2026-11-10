"""Strip ".html" from sitemap URLs so they match the site's extensionless URLs.

The sitemap plugin uses each article's and page's own URL (already extensionless,
see ARTICLE_URL in pelicanconf.py), but falls back to the output file name for
index pages such as blog.html. This rewrites those to /blog after the sitemap
is written. List it after "sitemap" in PLUGINS so it runs second.
"""
import os
import re

from pelican import signals


def clean_sitemap(pelican):
    path = os.path.join(pelican.output_path, "sitemap.xml")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fd:
        xml = fd.read()
    xml = re.sub(r"\.html</loc>", "</loc>", xml)
    with open(path, "w", encoding="utf-8") as fd:
        fd.write(xml)


def register():
    signals.finalized.connect(clean_sitemap)
