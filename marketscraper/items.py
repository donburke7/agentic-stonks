import scrapy

class ArticleItem(scrapy.Item):
    url      = scrapy.Field()
    title    = scrapy.Field()
    pub_dt   = scrapy.Field()
    html_raw = scrapy.Field()
    source   = scrapy.Field()