import feedparser
from dataclasses import dataclass

@dataclass
class FeedEntry:
    title: str
    link: str
    description: str

class RssDownloader:
    def __init__(self):
        pass

    def get_feed_entries(rssUrl, itemLink):
        feed = feedparser.parse(rssUrl)
        for entry in feed.entries:
            if entry.link.endswith(itemLink):
                return FeedEntry(entry.title, entry.link, entry.description)
        return None