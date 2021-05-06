import scrapy
from scrapy_splash import SplashRequest

class Baowu2Spider(scrapy.Spider):
    name = 'baowu2'
    allowed_domains = ['baowugroup.com']
    # start_urls = ['http://www.baowugroup.com/en/#/aboutus/291/327']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 30})

    def parse(self, response):

        script = '''
            function main(splash, args)
                assert(splash:go(args.url))
                assert(splash:wait(10))
                assert(splash:runjs("document.getElementsByClassName('router-link-active')[0].click()"))
                assert(splash:wait(10))
                assert(splash:runjs("document.getElementsByClassName('btn-next')[0].click()"))
                assert(splash:wait(10))
                return splash:html()
            end
        '''

        next_page = response.xpath("//button[@class='btn-next']")
        if next_page is not None:
            url = "http://www.baowugroup.com/en/#/aboutus/291/327"
            yield SplashRequest(
                url,
                self.parse,
                endpoint='execute',
                method='POST',
                dont_filter=True,
                args={
                    'wait': 30,
                    'lua_source': script,
                },
            )