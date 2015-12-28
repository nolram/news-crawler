# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Article(Item):
    titulo = Field()
    subtitulo = Field()
    data_publicado = Field()
    data_atualizado = Field()
    categoria = Field()
    subcategoria = Field()
    texto = Field()
