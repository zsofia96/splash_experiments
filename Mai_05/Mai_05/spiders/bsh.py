import scrapy
from scrapy_splash import SplashRequest

class BshSpider(scrapy.Spider):
    name = 'bsh'
    allowed_domains = ['bsh-group.com']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(30))
            assert(splash:runjs("document.getElementsByClassName('btn btn-primary js_accept-cookies')[0].click()"))
            assert(splash:wait(30))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='http://www.bsh-group.com/press/press-releases',
            callback=self.parse,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'},
            endpoint='execute',
            args={'lua_source': self.script}
        )

    def parse(self, response):
        articles = response.xpath("//button[@class='copyBtn btn btn-primary js_copyLinkBtn']")
        for article in articles:
            yield {
                'link': article.xpath(".//@data-clipboard-text").get()
            }

