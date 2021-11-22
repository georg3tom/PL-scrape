"""
This script takes the two cleaned JSONs: the PL scrape and the Wiki scrape
and merges them into one complete JSON, giving the final output of the 
pipeline: final.json
"""

import json

"""
Function that merges the attributes from the two JSONs for each player
and returns a new dictionary with the accumulated data
"""


def mergeData(PLFilename, wikifilename):
    with open(PLFilename, 'r', encoding='utf-8') as json_file:
        plData = json.load(json_file)
    with open(wikifilename, 'r', encoding='utf-8') as json_file:
        wikiData = json.load(json_file)
    common_players = list(set(wikiData.keys()) & set(plData.keys()))
    extra_players = list(set(wikiData.keys()) - set(plData.keys()))
    merged_data = {}
    for player in common_players:
        data = {}
        for attribute in plData[player].keys():
            if attribute not in data:
                data[attribute] = plData[player][attribute]
        for attribute in wikiData[player].keys():
            if attribute not in data:
                data[attribute] = wikiData[player][attribute]
        merged_data[player] = data
    for player in extra_players:
        merged_data[player] = wikiData[player]
    return merged_data


def main():
    mergedData = mergeData('../outputs/cleaned_pl_scrape.json',
                           '../outputs/cleaned_wiki_scrape.json')

    with open('../outputs/final.json', 'w', encoding='utf-8') as f:
        json.dump(mergedData, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
