import json
import requests
from tqdm import tqdm



def main():
    with open('../PL-wiki/new_links.json', 'r') as f:
        documents = json.load(f)
    data_map = { }

    for name in tqdm(documents):
        try:
            id = documents[name].split('=')[-1]
            url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&pageids={id}&format=json"
            data = requests.get(url).json()
            data_map[name] = data['query']['pages'][id]['pageprops']['wikibase_item']
        except:
            data_map[name] = None


    with open('wikidata_map.json', 'w') as f:
        json.dump(data_map,f)



if __name__ == "__main__":
    main()
