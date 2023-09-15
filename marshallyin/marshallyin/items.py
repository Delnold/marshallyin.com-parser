# items.py

import scrapy


class GrammarLessonItem(scrapy.Item):
    JLPT = scrapy.Field()
    info = scrapy.Field()
    Level = scrapy.Field()
    Lesson = scrapy.Field()
    usage = scrapy.Field()
    meanings = scrapy.Field()
    audios = scrapy.Field()
    examples = scrapy.Field()
    notes = scrapy.Field()


class KanjiLessonItem(scrapy.Item):
    JLPT = scrapy.Field()
    info = scrapy.Field()
    Level = scrapy.Field()
    Lesson = scrapy.Field()
    kanji = scrapy.Field()
    reading = scrapy.Field()
    meaning = scrapy.Field()
    how_to_write = scrapy.Field()
    origin_text = scrapy.Field()
    origin_image = scrapy.Field()
    development_image = scrapy.Field()
    vocabulary = scrapy.Field()
    examples = scrapy.Field()


class VocabularyLessonItem(scrapy.Item):
    JLPT = scrapy.Field()
    info = scrapy.Field()
    Level = scrapy.Field()
    Lesson = scrapy.Field()
    words = scrapy.Field()
    readings = scrapy.Field()
    meanings = scrapy.Field()
    examples = scrapy.Field()

class AlphabetLessonItem(scrapy.Item):
    JLPT = scrapy.Field()
    info = scrapy.Field()
    Level = scrapy.Field()
    Lesson = scrapy.Field()
    letters = scrapy.Field()
    romajis = scrapy.Field()
    tips_text = scrapy.Field()
    tips_image = scrapy.Field()
    stroke_orders = scrapy.Field()
    how_to_write = scrapy.Field()
    vocabulary = scrapy.Field()