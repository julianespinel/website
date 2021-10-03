from pelican import signals
from . import count


def add_filter(pelican):
    """Add count_elements filter to Pelican."""
    pelican.env.filters.update(
        {'sort_by_article_count': count.sort_by_article_count})


def register():
    """Plugin registration."""
    signals.generator_init.connect(add_filter)
