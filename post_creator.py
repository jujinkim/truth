from abc import ABC, abstractmethod
from rss_downloader import FeedEntry

class PostCreator(ABC):
    @abstractmethod
    def create_post(self, feed_entry: FeedEntry, path: str):
        pass