import json
devs = []
for i in range(3,23):
    if(i%2):
        devs.append(f"{i} - {i+2}")

with open("devs.json",mode="w") as f:
    json.dump(devs,f,indent=2)

