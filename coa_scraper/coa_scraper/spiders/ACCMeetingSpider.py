import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ACCMeetingSpider(CrawlSpider):
    name = 'austintexas.gov'
    allowed_domains = ['austintexas.gov']
    start_urls = ['https://www.austintexas.gov/department/city-council/archive/city_council_meeting_archives.htm']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('.htm', ), restrict_css=('a.edims')), callback='parse_files'),

        #Rule(LinkExtractor(allow=('document\.cfm', )), callback='download_file'),

    )

    def parse_files(self, response):
        return { 'file_urls': response.xpath('//a[contains(@href,"document.cfm")]/@href').getall() }

    def download_file(self, response):
        self.logger.info('Hi, this is a download! %s', response.url)
        return { 'file_urls' : [response.url] }
