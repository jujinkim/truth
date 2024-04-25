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
        published_time = self._extract_published_time(html)
        return ArticleEitnty(title, url, article, published_time)

    # Extract title from the given html
    def _extract_title(self, html, title_tag_selector):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one(title_tag_selector)
        return title.text if title else "No title found."

    # Extract article content from the given html
    def _extract_article(self, html, article_tag_selector):
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.select_one(article_tag_selector)
        return str(article.decode_contents()) if article else "No article content found."
    
    # Extract published time from the given html
    def _extract_published_time(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        published_time_meta = soup.find('meta', attrs={'property': 'article:published_time'})
        return published_time_meta['content'] if published_time_meta else ""