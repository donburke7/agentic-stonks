import os, psycopg2, psycopg2.extras
from db.utils import get_db_connection

class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = get_db_connection()
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    # marketscraper/pipelines.py
    def process_item(self, item, spider):
        sql = """
            INSERT INTO articles (url, title, pub_dt, html_raw, source)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
        """
        vals = (
            item["url"],
            item["title"],
            item["pub_dt"],
            item["html_raw"],
            item["source"],
        )
        self.cur.execute(sql, vals)  # ← use plain execute
        return item