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
        description_md = ''

        description_decoded = html.unescape(feed_entry.content)

        # Translate the description to English and convert to markdown
        soup = BeautifulSoup(description_decoded, 'html.parser')
        elements = soup.find_all(['p', 'a', 'img'])
        imgCnt = 1
        for elem in elements:
            if elem.name == 'img':
                print("Image: ", elem['src'])
                imgUrl = elem['src']
                description_md += f'![Image{imgCnt}]({imgUrl})\n\n'
                imgCnt += 1
            elif elem.name == 'a':
                print("Link: ", elem['href'])
                description_md += f'[{elem.text}]({elem["href"]})\n\n'
            elif elem.name == 'p':
                print("Translating: ", elem.text)
                if elem.text.replace('<br>', '').replace('<br/>', '').replace('<br />', '').strip() == '':
                    continue
                translated_p = self.translate_text(elem.text)
                description_md += self.converter.handle(translated_p) + '\n'

        print("Translating: ", feed_entry.title)
        translated_title = self.translate_text(feed_entry.title)

        # Write the post to the HUGO markdown file
        content = f'---\n'
        content += f'title: "{translated_title}"\n'
        content += f'date: {date}\n'
        content += f'draft: false\n'
        content += f'---\n\n'
        content += f'{description_md}\n\n'

        content += f'Automatically translated using Google Translate and copied by [Truth](https://github.com/jujinkim/truth).\n'
        content += f'Original post: [{feed_entry.link}]({feed_entry.link})'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
