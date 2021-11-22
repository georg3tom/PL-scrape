import blink.main_dense as main_dense
import argparse
import json
import copy


models_path = "./models/"

config = {
    "test_entities": None,
    "test_mentions": None,
    "interactive": False,
    "top_k": 10,
    "biencoder_model": models_path + "biencoder_wiki_large.bin",
    "biencoder_config": models_path + "biencoder_wiki_large.json",
    "entity_catalogue": models_path + "entity.jsonl",
    "entity_encoding": models_path + "all_entities_large.t7",
    "crossencoder_model": models_path + "crossencoder_wiki_large.bin",
    "crossencoder_config": models_path + "crossencoder_wiki_large.json",
    "fast": False,  # set this to be true if speed is a concern,
    "show_url": True,
    "output_path": "logs/",  # logging directory
}

args = argparse.Namespace(**config)

models = main_dense.load_models(args, logger=None)

with open("../outputs/player_names_ids.txt", "r") as f:
    names_data = f.read().splitlines()

names = [name.split(": ")[1] for name in names_data]
print(names)

template = {
    "id": 0,
    "label": "unknown",
    "label_id": -1,
    "context_left": "".lower(),
    "mention": "".lower(),
    "context_right": " played in the Premier League".lower(),
}

data_to_link = []
for name in names:
    tmp = copy.deepcopy(template)
    tmp["mention"] = name.lower()
    data_to_link.append(tmp)

(
    _,
    _,
    _,
    _,
    _,
    urls,
    scores,
) = main_dense.run(args, None, *models, test_data=data_to_link)

print(urls, scores)

data = {}
for name, url in zip(names, urls):
    data["name"] = url


with open("../outputs/wikipedia_links.json", "w") as f:

    json.dump(data, f, indent=2, ensure_ascii=False)
