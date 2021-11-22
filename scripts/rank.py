import json
import math
import re
import Stemmer

def tf_idf(documents, word, doc_key):
    tff = tf(documents, word, doc_key)
    N = len(documents)
    count = sum([1 if word in documents[key] else 0 for key in documents])
    idf = math.log(N/count)
    return tff/idf

def tf(documents, word, doc_key):
    try:
        return documents[doc_key][word]/sum([documents[doc_key][key] for key in documents[doc_key]])
    except:
        return 0

def clean_tok(content):
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
    content = content.lower()

    stemmer = Stemmer.Stemmer('english')
    with open("./data/english", "r") as f:
        stopwords_init = f.read().splitlines()
    stopwords = re.compile(r"\b(" + r"|".join(stopwords_init) + r")\b\s*")
    for ws in waste:
        content = ws.sub(" ", content)
    content = stopwords.sub("", content)
    content = content.split()
    content = stemmer.stemWords(content)
    return content


def main():
    with open('../outputs/data_200.json', 'r') as f:
        documents = json.load(f)
    with open('../outputs//wikidata_200.json', 'r') as f:
        wikidata = json.load(f)

    attributes = {}
    for player in wikidata:
        for attr in wikidata[player]:
            attributes[attr] = {'score':0, 'in_players': 0, 'in_wikipedia': 0}

    for player in wikidata:
        for attr in wikidata[player]:
            clean = clean_tok(" ".join(list(set(wikidata[player][attr]))))
            print(wikidata[player][attr])
            print(clean,'\n')
            for tok in clean:
                if tf(documents, tok,player) > 0:
                    attributes[attr]['in_wikipedia'] += 1
                    break
            
            attributes[attr]['in_players'] += 1

    for attr in attributes:
        attributes[attr]['score'] =  attributes[attr]['in_wikipedia']/attributes[attr]['in_players']


    with open('../outputs/rank.json','w') as f:
        json.dump(attributes, f)



if __name__ == "__main__":
    main()
