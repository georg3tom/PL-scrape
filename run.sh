#!/bin/bash

mkdir -p outputs

python3 scripts/name_scanner.py
python3 scripts/pl_scraper.py
python3 ./scripts/blink.py
python3 ./scripts/wikipedia-data_map.py
bash ./scripts/wikidata_extact.sh
python3 scripts/clean_and_stats.py
python3 scripts/merge.py

cp outputs/final.json ./
