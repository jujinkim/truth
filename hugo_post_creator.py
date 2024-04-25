from datetime import datetime
from post_creator import PostCreator
from googletrans import Translator
import pytz
import config
from article_entity import ArticleEitnty
import argostranslate.package, argostranslate.translate
import translatehtml
from markdownify import markdownify as md
import os

class HugoPostCreator(PostCreator):
    def __init__(self):
        #Init
        print("HugoPostCreator init")
        self.translator = Translator()

        # Check and load the Argostranslate package
        print("Loading Argostranslate package")
        available_packages = argostranslate.package.get_available_packages()
        available_package = list(filter(lambda x: x.from_code == config.from_lang and x.to_code == config.to_lang, available_packages))[0]
        download_path = available_package.download()
        argostranslate.package.install_from_path(download_path)

        # Load the translation model
        print("Loading Argostranslate translation model")
        installed_lang = argostranslate.translate.get_installed_languages()
        from_lang = list(filter(lambda x: x.code == config.from_lang, installed_lang))[0]
        to_lang = list(filter(lambda x: x.code == config.to_lang, installed_lang))[0]
        self.html_translation = from_lang.get_translation(to_lang)

    def translate_html(self, html_text):
        return translatehtml.translate_html(self.html_translation, html_text)

    def translate_text(self, text):
        return self.translator.translate(text, dest='en').text

    def create_post(self, feed_entry: ArticleEitnty, path):
        date = datetime.now(pytz.timezone('Asia/Seoul')).isoformat(timespec='seconds')
        description_md = ''

        # Translate the description to English and convert to markdown
        print("Translating: content")
        translated_html = str(self.translate_html(feed_entry.content)).strip()
        print("Convert to markdown")
        print("Translated HTML: ", translated_html)
        description_md = md(translated_html)

        print("Translating: ", feed_entry.title)
        translated_title = self.translate_text(feed_entry.title)

        # Write the post to the HUGO markdown file
        print("Writing to file: ", path)
        content = f'---\n'
        content += f'title: "{translated_title}"\n'
        content += f'date: {date}\n'
        content += f'draft: false\n'
        content += f'---\n\n'
        content += f'{description_md}\n\n'

        content += f'Automatically translated using Google Translate and copied by [Truth](https://github.com/jujinkim/truth).\n'
        content += f'Original post: [{feed_entry.link}]({feed_entry.link})'

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
