# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    HTTPS = "https:"

    rules = (
        # 文章id是有12位小写字母或者数字0-9构成
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    # 数据测试：scrapy shell https://www.jianshu.com/p/8d5ab6d5f258
    def parse_detail(self, response):
        title = response.xpath('//h1[@class="_2zeTMs"]/text()').get()

        author = response.xpath('//span[@class="_22gUMi"]/text()').get()

        avatar = self.HTTPS + response.xpath('//a[@class="qzhJKO"]/@href').get()

        pub_time = '2020-01-01 00:00:00'
        #response.xpath('//span[@class="publish-time"]/text()').get().replace("*", "")

        current_url = response.url
        real_url = current_url.split(r"?")[0]

        article_id = real_url.split(r'/')[-1]

        # 保留标签的H5内容[保留格式，方便后面排版]
        content = response.xpath('//article[@class="_2rhmJa"]').get()

        item = ArticleItem(
            title=title,
            avatar=avatar,
            pubtime=pub_time,
            origin_url=current_url,
            author=author,
            article_id=article_id,
            content=content
        )

        yield item
