"""
Taking the text file with ID-Name pairs, outputted from name_scanner.py,
Webscrape each of the pages and collect the available attributes for each
player. Make a Dataframe from it and write it to a CSV, making it easier for
visualizing the data and cleaning it.
"""

import requests
from bs4 import BeautifulSoup as bs4
import json
from tqdm import tqdm
import pandas as pd
import random


"""
This class encapsulates a Player entity and contains all the logic of scraping the required data
from the respective URLs. It stores all the attribute name-value pairs in self.data.
The class also has a static memeber set called attributes that keeps track of all the unique
attributes that have been encountered while fetching all the players from the website.
"""

class Player:

    attributes = {'Nationality', 'Date Of Birth', 'Height',
                  'Position', 'Club', 'Appearances', 'Wins', 'Losses'}

    def __init__(self, name, _id):
        self.name = name
        self.id = _id
        self.overview_url = f"https://www.premierleague.com/players/{self.id}/{self.name.replace(' ','_')}/overview"
        self.stats_url = f"https://www.premierleague.com/players/{self.id}/{self.name.replace(' ','_')}/stats"
        self.data = {'ID': self.id, 'Name': self.name}

    def scrapeStats(self):
        overview_page = requests.get(self.overview_url)
        overview_soup = bs4(overview_page.content, "html.parser")
        stats_page = requests.get(self.stats_url)
        stats_soup = bs4(stats_page.content, "html.parser")

        try:
            self.data['Nationality'] = overview_soup.find(
                "span", class_="playerCountry").text.strip()
        except:
            self.data['Nationality'] = None
        try:
            self.data['Date Of Birth'] = overview_soup.find(
                "ul", class_="pdcol2").find("div", class_="info").text.strip()
        except:
            self.data['Date Of Birth'] = None
        try:
            self.data['Height'] = overview_soup.find("ul", class_="pdcol3").find(
                "div", class_="info").text.strip()
        except:
            self.data['Height'] = None
        try:
            labels = list(map(lambda e: e.text.strip(), overview_soup.find(
                "section", class_="playerIntro").find_all("div", class_="label")))
            infos = list(map(lambda e: e.text.strip(), overview_soup.find(
                "section", class_="playerIntro").find_all("div", class_="info")))
            for key, val in zip(labels, infos):
                self.data[key] = val
        except:
            self.data['Position'] = None
            self.data['Club'] = None

        try:
            self.data["Appearances"] = stats_soup.find(
                "span", class_="statappearances").text.strip()
        except:
            self.data["Appearances"] = None

        try:
            self.data["Wins"] = stats_soup.find(
                "span", class_="statwins").text.strip()
        except:
            self.data["Wins"] = None

        try:
            self.data["Losses"] = stats_soup.find(
                "span", class_="statlosses").text.strip()
        except:
            self.data["Losses"] = None

        stats = stats_soup.find_all(
            "div", class_="normalStat")
        for stat in stats:
            try:
                self.data[stat.find("span", class_="stat").text.split('\n')[0].strip()] = stat.find(
                    "span", class_="allStatContainer").text.strip()
                Player.attributes.add(
                    stat.find("span", class_="stat").text.split('\n')[0].strip())
            except:
                continue

    def __str__(self):
        return f"{self.id}. {self.name} : {self.data}"

    def __doc__(self):
        print("I am a player class")


def main():

    with open('../outputs/player_names_ids.txt', 'r', encoding='utf-8') as f:
        player_list = f.read().splitlines()

    player_ids = [line.split(': ')[0] for line in player_list]
    player_names = [line.split(': ')[1] for line in player_list]

    player_list = [Player(n, i) for (n, i) in zip(player_names, player_ids)]

    for player in tqdm(player_list):
        player.scrapeStats()
    
    """
    Using a Dataframe and exporting to a CSV so it's easier to visualize 
    and later load into the cleaning script.
    """

    df = pd.DataFrame([p.data for p in player_list])
    df.to_csv('../outputs/uncleaned_pl_scrape.csv', index=False)


if __name__ == "__main__":
    main()
