# output to attributes based on the score. 
# if score is > 0 then add it to the list

import json


with open("../outputs/rank.json", "r") as f:
    data = json.load(f)


stuff = []

print(len(data))
for d in data:
    stuff.append([data[d]["score"], d])

data = sorted(stuff, reverse=True)


final = {"attr": []}
for d in data:
    if d[0] > 0:
        final["attr"].append(d[1])


with open("../outputs/attr.json", "w") as f:
    json.dump(final, f, ensure_ascii=False, indent=4)
