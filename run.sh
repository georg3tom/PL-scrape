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

echo "Running blink.py"
python3 blink.py
echo "Done"
echo

echo "Running wikipedia-data_map.py"
python3 wikipedia-data_map.py
echo "Done"
echo

echo "Running wikidata_extact.sh"
bash wikidata_extact.sh
echo "Done"
echo


echo "Running clean_and_stats.py"
python3 clean_and_stats.py
echo "Done"
echo

echo "Running merge.py"
python3 merge.py
echo "Done"

cd ..

cp outputs/final.json ./
