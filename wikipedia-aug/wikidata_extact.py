import json

with open('./attr.json', 'r')  as f:
    attrs = json.load(f)['attr']

with open('../PL-Stat-Scrape/wikidata.json', 'r') as f:
    wikidata = json.load(f)

final = {}

for player in wikidata:
    final[player] = {}
    for attr in wikidata[player]:
        if attr in attrs:
            point =  wikidata[player][attr]
            if len(point) == 1:
                point =  wikidata[player][attr][0]
            else:
                point = list(set(wikidata[player][attr]))
            final[player][attr] = point

with open('wikidata_attr_unclean.json', 'w') as f:
    json.dump(final, f)
    

