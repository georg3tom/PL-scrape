# Uses SPARQL to scrape the wikidata pages of all players

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import sys
from SPARQLWrapper import SPARQLWrapper, JSON


def get_labels(wd):
    endpoint_url = "https://query.wikidata.org/sparql"
    query_new = (
        """SELECT ?wdLabel ?ps_Label ?wdpqLabel ?pq_Label {
        VALUES (?player) {(wd:"""
        + wd
        + """)}
        ?player ?p ?statement .
        ?statement ?ps ?ps_ .

        ?wd wikibase:claim ?p.
        ?wd wikibase:statementProperty ?ps.

        OPTIONAL {
        ?statement ?pq ?pq_ .
        ?wdpq wikibase:qualifier ?pq .
        }

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    } ORDER BY ?wd ?statement ?ps_"""
    )
    user_agent = "WDQS-example Python/%s.%s" % (
        sys.version_info[0],
        sys.version_info[1],
    )
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query_new)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_wikiData(wd):
    data = {}
    labels = get_labels(wd)["results"]["bindings"]
    for label in labels:
        try:
            attr = label["wdLabel"]["value"]
            value = label["ps_Label"]["value"]
            if attr in data:
                data[attr].append(value)
            else:
                data[attr] = []
                data[attr].append(value)

        except:
            pass
    return data


def main():
    final = {}
    with open("../wikipedia-aug/data_200.json", "r") as f:
        sample = json.load(f)
    full = True
    sample_players = list(sample.keys())
    with open("../wikipedia-aug/wikidata_map.json", "r") as f:
        data = json.load(f)

        for player in tqdm(data):
            if player in sample or full:
                try:
                    final[player] = get_wikiData(data[player])
                except:
                    final[player] = {}
    with open("wikidata.json", "w") as f:
        json.dump(final, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
