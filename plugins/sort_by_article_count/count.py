def sort_by_article_count(tags):
    """Return a number articles with the given tag."""
    return sorted(tags, key=lambda tags: len(tags[1]), reverse=True)
