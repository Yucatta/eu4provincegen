import json
# religions = []
# terrains = []
tradegoods = []
with open("tradegoods.json",mode="r") as f:
    tradegoods = json.load(f)

# with open("terrains.json",mode="r") as f:
#     terrains =json.load(f)
# with open("tradegoods.json",mode="r") as f:
#     tradegoods = json.load(f)

for i  in range(len(tradegoods)):
    tradegoods[i] =[tradegoods[i][0],f"rgb({tradegoods[i][1]},{tradegoods[i][2]},{tradegoods[i][3]})"]

with open("tradegoods.json",mode="w") as f:
    json.dump(tradegoods,f,indent=2)