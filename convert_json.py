import json

data = []
with open('./playerData_tmp.json', 'r') as f:
    for obj in f:
        data.append(json.loads(obj))

new_data = {}
for d in data:
    key = list(d.keys())[0]
    new_data[key] = d[key]

with open('./playerData.json', 'w') as f:
    json.dump(new_data, f,indent=4)
