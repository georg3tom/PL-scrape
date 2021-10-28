import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

def premierLeaguePlayerPageScrapper(id,name):
    data = {}
    overviewURL = "https://www.premierleague.com/players/" + str(id) + "/" + name.replace(" ","-") + "/overview"
    # print(overviewURL)
    statsURL = "https://www.premierleague.com/players/" + str(id) + "/" + name.replace(" ","-") + "/stats"
    overviewPage = requests.get(overviewURL)
    overviewSoup = BeautifulSoup(overviewPage.content, "html.parser")
    statsPage = requests.get(statsURL)
    statsSoup = BeautifulSoup(statsPage.content, "html.parser")
    # attributes
    try:
        data['Nationality'] = overviewSoup.find("span", class_="playerCountry").text.strip()
    except:
        print("Nationality not found")
    try:
        data['Date Of Birth'] = overviewSoup.find("ul", class_="pdcol2").find("div",class_="info").text.strip()
    except:
        print("DOB not found")
    try:
        data['Height'] = overviewSoup.find("ul", class_="pdcol3").find("div",class_="info").text.strip()
    except:
        print("Height not found")
    try:
        data['Position'] = overviewSoup.find("section", class_="playerIntro").find("div",class_="info").text.strip()
    except:
        print("Position not found")
    PLStats = statsSoup.find_all("div", class_="normalStat")
    for stat in PLStats:
        try:
            data[stat.find("span", class_="stat").text.split('\n')[0].strip()] = stat.find("span",class_="allStatContainer").text.strip() 
        except:
            print("Invalid Row")

    PLStats = statsSoup.find_all("div", class_="topStat")
    for stat in PLStats:
        try:
            data[stat.find("span", class_="stat").text.split('\n')[0].strip()] = stat.find("span",class_="allStatContainer").text.strip() 
        except:
            print("Invalid Row")
    return data


with open('./PL-wiki/names.txt', 'r', encoding="utf-8") as f:
    names_data = f.read().splitlines()

playerID = [name.split(': ')[0] for name in names_data]
names = [name.split(': ')[1] for name in names_data]

data = []
with open('playerData_tmp.json', 'r') as f:
    for obj in f:
        data.append(json.loads(obj))
    
cache = []
for d in data:
    cache.append(list(d.keys())[0])

with open('playerData_tmp.json','w') as f:
    for i in tqdm(range(len(playerID))):
        # print(names[i])
        if names[i] in cache:
            continue

        playerData = {}
        playerData[names[i]] = premierLeaguePlayerPageScrapper(playerID[i],names[i])

        f.write(json.dumps(playerData))
        f.write("\n")
