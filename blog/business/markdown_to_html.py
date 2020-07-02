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
from ..models import Post
from django_static_image import DjangoStaticImageExtension

logger = logging.getLogger(__name__)

POSTS_PATH = 'blog/templates/blog/posts/'


def refresh_posts():
    logger.info('refresh_posts start')
    posts_from_db = Post.objects.order_by('-date')
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
            db_post = __update_db_post_fields(db_post, post)
            updated_posts.append(db_post)

    __log_posts_names('new_posts', new_posts)
    __log_posts_names('updated_posts', updated_posts)

    if (len(new_posts) > 0):
        Post.objects.bulk_create(new_posts)

    if (len(updated_posts) > 0):
        Post.objects.bulk_update(
            updated_posts,
            ['title', 'slug', 'date', 'checksum', 'categories', 'tags']
        )

    logger.info('refresh_posts end')


def get_slug_to_post(posts):
    dictionary = {}
    for post in posts:
        dictionary[post.slug] = post
    return dictionary


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
    posts = []
    __create_posts_directory_if_needed()
    for md_file in markdown_files:
        metadata = __to_html(markdown_converter, md_file)
        post = get_post(metadata)
        posts.append(post)
    logger.debug('End process to convert Markdown to HTML')
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


def __log_posts_names(message, posts):
    posts_names = ''
    if len(posts) > 0:
        posts_names = ', '.join(map(lambda p: p.title, posts))
    logger.info(f'{message}: [{posts_names}]')


def __update_db_post_fields(db_post, post):
    db_post.title = post.title
    db_post.slug = post.slug
    db_post.date = post.date
    db_post.checksum = post.checksum
    db_post.categories = post.categories
    db_post.tags = post.tags
    return db_post
