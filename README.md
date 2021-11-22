# PL-Wiki Scrape

This project aims to scrape data about past and present Premier League players from the Premier League website and further aguments it by scraping more information about the players from Wikipedia and WikiData.

## File Structure Organization

The files in this project have been well organized. All Python scripts are in the `scripts` folder. Within the `scripts` folder, is another subfolder called `notebooks` that were used for experimenting and data visualization, but aren't needed for running this project. Still, they have been included for completeness.

The `plots` folder contains the plots outputted from the visulziation notebooks.

The `outputs` folder contains output files from most of the scripts. Due the the serial nature of our pipeline, the outputs from one script is generally fed into the next script as an input, so most of the inputs are also taken from this directory.

### `scripts/`

1. `name_scanner.py`: Scans all URLs from `ID_MIN` to `ID_MAX` (set to 0 and 100,000 by default) and checks if there is a valid player page there. If there is a page, it saves `<ID>: <Name>` of that player to `outputs/player_names_ids.txt`. This file contains $6587$ such pairs.

2. `pl_scrape.py`: Takes the ID-Name pairs from `outputs/player_names_ids.txt` and scrapes their respective Overview and Stats page for various attributes. Once it has scraped all the pages and organized their contents, it creates a Pandas Dataframe from the data and writes it to `outputs/uncleaned_pl_scrape.csv`. We've chosen CSV as the intermediate format here since this scrape has a log of numerical data, and it is easier to understand this data in a tabular format, which is easy to generate from a CSV.

3. `clean_and_stats.py`: Takes `outputs/uncleaned_pl_scrape.csv` and `outputs/uncleaned_wiki_scrape.json`, performs quantitative analysis of the data obtained and then cleans them. The plots generated can be saved if required. This script outputs one new JSON file for each of the inputted data files: `outputs/cleaned_pl_scrape.json` and `outputs/cleaned_wiki_scrape.json`.

4. `wikidata_extact.sh`: Attributes are chosen based on a sample of 200 players and their wikipedia entry is used to determine how relevant each attribute is. Following that, the selected attributes are obtained for all players.

5. `merge.py`: Takes the two cleaned JSONs: `outputs/cleaned_pl_scrape.json` and `outputs/cleaned_wiki_scrape.json`, and merges the attributes in them player-wise to generate a dictionary with all the cumulative data from both the scrapes. It then writes this to a file, generating our desired output: `outputs/final.json`.

6. `notebooks/`: As mentioned earlier, this directory contains notebooks that were used for experimenting, intermediate steps, and data visualization. The two `clean_*.ipynb` files have been merged into the `clean_and_stats.py` script, but the `analysis.ipynb` file is a standalone, that was used for data analysis and visualization to be used in the Report.

### `outputs/`

The explanation of these files have already been provided in the above section, but here is a quick overview:

1. `player_names_id.txt`: Stores `<ID>: <Name>` pairs for all the players to be scraped.

2. `uncleaned_pl_scrape.csv`: Stores the raw data obtained by scraping the Premier League website.

3. `uncleaned_wiki_scrape.json`: Stores the raw data obtained by scraping Wikipedia and WikiData sites.

4. `cleaned_pl_scrape.json`: Stores the cleaned data scraped from the Premier League website.

5. `data_200.json`: Stores tokenised wikipedia articles for 200 sample players.

6. `wikidata.json`: Stores Wikidata attributes for all players.

7. `wikipedia_links.json`: Stores Wikipedia article links for all players.

8. `wikidata_map.json`: Stores mappings of Wikipedia articles to WikiData id for all players.

9. `attr.json`: Stores the list of relevant wikidata attributes.

10. `cleaned_wiki_scrape.json`: Stores the cleaned data scraped from Wikipedia and WikiData

11. `final.json`: Stores the cumulative information about all the players from both the scrapes. This is the final output file.

### `plots/`

Contains plots generated for the analysis of the data:

1. `PL_Attribute_Dist_*.png`: Histograms showing the distribution of values across players for each of the numerical attribute obtained from the Premier League website. It has been split into 2 parts for better formatting in the Report.

2. `PL_Attribute_NaN_Percentage.png`: Barchart showing the percentage of entries that are NaN for each attribute in the data scraped from the Premier League website.

3. `Wiki_Attribute_NaN_Percentage.png`: Barchart showing the percentage of entries that are NaN for each attribute in the data scraped from Wikipedia and WikiData.

4. `Attribute_Corr_Matrix.png`: A Heatmap representing the correlation matrix between all the Numerica attributes in the total data collected.

## Running the Pipeline

Since all of our scripts work in a sequential manner, with the output of one feeding into the input another, we have come up with an easy bash script that executes the required Python scripts in order. To run the entire pipeline, just do:

```bash
chmod +x ./run.sh
./run.sh
```

This will run all the scripts and copy `final.json` to the root directory of the project.

*Note: The entire pipleline may take a few hours to run, as the scripts need to make a lot of web request to fetch all the required data.*

*Note: `run.sh` won't generate the plot files, as those files have been manually saved from the notebooks. It will however show the plots in a window, so you can choose to manually save them if you like.*

You can run individual scripts as well if you want, however, it is important that you run them from the `scripts/` directory as the paths for the data files have been written relative to their location from the `scripts/` directory. For example:

**❌ Incorrect**:
```bash
python3 scripts/pl_scraper.py
```

**✔️ Correct**:
```bash
cd scripts
python3 pl_scraper.py
```

`run.sh` already takes this into account, so that can be run directly from the root directory of the project. 
