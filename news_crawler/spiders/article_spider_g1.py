# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import ArticleG1

__author__ = 'nolram'


class ArticleSpiderG1(CrawlSpider):

    name = "articleg1"
    allowed_domains = ["g1.globo.com", "globo.com"]
    start_urls = ["http://www.globo.com/"]
    # "http://g1.globo.com/Noticias/Politica/0,,MUL4109-5601,00-VOTACAO+DO+PAC+NAO+DEVE+ATRASAR+DIZ+CHINAGLIA.html"]

    rules = (
        Rule(LinkExtractor(allow=('(.+).html$', '(.+).ghtml$'), deny=('(.+)(/blog/)', '(.+)(/previsao-do-tempo/)',)),
             callback='parse_item', follow=True,),
    )

    def parse_item(self, response):
        item = ArticleG1()

        titulo = response.xpath('//h1[contains(concat(" ", @class, " "), " content-head__title ")]/text()').extract_first()
        if titulo is None:
            titulo = response.xpath(
                '//h1[contains(concat(" ", @class, " "), " entry-title ")]/text()').extract_first()
        categoria = response.xpath(
            '//a[contains(concat(" ", @class, " "), " header-editoria--link ")]/text()').extract_first()
        if categoria is None:
            categoria = response.xpath(
                '//div[contains(concat(" ", @class, " "), " item-editoria ")]//a/text()').extract_first()

        item["categoria"] = categoria

        # if categoria:
        #     tmp_categ = categoria[0]
        #     tmp_categ = tmp_categ.replace("\r", "").replace("\n", "").replace("\t", "")
        #     if len(tmp_categ) > 2:
        #         item["categoria"] = tmp_categ
        #     else:
        #         categoria = response.xpath('//div[@class="breadcrumb"]//h1//a//text()').extract()
        #         if categoria and len(categoria) > 0:
        #             item["categoria"] = categoria[0]

        texto = response.xpath('//p[contains(concat(" ", @class, " "), " content-text__container ")]/text()').extract()
        if len(texto) == 0:
            texto = response.xpath(
                '//div[contains(concat(" ", @class, " "), " materia-conteudo ")]//p/text()').extract()

        subcategoria = response.xpath(
            '//a[contains(concat(" ", @class, " "), " header-subeditoria--link ellip-line ")]/text()').extract_first()

        if subcategoria:
            subcategoria = u" ".join(subcategoria).lstrip()
            subcategoria = subcategoria.rstrip()
            item["subcategoria"] = subcategoria

        data_publicado = response.xpath(
            '//time[contains(concat(" ", @itemprop, " "), " datePublished ")]/@datetime').extract_first()

        if data_publicado:
            data_publicado = response.xpath(
                '//abbr[contains(concat(" ", @class, " "), " published ")]/text()').extract_first()
        data_atualizado = response.xpath(
            '//abbr[contains(concat(" ", @class, " "), " updated ")]/text()').extract_first()

        if titulo:
            item["titulo"] = titulo
        if data_publicado:
            item["data_publicado"] = data_publicado
        if data_atualizado:
            item["data_atualizado"] = data_atualizado
        if texto:
            texto = " ".join(texto)
            item["texto"] = texto

        item["url"] = response.url

        yield item
