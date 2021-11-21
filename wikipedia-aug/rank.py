import json
import math

def tf_idf(documents, word, doc_key):
    tf = documents[doc_key][word]/sum([documents[doc_key][key] for key in documents[doc_key]])
    N = len(documents)
    count = sum([1 if word in documents[key] else 0 for key in documents])
    idf = math.log(N/count)
    return tf/idf
    


def main():
    with open('data_200.json', 'r') as f:
        documents = json.load(f)
    print(tf_idf(documents,'pril',"Andy Thomson"))



if __name__ == "__main__":
    main()
