import re
import scrapy
from ..data_extraction.grammar import data_extractor_grammar
from ..utils import get_cleaned_html
from ..items import GrammarLessonItem


class GrammarSpider(scrapy.Spider):
    name = "GrammarJP"
    allowed_domains = ["marshallyin.com"]

    custom_settings = {
        'FEEDS': {
            'data/GrammarJP.json': {
                'format': 'json',
                'overwrite': True,
                'indent': 2,
                'ensure_ascii': False,
            },
        },
        'DOWNLOAD_DELAY': 2
    }

    def start_requests(self):
        urls = ['https://marshallyin.com/courses/n1-grammar-course/?tab=tab-curriculum',
                'https://marshallyin.com/courses/n2-grammar-course/?tab=tab-curriculum',
                'https://marshallyin.com/courses/n3-grammar-course/?tab=tab-curriculum',
                'https://marshallyin.com/courses/n4-grammar-course/?tab=tab-curriculum',
                'https://marshallyin.com/courses/n5-grammar-course/?tab=tab-curriculum']

        for index, url in enumerate(urls, start=1):
            yield scrapy.Request(url, callback=self.parse, meta={'JLPT': index})

    def parse(self, response):
        JLPT = response.meta['JLPT']

        for level in response.xpath(".//ul[@class='curriculum-sections']/li[@class='section']"):
            if level.xpath(
                    ".//h5[contains(.,'Previous Levels')]"):
                continue
            for lesson in level.xpath(".//ul[@class='section-content']/li"):
                info = lesson.xpath(".//span[contains(@class, 'item-name')]/text()").get()
                level_info = level.xpath(".//h5[contains(@class, 'section-title')]/text()").get()

                if level_info == "Level MAX":
                    level_number = 'MAX'
                else:
                    level_number = int(level_info.split()[1])

                lesson_number = int(re.search(r'\d+', info).group())

                lesson_item = GrammarLessonItem(
                    JLPT=JLPT,
                    info=info,
                    Level=level_number,
                    Lesson=lesson_number,
                )

                next_page = lesson.xpath(".//a[contains(@class, 'section-item-link')]/@href").get()
                if next_page is not None:
                    yield response.follow(next_page, self.parse_lesson_page, meta={'lesson_item': lesson_item})
                else:
                    yield lesson_item


    def parse_lesson_page(self, response):

        lesson_item = response.meta['lesson_item']
        html_string = response.body.decode('utf-8')

        cleaned_response = get_cleaned_html(html_string, 'rt')
        usages = data_extractor_grammar(cleaned_response,
                                xpath_div_w_b_quote_str=
                                "//p[strong[contains(., 'Usage')]]/following::div[@class='w_b_quote w_b_div'][1]")
        meanings = data_extractor_grammar(cleaned_response,
                                  xpath_figure_wp_block_str=
                                  "//p[strong[contains(., 'Meaning')]]/following::figure[@class='wp-block-table'][1]/table/tbody/tr",
                                  xpath_div_w_b_quote_str=
                                  "//p[strong[contains(., 'Meaning')]]/following::div[@class='w_b_quote w_b_div'][1]"
                                  )
        examples = data_extractor_grammar(cleaned_response,
                                  xpath_figure_wp_block_str=
                                  "//p[strong[contains(., 'Example')]]/following::figure[@class='wp-block-table'][1]/table/tbody/tr",
                                  xpath_div_w_b_quote_str=
                                  "//p[strong[contains(., 'Example')]]/following::div[@class='w_b_quote w_b_div'][1]"
                                  )
        audios = cleaned_response.xpath("//p[strong[contains(., 'Example')]]/following::figure[@class='wp-block-audio']/audio/@src").getall()

        lesson_item["usage"] = usages
        lesson_item["meanings"] = meanings
        lesson_item["audios"] = audios
        lesson_item["examples"] = examples

        yield lesson_item
