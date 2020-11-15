"""
This file contains the business logic for the blogs app.
If the business logic grows I will create a folder named `business/`
and then I will create files to separate different business logic,
for example: `posts.py`, `comments.py`, etc.
"""

import glob
import hashlib
import logging
import os
import markdown

from pathlib import Path
from ..models import Post, Category, Tag
from ..business import posts
from django_static_image import DjangoStaticImageExtension

logger = logging.getLogger(__name__)

POSTS_PATH = 'blog/templates/blog/posts/'


def refresh_posts():
    logger.info('refresh_posts start')
    posts_tuples = convert_markdown_files()
    posts.delete_all()
    for post_tuple in posts_tuples:
        post = post_tuple[0]
        categories = post_tuple[1]
        tags = post_tuple[2]
        posts.create(post, categories, tags)
    logger.info('refresh_posts end')


def convert_markdown_files():
    logger.debug('Start process to convert Markdown to HTML')
    directory = 'blog/posts'
    file_extension = '.md'
    markdown_files = __list_files_from(directory, file_extension)
    logger.debug(f'listdir: {os.listdir(".")}')
    logger.debug(f'markdown_files: {markdown_files}')
    markdown_converter = markdown.Markdown(
        extensions=[
            DjangoStaticImageExtension(),
            'meta',
            'tables',
            'pymdownx.tilde',
            'pymdownx.superfences',
        ]
    )
    posts_data = []
    __create_posts_directory_if_needed()
    for md_file in markdown_files:
        metadata = __to_html(markdown_converter, md_file)
        post_data = get_post_data(metadata)
        posts_data.append(post_data)
    logger.debug('End process to convert Markdown to HTML')
    return posts_data


def to_slug(string):
    return string.replace(" ", "-")


def to_category(name):
    return Category(name=to_slug(name))


def to_tag(name):
    return Tag(name=to_slug(name))


def get_post_data(metadata):
    title = metadata['title'][0]
    slug = metadata['slug'][0]
    date = metadata['date'][0]
    checksum = metadata['checksum'][0]
    categories = list(map(to_category, metadata['categories']))
    tags = list(map(to_tag, metadata['tags']))
    post = Post(title=title, slug=slug, date=date, checksum=checksum)
    return post, categories, tags  # tuple


def __list_files_from(directory, file_extension):
    return glob.glob(f'{directory}/*{file_extension}')


def __create_posts_directory_if_needed():
    Path(POSTS_PATH).mkdir(parents=True, exist_ok=True)


def __to_html(converter, markdown_file_path):
    slug = __get_file_name_only(markdown_file_path)
    output_file_name = slug + ".html"
    output_file_path = POSTS_PATH + output_file_name
    logger.debug(f'About to write to: {output_file_path}')
    checksum = __get_file_checksum(markdown_file_path)
    converter.convertFile(input=markdown_file_path,
                          output=output_file_path, encoding='utf-8')
    __add_django_tags(output_file_path)
    logger.debug(f'converted {markdown_file_path} to {output_file_path}')
    converter.Meta['slug'] = [slug]  # A list to be consistent
    converter.Meta['checksum'] = [checksum]  # A list to be consistent
    logger.debug(f'metadata: {converter.Meta}\n')
    return converter.Meta


def __add_django_tags(html_file_path):
    with open(html_file_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        initial_tags = "{% extends 'blog/base.html' %}\n{% load static %}\n\n{% block content %}\n"
        final_tags = "\n{% endblock %}\n"
        modified_contents = initial_tags + content + final_tags
        f.write(modified_contents)
        f.truncate()


def __get_file_name_only(file_path_with_extension):
    name = os.path.basename(file_path_with_extension)
    return os.path.splitext(name)[0]


def __get_file_checksum(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        # Read file in 4KB chunks
        for chunk in iter(lambda: file.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()
