#!/usr/bin/env bash
# Run the Scrapy spider, then verify that rows were inserted into `articles`.
# Works whether or not you have the `psql` client installed locally.


set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# 1 ) Load DB credentials from .env (if present)
if [[ -f .env ]]; then
  export $(grep -E '^(POSTGRES_USER|POSTGRES_PASSWORD|POSTGRES_DB)=' .env | xargs)
fi
: "${POSTGRES_USER:=marketscraper}"
: "${POSTGRES_PASSWORD:=supersecret}"
: "${POSTGRES_DB:=marketrisk}"

docker exec -it marketrisk_postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c \
  "TRUNCATE TABLE articles;"

# 2 ) Ensure logs/ exists and run the crawler
mkdir -p logs
echo "→ Crawling feeds …"
scrapy crawl feeds -s LOG_FILE="logs/manual_test_$(date +%F_%H%M).log"

# 3 ) Count rows in Postgres
echo "→ Checking row count in database …"
COUNT_CMD="SELECT COUNT(*) FROM articles;"
if command -v psql >/dev/null 2>&1; then
  # Local psql client available
  ROWS=$(PGPASSWORD="$POSTGRES_PASSWORD" \
         psql -h 127.0.0.1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "$COUNT_CMD")
else
  # Fallback: exec into the container (requires docker compose)
  CONTAINER=$(docker compose ps -q db)
  ROWS=$(docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" "$CONTAINER" \
         psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "$COUNT_CMD")
fi

echo "✔  $ROWS rows now in articles table."
[[ "$ROWS" -gt 0 ]] && exit 0 || exit 1
