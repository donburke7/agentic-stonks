# env vars must match partner A’s docker-compose
export POSTGRES_USER=marketrisk
export POSTGRES_PASSWORD=marketrisk
export POSTGRES_DB=marketrisk
export POSTGRES_HOST=127.0.0.1

scrapy crawl feeds -s LOG_FILE=logs/manual_test.log
psql -h 127.0.0.1 -U marketscraper -d marketscraper -c "SELECT count(*) FROM articles;"
