import json
uncolonized = []
with open("uncolonized.json",mode="r") as f:
    uncolonized = json.load(f)

for i,item in enumerate(uncolonized):
    uncolonized[i] = int(item)

with open("uncolonized2.json",mode="w") as f:
    json.dump(uncolonized,f,indent=2)