import scrapy, datetime
from dateutil import parser as dtp
from marketscraper.items import ArticleItem

RSS_FEEDS = {
    #"reuters": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
    "SEC":     "https://www.sec.gov/news/pressreleases.rss",
}

class FeedsSpider(scrapy.Spider):
    name = "feeds"
    allowed_domains = ["sec.gov"]
    start_urls = list(RSS_FEEDS.values())

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.5,
        "ITEM_PIPELINES": {"marketscraper.pipelines.PostgresPipeline": 300},
    }

    def parse(self, response):
        for it in response.xpath("//item"):
            link = it.xpath("link/text()").get().strip()
            title = it.xpath("title/text()").get().strip()
            pub = dtp.parse(it.xpath("pubDate/text()").get())

            item = ArticleItem(  # ← instantiate before Request
                url=link,
                title=title,
                pub_dt=pub,
                source="sec",
            )

            yield scrapy.Request(
                link,
                callback=self.parse_article,
                headers={
                    "User-Agent": "market-risk-bot/0.1 (+mailto:you@example.com)",
                    "Referer": "https://www.sec.gov/",
                },
                meta={"item": item},
            )

    def parse_article(self, response):
        item = response.meta["item"]
        item["html_raw"] = response.text
        yield item