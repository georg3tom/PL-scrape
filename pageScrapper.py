import requests
from bs4 import BeautifulSoup
def premierLeaguePlayerPageScrapper(id,name):
    data = {}
    overviewURL = "https://www.premierleague.com/players/" + str(id) + "/" + name.replace(" ","-") + "/overview"
    statsURL = "https://www.premierleague.com/players/" + str(id) + "/" + name.replace(" ","-") + "/stats"
    overviewPage = requests.get(overviewURL)
    overviewSoup = BeautifulSoup(overviewPage.content, "html.parser")
    statsPage = requests.get(statsURL)
    statsSoup = BeautifulSoup(statsPage.content, "html.parser")
    # attributes
    data['Nationality'] = overviewSoup.find("span", class_="playerCountry").text.strip()
    data['Date Of Birth'] = overviewSoup.find("ul", class_="pdcol2").find("div",class_="info").text.strip()
    data['Height'] = overviewSoup.find("ul", class_="pdcol3").find("div",class_="info").text.strip()
    data['Position'] = overviewSoup.find("section", class_="playerIntro").find("div",class_="info").text.strip()
    PLStats = statsSoup.find_all("div", class_="normalStat")
    for stat in PLStats:
        data[stat.find("span", class_="stat").text.split('\n')[0].strip()] = stat.find("span",class_="allStatContainer").text.strip() 
    PLStats = statsSoup.find_all("div", class_="topStat")
    for stat in PLStats:
        data[stat.find("span", class_="stat").text.split('\n')[0].strip()] = stat.find("span",class_="allStatContainer").text.strip() 
    return data

page = premierLeaguePlayerPageScrapper(3513,'Gareth Bale')
print(page)
