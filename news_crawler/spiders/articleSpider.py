# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import ArticleG1

__author__ = 'nolram'


class ArticleSpiderG1(CrawlSpider):

    name = "articleg1"
    allowed_domains = ["g1.globo.com"]
    start_urls = ["http://g1.globo.com/Noticias/Mundo/0,,MUL1569411-5602,00.html"]
    # "http://g1.globo.com/Noticias/Politica/0,,MUL4109-5601,00-VOTACAO+DO+PAC+NAO+DEVE+ATRASAR+DIZ+CHINAGLIA.html"]

    rules = (
        Rule(LinkExtractor(allow=('(.+).html$', ), deny=('(.+)(/blog/)', '(.+)(/previsao-do-tempo/)',)),
             callback='parse_item', follow=True,),
    )

    def parse_item(self, response):
        item = ArticleG1()

        titulo = response.xpath('//h1[contains(concat(" ", @class, " "), " entry-title ")]/text()').extract()
        categoria = response.xpath('//a[contains(concat(" ", @class, " "), " logo ")]/text()').extract()

        if categoria:
            tmp_categ = categoria[0]
            tmp_categ = tmp_categ.replace("\r", "").replace("\n", "").replace("\t", "")
            if len(tmp_categ) > 2:
                item["categoria"] = tmp_categ
            else:
                categoria = response.xpath('//div[@class="breadcrumb"]//h1//a//text()').extract()
                if categoria and len(categoria) > 0:
                    item["categoria"] = categoria[0]

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
        if data_publicado:
            item["data_publicado"] = data_publicado
        if data_atualizado:
            item["data_atualizado"] = data_atualizado
        if texto:
            item["texto"] = texto

        item["url"] = response.url

        return item
