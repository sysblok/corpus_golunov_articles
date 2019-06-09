# -*- coding: utf-8 -*-

from meduza_articles.items import title_shortener


class MeduzaArticlesPipeline(object):
    def process_item(self, item, spider):
        title = title_shortener(item['title'])
        with open('../corpus/{}-{}.txt'.format(item['date_published'], title), 'w') as f:
            f.write(item['text'])
        print(
            'Got text of {} {}'.format(
                item['date_published'],
                item['title']))
        return item
