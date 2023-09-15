import scrapy

from ..data_extraction.alphabet import figure_wp_block_table_explanation_extractor_alphabet, \
    table_press_extractor_alphabet, \
    figure_wp_block_table_extractor_row_variation_alphabet
from ..data_formatting.alphabet import letters_romaji_separator
from ..items import AlphabetLessonItem
from ..utils import contains_katakana_hiragana


class AlphabetSpider(scrapy.Spider):
    name = "AlphabetJP"
    allowed_domains = ["marshallyin.com"]
    custom_settings = {
        'FEEDS': {
            'data/AlphabetJP.json': {
                'format': 'json',
                'overwrite': True,
                'indent': 2,
                'ensure_ascii': False,
            },
        },
        'DOWNLOAD_DELAY': 2
    }

    def start_requests(self):
        urls = ["https://marshallyin.com/alphabet-course/"]

        for index, url in enumerate(urls, start=5):
            yield scrapy.Request(url, callback=self.parse, meta={'JLPT': index})

    def parse(self, response):
        JLPT = response.meta['JLPT']
        level_number = 1
        lesson_number = 1
        for lesson in response.xpath(".//table[contains(@class, 'tablepress')]/tbody/tr"):
            info = lesson.xpath(".//td[contains(@class, 'column-1')]/text()").get()
            if contains_katakana_hiragana(info):
                lesson_item = AlphabetLessonItem(
                    JLPT=JLPT,
                    info=info,
                    Level=level_number,
                    Lesson=lesson_number,
                )
                if lesson_number % 5 == 0:
                    level_number += 1
                lesson_number += 1

                next_page = lesson.xpath(".//td[contains(@class, 'column-2')]/a/@href").get()
                if next_page is not None:
                    yield response.follow(next_page, self.parse_lesson_page, meta={'lesson_item': lesson_item})
                else:
                    yield lesson_item
            else:
                continue

    def parse_lesson_page(self, response):
        lesson_item = response.meta['lesson_item']
        tips_text, tips_image, stroke_orders, how_to_write = figure_wp_block_table_explanation_extractor_alphabet(
            "//figure[@class='wp-block-table']/table/tbody[tr[td[strong[contains(.,'Tip')]]]]", response)
        letters_romajis = figure_wp_block_table_extractor_row_variation_alphabet(
            "//p[strong[contains(., 'Romaji')]]/following::figure[@class='wp-block-table'][1]/table/tbody", response)
        vocabulary = table_press_extractor_alphabet("//p[strong[contains(., 'Vocabulary')]]/following::table[1]",
                                                    response)
        letters, romajis = letters_romaji_separator(letters_romajis)

        lesson_item["tips_text"] = tips_text
        lesson_item["tips_image"] = tips_image
        lesson_item["stroke_orders"] = stroke_orders
        lesson_item["how_to_write"] = how_to_write
        lesson_item["letters"] = letters
        lesson_item["romajis"] = romajis
        lesson_item["vocabulary"] = vocabulary
        yield lesson_item
