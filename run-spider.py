from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from marshallyin.marshallyin.spiders.kanji import KanjiSpider
from marshallyin.marshallyin.spiders.alphabet import AlphabetSpider
from marshallyin.marshallyin.spiders.grammar import GrammarSpider
from marshallyin.marshallyin.spiders.vocabulary import VocabularySpider

process = CrawlerProcess(get_project_settings())
process.crawl(KanjiSpider)
process.crawl(AlphabetSpider)
process.crawl(GrammarSpider)
process.crawl(VocabularySpider)
process.start()