import requests
from bs4 import BeautifulSoup
from article_entity import ArticleEitnty

class ArticleDownloader:
    def __init__(self):
        pass

    # Download html from the given url, and return the title and article content
    def download_article(self, url, title_tag_selector, article_tag_selector):
        html = requests.get(url).text
        title = self._extract_title(html, title_tag_selector)
        article = self._extract_article(html, article_tag_selector)
        return ArticleEitnty(title, url, article)

    # Extract title from the given html
    def _extract_title(self, html, title_tag_selector):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one(title_tag_selector)
        return title.text if title else None

    # Extract article content from the given html
    def _extract_article(self, html, article_tag_selector):
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.select_one(article_tag_selector)
        return article.text if article else None