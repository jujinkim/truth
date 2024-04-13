import feedparser
from article_entity import ArticleEitnty

class RssDownloader:
    def __init__(self):
        pass

    def get_feed_entries(rssUrl, itemLink):
        feed = feedparser.parse(rssUrl)
        for entry in feed.entries:
            if entry.link.endswith(itemLink):
                return ArticleEitnty(entry.title, entry.link, entry.description)
        return None