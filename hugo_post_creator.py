from datetime import datetime
import html2text
import html
from post_creator import PostCreator
from googletrans import Translator
from bs4 import BeautifulSoup
import pytz
from article_entity import ArticleEitnty

class HugoPostCreator(PostCreator):
    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.translator = Translator()

    def translate_text(self, text):
        return self.translator.translate(text, dest='en').text

    def create_post(self, feed_entry: ArticleEitnty, path):
        date = datetime.now(pytz.timezone('Asia/Seoul')).isoformat(timespec='seconds')
        description_decoded = html.unescape(feed_entry.content)

        # Translate the description to English and convert to markdown
        soup = BeautifulSoup(description_decoded, 'html.parser')
        paragraphs = soup.find_all('p')
        description_md = ''
        for paragraph in paragraphs:
            print("Translating: ", paragraph.text)
            translated_p = self.translate_text(paragraph.text)
            description_md += self.converter.handle(translated_p) + '\n\n'

        print("Translating: ", feed_entry.title)
        translated_title = self.translate_text(feed_entry.title)

        # Write the post to the HUGO markdown file
        content = f'---\n'
        content += f'title: "{translated_title}"\n'
        content += f'date: {date}\n'
        content += f'draft: false\n'
        content += f'---\n\n'
        content += f'{description_md}\n\n'
        content += f'Original post: [{feed_entry.link}]({feed_entry.link})'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
