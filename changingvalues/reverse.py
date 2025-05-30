import json
tradenoeds = []
with open("tradenodes.json",mode="r") as f:
    tradenoeds = json.load(f)

tradenoeds.reverse()

print(tradenoeds)

with open("tradenodes.json",mode="w") as f:
    json.dump(tradenoeds,f,indent=2)
