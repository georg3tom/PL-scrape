import requests
import json
import re
import Stemmer
from collections import Counter
import random

def tf_idf(documents, words):
    pass

def get_content(id):
    url = f"https://en.wikipedia.org/w/api.php?action=query&origin=*&prop=extracts&explaintext&pageids={id}&format=json"
    stemmer = Stemmer.Stemmer('english')
    data = requests.get(url).json()
    content = data['query']['pages'][id]['extract']
    waste = [
        re.compile(r"http.?://(?:[^\s])*"),  # urls
        re.compile(r"(\|[^\|\n\]]*=)"),  # | * =
        re.compile(r"#[0-9a-fA-F]+"),  # hex colors
        re.compile(r"&(?:[^;])*;!?"),  # &**;
        re.compile(r"[^a-z'\s0-9]"),  # non alpha num
        re.compile(r"\b[0-9]+[a-z]+\b"),  # word nums
        re.compile(r"\b[a-z]+[0-9]+\b"),  # word nums
        re.compile(r"\b[\d]{7,}\b"),  # numbers > 7
    ]

    # cleaning
    with open("./data/english", "r") as f:
        stopwords_init = f.read().splitlines()
    stopwords = re.compile(r"\b(" + r"|".join(stopwords_init) + r")\b\s*")
    for ws in waste:
        content = ws.sub(" ", content)
    content = stopwords.sub("", content)
    content = content.split()
    content = stemmer.stemWords(content)
    # print(content)
    return Counter(content)

def main():
    with open('../PL-wiki/new_links.json' ,'r') as f:
        data = json.load(f)

    keys = list(data.keys())
    keys = random.sample(keys,200)
    data_200 = {}
    for name in keys:
        id = data[name].split('=')[-1]
        ret = get_content(id)
        data_200[name] = ret

    with open('data_200.json', 'w') as f:
        json.dump(data_200,f)

if __name__ == "__main__":
    main()
