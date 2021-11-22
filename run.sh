#!/bin/bash

mkdir -p outputs

python3 scripts/name_scanner.py
python3 scripts/pl_scraper.py
# Call George's scripts here
python3 scripts/clean_and_stats.py
python3 scripts/merge.py

cp outputs/final.json ./