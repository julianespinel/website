#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import toml
import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# Load non-secrets from file
public = toml.load('public.toml')

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = public['website']['url']
WEBSITE_VERSION = public['website']['version']

RELATIVE_URLS = True

FEED_ALL_ATOM = 'feeds/all.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Load secrets from file
secrets = toml.load('secrets.toml')
GOOGLE_ANALYTICS = secrets['website']['google_analytics']
