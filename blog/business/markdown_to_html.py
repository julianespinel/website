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
from django_static_image import DjangoStaticImageExtension
from pathlib import Path

from ..models import Post

logger = logging.getLogger(__name__)

POSTS_PATH = 'blog/templates/blog/posts/'


def get_posts():
    posts = Post.objects.order_by('-date')
    (new_posts, updated_posts) = get_new_and_updated(posts)
    Post.objects.bulk_create(new_posts)
    Post.objects.bulk_update(updated_posts, ['checksum'])
    return Post.objects.order_by('-date')


def get_by_category(category):
    return Post.objects.filter(categories__contains=[category]).order_by('-date')


def get_by_tag(tag):
    return Post.objects.filter(tags__contains=[tag]).order_by('-date')


def get_new_and_updated(posts_from_db):
    from_db_map = get_slug_to_post(posts_from_db)
    posts_from_files = convert_markdown_files()
    from_files_map = get_slug_to_post(posts_from_files)
    new_posts = []
    updated_posts = []
    for slug, post in from_files_map.items():
        db_post = from_db_map.get(slug, None)
        if not db_post:
            new_posts.append(post)
            continue
        if db_post.checksum != post.checksum:
            db_post.checksum = post.checksum
            updated_posts.append(db_post)
    return (new_posts, updated_posts)


def get_slug_to_post(posts):
    dictionary = {}
    for post in posts:
        dictionary[post.slug] = post
    return dictionary


def convert_markdown_files():
    logger.info('Start process to convert Markdown to HTML')
    directory = 'blog/posts'
    file_extension = '.md'
    markdown_files = __list_files_from(directory, file_extension)
    logger.info(f'listdir: {os.listdir(".")}')
    logger.info(f'markdown_files: {markdown_files}')
    markdown_converter = markdown.Markdown(
        extensions=[
            DjangoStaticImageExtension(),
            'meta',
            'tables',
            'pymdownx.tilde',
            'pymdownx.superfences',
        ]
    )
    posts = []
    __create_posts_directory_if_needed()
    for md_file in markdown_files:
        metadata = __to_html(markdown_converter, md_file)
        post = get_post(metadata)
        posts.append(post)
    logger.info('End process to convert Markdown to HTML')
    return posts


def to_slug(string):
    return string.replace(" ", "-")


def get_post(metadata):
    title = metadata['title'][0]
    slug = metadata['slug'][0]
    date = metadata['date'][0]
    checksum = metadata['checksum'][0]
    categories = list(map(to_slug, metadata['categories']))
    tags = list(map(to_slug, metadata['tags']))
    return Post(title=title, slug=slug, date=date, checksum=checksum,
                categories=categories, tags=tags)


def get_categories_frequency(posts):
    categories_frequency = {}
    for post in posts:
        categories = post.categories
        for category in categories:
            occurrences = categories_frequency.get(category, 0)
            categories_frequency[category] = occurrences + 1
    return categories_frequency


def get_tags_frequency(posts):
    tags_frequency = {}
    for post in posts:
        tags = post.tags
        for tag in tags:
            occurrences = tags_frequency.get(tag, 0)
            tags_frequency[tag] = occurrences + 1
    return tags_frequency


def __list_files_from(directory, file_extension):
    return glob.glob(f'{directory}/*{file_extension}')


def __create_posts_directory_if_needed():
    Path(POSTS_PATH).mkdir(parents=True, exist_ok=True)


def __to_html(converter, markdown_file_path):
    slug = __get_file_name_only(markdown_file_path)
    output_file_name = slug + ".html"
    output_file_path = POSTS_PATH + output_file_name
    logger.info(f'About to write to: {output_file_path}')
    checksum = __get_file_checksum(markdown_file_path)
    converter.convertFile(input=markdown_file_path,
                          output=output_file_path, encoding='utf-8')
    __add_django_tags(output_file_path)
    logger.info(f'converted {markdown_file_path} to {output_file_path}')
    converter.Meta['slug'] = [slug]  # A list to be consistent
    converter.Meta['checksum'] = [checksum]  # A list to be consistent
    logger.info(f'metadata: {converter.Meta}\n')
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
