from abc import ABC, abstractmethod
from article_entity import ArticleEitnty

class PostCreator(ABC):
    @abstractmethod
    def create_post(self, article: ArticleEitnty, path: str):
        pass