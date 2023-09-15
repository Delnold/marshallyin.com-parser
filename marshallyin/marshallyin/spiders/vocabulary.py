import scrapy
from ..items import VocabularyLessonItem
from ..data_extraction.vocabulary import table_press_extractor_vocabulary, figure_wp_block_table_extractor_vocabulary
from ..data_formatting.vocabulary import words_readings_meanings_separator


class VocabularySpider(scrapy.Spider):
    name = "VocabularyJP"
    allowed_domains = ["marshallyin.com"]
    custom_settings = {
        'FEEDS': {
            'data/VocabularyJP.json': {
                'format': 'json',
                'overwrite': True,
                'indent': 2,
                'ensure_ascii': False,
            },
        },
        'DOWNLOAD_DELAY': 2
    }

    def start_requests(self):
        urls = ["https://marshallyin.com/courses/n1-vocabulary-course/?tab=tab-curriculum",
                "https://marshallyin.com/courses/n2-vocabulary-course/?tab=tab-curriculum",
                "https://marshallyin.com/courses/n3-vocabulary-course/?tab=tab-curriculum",
                "https://marshallyin.com/courses/n4-vocabulary-course/?tab=tab-curriculum",
                "https://marshallyin.com/courses/n5-vocabulary-course/?tab=tab-curriculum"]

        for index, url in enumerate(urls, start=1):
            yield scrapy.Request(url, callback=self.parse, meta={'JLPT': index})

    def parse(self, response):
        JLPT = response.meta['JLPT']
        level_number = 1
        lesson_number = 1
        if JLPT == 5:
            for lesson in response.xpath(".//ul[@class='section-content']/li"):
                info = lesson.xpath(".//a[@class='section-item-link']/span/text()").get()
                lesson_item = VocabularyLessonItem(
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
        if JLPT == 4 or JLPT == 3 or JLPT == 2 or JLPT == 1:
            for level in response.xpath(".//ul[@class='curriculum-sections']/li[@class='section']"):
                if level.xpath(
                        ".//h5[contains(.,'Previous Levels')]"):
                    continue
                for lesson in level.xpath(".//ul[@class='section-content']/li"):
                    if lesson.xpath(".//a[@class='section-item-link']/span[contains(., 'Review')]"):
                        continue
                    info = lesson.xpath(".//span[contains(@class, 'item-name')]/text()").get()
                    lesson_item = VocabularyLessonItem(
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
        words_readings_meanings = table_press_extractor_vocabulary(
            ".//table[1]",
            response)
        words, readings, meanings = words_readings_meanings_separator(words_readings_meanings)
        examples = figure_wp_block_table_extractor_vocabulary(
            "//p[strong[contains(., 'Example')]]/following::figure[@class='wp-block-table'][1]/table/tbody",
            response)
        lesson_item["words"] = words
        lesson_item["readings"] = readings
        lesson_item["meanings"] = meanings
        lesson_item["examples"] = examples
        yield lesson_item
