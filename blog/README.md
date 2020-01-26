# Blog

The blog is a Django application within the website project.

It currently supports the following URLs:

* Home: http://localhost:8000/blog (Shows tags and stats about the blog?)
* Posts: http://localhost:8000/blog/posts (Shows a list of the published posts ordered by date descending)
* Single post: http://localhost:8000/blog/posts/`<post-slug>` (Shows the contents of a single post)

## Anatomy of a post

A post is a Markdown file with two main parts:

1. Metadata
1. Content

### Metadata

This block represents the metadata of a single post:
```
title: Should parking fares work like Uber?
date: 2018-04-14 
tags: economics, uber
```

Currently only those three fields are supported as metadata:
1. title: the title of the post.
1. date: the date the post was published for the first time.
    * According to ISO 8601 standard
    * Date only, no time
    * Example: `2020-12-30`
1. tags: comma separated strings to categorize the post.

### Content

The content of the post written in Markdown.<br>
See: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

#### Sources

As part of the content, it is **vital** to refernce the sources used in the post.

To references a source do the following:

1. In the content add a superscripted number or char.
1. By the end of the post add a section named Sources.
1. In the Sources section add the matching number or char superscripted in point 1, and add the citation or web link.

Example:

```
# About Django <--- Title

... <--- Content
This post is about the Django Web Framework<sup>1</sup> <--- Add superscripted number
Not to be confused with this other Django<sup>2</sup> <--- Add other superscripted number
... <--- More content

## Sources <--- Sources section

1. https://www.djangoproject.com <--- Matching superscripted number. Reference link
2. https://www.imdb.com/title/tt1853728/
```

## How to add a new post?

Let's pretend we are going to crete a new blog post about Django.

1. Create a new Markdown file in the folder `posts/`. For example: `posts/about-django.md`
1. Add the metadata and the content as described in the section [Anatomy of a post](#anatomy-of-a-post) of this file.
1. Restart the server.
1. Go to `http://localhost:8000/blog/posts/about-django`

## How does it work?

As soon as the Django project is started, the following steps are executed by the blog application:

1. Get all the files with `.md` extension from the directory `posts/`
1. For each Markdown file:
    1. Convert the contents of the file as HTML. (We use GitHub flavored markdown here)
    1. Save the HTML file perserving the markdown file name in the folder `templates/blog/posts`