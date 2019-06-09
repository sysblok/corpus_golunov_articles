# -*- coding: utf-8 -*-

from scrapy import Item, Field


class MeduzaArticlesItem(Item):
    url = Field()
    title = Field()
    date_published = Field()
    text = Field()
    fb_likes = Field()
    vk_likes = Field()
    ok_likes = Field()


def title_shortener(title):
    if '.' in title:
        title = title.split('.')[0]
    return title
