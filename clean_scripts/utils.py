import json

def mergeData(PLFilename,wikifilename):
    with open(PLFilename) as json_file:
        plData = json.load(json_file)
    with open(wikifilename) as json_file:
        wikiData = json.load(json_file)
    common_players = list(set(wikiData.keys()) & set(plData.keys()))
    extra_players = list(set(wikiData.keys()) - set(plData.keys()))
    merged_data = {}
    for player in common_players:
        data = {}
        for attribute in plData[player].keys():
            if attribute.lower() not in data:
                data[attribute.lower()] = plData[player][attribute]
        for attribute in wikiData[player].keys():
            if attribute.lower() not in data:
                data[attribute.lower()] = wikiData[player][attribute]
        merged_data[player] = data
    for player in extra_players:
        merged_data[player] = wikiData[player]
    return merged_data

# a = mergeData('../PL-Stat-Scrape/playerData.json','../wikipedia-aug/wikidata_attr_unclean.json')

# with open('temp.json', 'w') as f:
#     json.dump(a, f, indent=4)
