from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zoominfo_interview_spider.sos_search.spiders.company_search_spider import CompanySearchSpider
import os

path = os.path.dirname(os.path.abspath(__file__))

settings = get_project_settings()
settings.update({'FEED_URI': '{0}/data.json'.format(path)})

process = CrawlerProcess(settings)

process.crawl(CpSearchSpider, startswith='X')
process.start()