# extract just the relevant attributes for all players from the wikidata entries

import json

with open("../outputs/attr.json", "r") as f:
    attrs = json.load(f)["attr"]

with open("../outputs/wikidata.json", "r") as f:
    wikidata = json.load(f)

final = {}

for player in wikidata:
    final[player] = {}
    for attr in wikidata[player]:
        if attr in attrs:
            point = wikidata[player][attr]
            if len(point) == 1:
                point = wikidata[player][attr][0]
            else:
                point = list(set(wikidata[player][attr]))
            final[player][attr] = point


with open("../outputs/uncleaned_wiki_scrape.json", "w") as f:

    json.dump(final, f, ensure_ascii=False, indent=4)
