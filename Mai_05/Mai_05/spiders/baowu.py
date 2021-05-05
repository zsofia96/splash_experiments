import scrapy
from scrapy_splash import SplashRequest

class BaowuSpider(scrapy.Spider):
    name = 'baowu'
    allowed_domains = ['baowugroup.com']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(10))
            assert(splash:runjs("document.getElementsByClassName('router-link-active')[0].click()"))
            assert(splash:wait(10))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='http://www.baowugroup.com/en/#/aboutus/291/327',
            callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        articles = response.xpath("//th[@class='ht']")
        for article in articles:
            yield {
                'link': "http://www.baowugroup.com/en/"+str(article.xpath(".//a/@href").get())
            }
