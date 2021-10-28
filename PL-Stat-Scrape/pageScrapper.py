import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

dump_file = "playerData_tmp2.json"
dump_rate = 10


def premierLeaguePlayerPageScrapper(id, name):
    data = {}
    overviewURL = "https://www.premierleague.com/players/" + \
        str(id) + "/" + name.replace(" ", "-") + "/overview"
    statsURL = "https://www.premierleague.com/players/" + \
        str(id) + "/" + name.replace(" ", "-") + "/stats"
    overviewPage = requests.get(overviewURL)
    overviewSoup = BeautifulSoup(overviewPage.content, "html.parser")
    statsPage = requests.get(statsURL)
    statsSoup = BeautifulSoup(statsPage.content, "html.parser")
    # attributes
    try:
        data['Nationality'] = overviewSoup.find(
            "span", class_="playerCountry").text.strip()
    except:
        print("Nationality not found")
    try:
        data['Date Of Birth'] = overviewSoup.find(
            "ul", class_="pdcol2").find("div", class_="info").text.strip()
    except:
        print("DOB not found")
    try:
        data['Height'] = overviewSoup.find("ul", class_="pdcol3").find(
            "div", class_="info").text.strip()
    except:
        print("Height not found")
    try:
        data['Position'] = overviewSoup.find("section", class_="playerIntro").find(
            "div", class_="info").text.strip()
    except:
        print("Position not found")
    PLStats = statsSoup.find_all("div", class_="normalStat")
    for stat in PLStats:
        try:
            data[stat.find("span", class_="stat").text.split('\n')[0].strip()] = stat.find(
                "span", class_="allStatContainer").text.strip()
        except:
            print("Invalid Row")

    PLStats = statsSoup.find_all("div", class_="topStat")
    for stat in PLStats:
        try:
            data[stat.find("span", class_="stat").text.split('\n')[0].strip()] = stat.find(
                "span", class_="allStatContainer").text.strip()
        except:
            print("Invalid Row")
    return data


def main():

    with open('../NameScanner/names.txt', 'r', encoding="utf-8") as f:
        names_data = f.read().splitlines()

    playerIDs = [line.split(': ')[0] for line in names_data]
    names = [line.split(': ')[1] for line in names_data]

    try:
        with open(dump_file, 'r') as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}
        print("No existing data dump found. Creating dump from scratch...")

    playerData = {}

    for i in tqdm(range(len(playerIDs))):
        if names[i] in cache:
            continue

        playerData[names[i]] = premierLeaguePlayerPageScrapper(
            playerIDs[i], names[i])

        if i > 0 and i % dump_rate == 0:
            with open(dump_file, 'w') as f:
                json.dump(playerData, f)

    with open(dump_file, 'w') as f:
        json.dump(playerData, f)


if __name__ == "__main__":
    main()
