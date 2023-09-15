import re
from bs4 import BeautifulSoup
from scrapy import Selector


def get_cleaned_html(html_string, *tags) -> Selector:
    soup = BeautifulSoup(html_string, 'html.parser')
    for tag_to_remove in tags:
        for tag in soup.find_all(tag_to_remove):
            tag.extract()
    return Selector(text=str(soup))


def contains_katakana_hiragana(text):
    pattern = r'[\u3040-\u309F\u30A0-\u30FF]+'
    match = re.search(pattern, text)
    return bool(match)