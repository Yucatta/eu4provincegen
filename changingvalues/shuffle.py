import random
import json
areas = []
with open("areadi2222f.json",mode="r") as f:
    areas = json.load(f)

for row in areas:
    random.shuffle(row)

with open("areaids.json",mode="w") as f:
    json.dump(areas,f,indent=2)