# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import ArticleG1

__author__ = 'nolram'


class ArticleSpiderG1(CrawlSpider):
    name = "articleg1"
    allowed_domains = ["g1.globo.com"]
    start_urls = ["http://g1.globo.com/index.html"]

    rules = (
        Rule(LinkExtractor(allow=('(.+).html$', ), deny=('(.+)(/blog/)', )), callback='parse_item', follow=True,),
    )

    def parse_item(self, response):
        item = ArticleG1()
        titulo = response.xpath('//h1[contains(concat(" ", @class, " "), " entry-title ")]/text()').extract()
        categoria = response.xpath('//a[contains(concat(" ", @class, " "), " logo ")]/text()').extract()
        texto = response.xpath('//div[@id="materia-letra"]//p/text()').extract()

        subcategoria = response.xpath('//div[contains(concat(" ", @class, " "), " menu-subeditoria ")]//span/text()').extract()

        if subcategoria:
            subcategoria = u" ".join(subcategoria).lstrip()
            subcategoria = subcategoria.rstrip()
            item["subcategoria"] = subcategoria

        data_publicado = response.xpath('//abbr[@class="published"]/text()').extract()
        data_atualizado = response.xpath('//abbr[@class="updated"]/text()').extract()

        if titulo:
            item["titulo"] = titulo[0]
        if categoria:
            item["categoria"] = categoria[0]
        if data_publicado:
            item["data_publicado"] = data_publicado
        if data_atualizado:
            item["data_atualizado"] = data_atualizado
        if texto:
            item["texto"] = texto

        item["url"] = response.url

        return item
