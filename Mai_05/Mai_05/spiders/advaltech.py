import scrapy
from scrapy_splash import SplashRequest

class AdvaltechSpider(scrapy.Spider):
    name = 'advaltech'
    allowed_domains = ['advaltech.com']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(40))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.advaltech.com/en/group/news/corporate-news/',
            callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        articles = response.xpath("//div[@class='panel-body']/article")
        for article in articles:
            yield {
                'link': "https://www.advaltech.com/"+article.xpath(".//a/@href").get()
            }
