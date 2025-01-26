#!/bin/bash

FIRST_RUN_DELAY=$((30 * 24 * 60 * 60))

run_scraper() {
    echo "$(date) - Start scrapowania" >> /var/log/scraper.log
    python /app/scraper.py >> /var/log/scraper.log 2>&1
    echo "$(date) - Koniec scrapowania" >> /var/log/scraper.log
}

sleep $FIRST_RUN_DELAY
run_scraper

while true; do
    sleep $((30 * 24 * 60 * 60))
    run_scraper
done