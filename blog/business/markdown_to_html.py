"""
This file contains the business logic for the blogs app.
If the business logic grows I will create a folder named `business/`
and then I will create files to separate different busines logic,
for example: `posts.py`, `comments.py`, etc.
"""

from django.apps import AppConfig

import os
import glob
import markdown
import logging

from mdx_gfm import GithubFlavoredMarkdownExtension


logger = logging.getLogger(__name__)


def convert_all():
    logger.info('Start process to convert Markdown to HTML')
    directory = 'blog/posts'
    file_extension = '.md'
    markdown_files = __list_files_from(directory, file_extension)
    logger.info(f'listdir: {os.listdir(".")}')
    logger.info(f'markdown_files: {markdown_files}')
    markdown_converter = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()])
    for md_file in markdown_files:
        __convert_single(markdown_converter, md_file)
    logger.info('End process to convert Markdown to HTML')


def __list_files_from(directory, file_extension):
    return glob.glob(f'{directory}/*{file_extension}')


def __convert_single(converter, markdown_file_path):
    output_file_name = __get_file_name_only(markdown_file_path) + ".html"
    output_file_path = f'blog/templates/blog/posts/{output_file_name}'
    logger.info(f'About to write to: {output_file_path}')
    converter.convertFile(input=markdown_file_path, output=output_file_path, encoding='utf-8')
    logger.info(f'converted {markdown_file_path} to {output_file_path}')


def __get_file_name_only(file_path_with_extension):
    name = os.path.basename(file_path_with_extension)
    return os.path.splitext(name)[0]
