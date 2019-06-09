# -*- coding:utf8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector, Selector
from meduza_articles.items import MeduzaArticlesItem


class ArticleLoader(ItemLoader):
    default_output_processor = Join('\n')


class ArticlesSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['meduza.io']
    start_urls = [
        'https://meduza.io/feature/2019/06/08/my-prizyvaem-vseh-perepechatyvat-polnye-teksty-rassledovaniy-ivana-golunova']

    def parse(self, response):
        for url in response.xpath('//li[@class=""]/a[1]/@href').extract():
            request = Request(str(url), callback=self.parse_story)
            yield request

    def parse_story(self, response):
        hxs = HtmlXPathSelector(response)
        loader = ArticleLoader(MeduzaArticlesItem(), hxs)

        date = str('-'.join(response.url.split('/')[4:7]))
        title = hxs.xpath(
            '//div/h1[contains(@class, "RichTitle-root")]/text()'
        ).extract()[0]

        p = []
        for par in hxs.xpath('''
            //div[@class="GeneralMaterial-article"]/p//text()
            |//div[@class="GeneralMaterial-article"]/h3//text()
            ''').extract():
            p.append(par)
        text = ' '.join(p)

        loader.add_value('url', str(response.url))
        loader.add_xpath(
            'title',
            '//div/h1[contains(@class, "RichTitle-root")]/text()')
        loader.add_value('date_published', date)
        loader.add_value('text', text)
        # TODO crawl likes
        loader.add_value('fb_likes', '')
        loader.add_value('vk_likes', '')
        loader.add_value('ok_likes', '')

        return loader.load_item()
