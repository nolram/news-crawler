# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import Article

__author__ = 'nolram'


class ArticleSpider(CrawlSpider):
    name = "article"
    allowed_domains = ["g1.globo.com"]
    start_urls = ["http://g1.globo.com/index.html"]

    rules = (
        Rule(LinkExtractor(allow=('(.+).html$', )), callback='parse_item', follow=True,),
    )

    def parse_item(self, response):
        item = Article()
        titulo = response.xpath('//h1[contains(concat(" ", @class, " "), " entry-title ")]/text()').extract()
        categoria = response.xpath('//a[contains(concat(" ", @class, " "), " logo ")]/text()').extract()
        texto = response.xpath('//div[@id="materia-letra"]//p/text()').extract()

        subcategoria = response.xpath('//div[contains(concat(" ", @class, " "), " menu-subeditoria ")]//span/text()').extract()
        if subcategoria:
            subcategoria = u" ".join(subcategoria).lstrip()
            subcategoria = subcategoria.rstrip()
        else:
            subcategoria = u""

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
            texto = u" ".join(texto)
            item["texto"] = texto

        item["subcategoria"] = subcategoria
        return item
