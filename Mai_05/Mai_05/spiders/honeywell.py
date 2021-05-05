import scrapy


class HoneywellSpider(scrapy.Spider):
    name = 'honeywell'
    allowed_domains = ['honeywellprocess.com']
    start_urls = ['https://www.honeywellprocess.com/en-us/news-and-events/pages/press-releases.aspx']

    def parse(self, response):
        articles = response.xpath("//div[@class='srch-Title3']")
        for article in articles:
            yield {
                'link': article.xpath(".//a/@href").get()
            }

        next_page = response.xpath("//a[@id='SRP_NextImg']/@href").get()
        if next_page:
            absolute_url = f"https://www.honeywellprocess.com{next_page}"
            yield scrapy.Request(url=absolute_url, callback=self.parse)
