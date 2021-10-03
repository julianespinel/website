#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Julian Espinel'
SITENAME = 'jespinel.com'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins']
PLUGINS = ['sort_by_article_count', 'sitemap']

SITEMAP = {
    "format": "xml"
}

STATIC_PATHS = ['extra/robots.txt']

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'}
}

GOOGLE_ANALYTICS = ""
WEBSITE_VERSION = "x.y.z"
