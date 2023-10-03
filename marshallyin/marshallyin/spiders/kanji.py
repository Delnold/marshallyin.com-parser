import re
import scrapy
from ..data_extraction.kanji import figure_wp_block_table_extractor_kanji, \
    div_w_b_quote_extractor_kanji, \
    figure_wp_block_table_extractor_row_variation_kanji, div_wp_block_image, table_press_extractor_kanji
from ..items import KanjiLessonItem
from ..data_formatting.kanji import reading_meaning_kanji_separator


class KanjiSpider(scrapy.Spider):
    name = "KanjiJP"
    allowed_domains = ["marshallyin.com"]
    # Matching Kanji in text
    kanji_pattern = r'[\u4E00-\u9FFF]'
    custom_settings = {
        'FEEDS': {
            'data/KanjiJP.json': {
                'format': 'json',
                'overwrite': True,
                'indent': 2,
                'ensure_ascii': False,
            },
        },
        'DOWNLOAD_DELAY': 2
    }

    def start_requests(self):
        urls = ["https://marshallyin.com/courses/n2-kanji-course/?tab=tab-curriculum",
                "https://marshallyin.com/courses/n3-kanji-course/?tab=tab-curriculum",
                "https://marshallyin.com/courses/n4-kanji-course/?tab=tab-curriculum",
                "https://marshallyin.com/courses/n5-kanji-course/?tab=tab-curriculum"]

        for index, url in enumerate(urls, start=2):
            yield scrapy.Request(url, callback=self.parse, meta={'JLPT': index})

    def parse(self, response):
        JLPT = response.meta['JLPT']
        level_number = 1
        lesson_number = 1
        if JLPT == 5:
            for lesson in response.xpath(".//ul[@class='section-content']/li"):
                info = lesson.xpath(".//a[@class='section-item-link']/span/text()").get()
                lesson_item = KanjiLessonItem(
                    JLPT=JLPT,
                    info=info,
                    Level=level_number,
                    Lesson=lesson_number,
                )
                if lesson_number % 5 == 0:
                    level_number += 1
                lesson_number += 1

                next_page = lesson.xpath(".//a[contains(@class, 'section-item-link')]/@href").get()
                if next_page is not None:
                    yield response.follow(next_page, self.parse_lesson_page, meta={'lesson_item': lesson_item})
                else:
                    yield lesson_item
        if JLPT == 4 or JLPT == 3 or JLPT == 2:
            for level in response.xpath(".//ul[@class='curriculum-sections']/li[@class='section']"):
                if level.xpath(
                        ".//h5[contains(.,'Previous Levels')]"):
                    continue
                for lesson in level.xpath(".//ul[@class='section-content']/li"):
                    if lesson.xpath(".//a[@class='section-item-link']/span[contains(., 'Review')]"):
                        continue
                    info = lesson.xpath(".//span[contains(@class, 'item-name')]/text()").get()
                    lesson_item = KanjiLessonItem(
                        JLPT=JLPT,
                        info=info,
                        Level=level_number,
                        Lesson=lesson_number,
                    )
                    if lesson_number % 5 == 0:
                        level_number += 1
                    lesson_number += 1

                    next_page = lesson.xpath(".//a[contains(@class, 'section-item-link')]/@href").get()
                    if next_page is not None:
                        yield response.follow(next_page, self.parse_lesson_page, meta={'lesson_item': lesson_item})
                    else:
                        yield lesson_item

    def parse_lesson_page(self, response):
        lesson_item = response.meta['lesson_item']
        kanji = None
        reading = None
        meaning = None
        how_to_write = None
        origin_text = None
        origin_image = None
        development_image = None
        vocabulary = None
        examples = None

        if lesson_item["JLPT"] == 5:
            reading_meaning_kanji = figure_wp_block_table_extractor_kanji(
                "//p[strong[contains(., 'Reading & Meaning')]]/following::figure[@class='wp-block-table'][1]/table/tbody",
                response)
            reading, meaning, kanji = reading_meaning_kanji_separator(reading_meaning_kanji)
            how_to_write = figure_wp_block_table_extractor_kanji(
                "//p[strong[contains(., 'How to write')]]/following::figure[@class='wp-block-table'][1]/table/tbody",
                response)
            vocabulary = figure_wp_block_table_extractor_kanji(
                "//p[strong[contains(., 'Words of')]]/following::figure[@class='wp-block-table'][1]/table/tbody",
                response)
            examples = figure_wp_block_table_extractor_kanji(
                "//p[strong[contains(., 'Example Sentences')]]/following::figure[@class='wp-block-table'][1]/table/tbody",
                response)
        if lesson_item["JLPT"] == 2 or lesson_item["JLPT"] == 3 or lesson_item["JLPT"] == 4:
            kanji = re.findall(self.kanji_pattern, lesson_item["info"])
            meaning = div_w_b_quote_extractor_kanji(
                "//p[strong[contains(., 'Meaning')]]/following::div[@class='w_b_quote w_b_div'][1]", response)
            reading = figure_wp_block_table_extractor_row_variation_kanji(
                "//p[strong[contains(., 'How to read')]]/following::figure[@class='wp-block-table'][1]/table/tbody",
                response)
            if not reading:
                reading = div_w_b_quote_extractor_kanji(
                    "//p[strong[contains(., 'How to read it')]]/following::div[@class='w_b_quote w_b_div'][1]",
                    response)
            how_to_write = div_wp_block_image(
                "//p[strong[contains(., 'How to write')]]/following::div[@class='wp-block-image'][1]",
                response)
            origin_text = div_w_b_quote_extractor_kanji(
                "//p[strong[contains(., 'Origin')]]/following::div[@class='w_b_quote w_b_div'][1]", response)
            origin_image = div_wp_block_image(
                "//p[strong[contains(., 'Origin')]]/following::div[@class='wp-block-image'][1]", response)
            development_image = div_wp_block_image(
                "//p[strong[contains(., 'Development')]]/following::div[@class='wp-block-image'][1]", response)
            vocabulary = table_press_extractor_kanji(
                "//p[strong[contains(., 'Vocabulary')]]/following::table[1]",
                response)
            examples = figure_wp_block_table_extractor_kanji(
                "//p[strong[contains(., 'Example')]]/following::figure[@class='wp-block-table'][1]/table/tbody",
                response)

        lesson_item["kanji"] = kanji
        lesson_item["reading"] = reading
        lesson_item["meaning"] = meaning
        lesson_item["how_to_write"] = how_to_write
        lesson_item["origin_text"] = origin_text
        lesson_item["origin_image"] = origin_image
        lesson_item["development_image"] = development_image
        lesson_item["vocabulary"] = vocabulary
        lesson_item["examples"] = examples

        yield lesson_item
