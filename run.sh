#!/bin/bash

mkdir -p outputs
cd scripts

echo "Running name_scanner.py"
python3 name_scanner.py
echo "Done"
echo

echo "Running pl_scraper.py"
python3 pl_scraper.py
echo "Done"
echo

# Call George's scripts here

echo "Running clean_and_stats.py"
python3 clean_and_stats.py
echo "Done"
echo

echo "Running merge.py"
python3 merge.py
echo "Done"

cd ..

cp outputs/final.json ./
