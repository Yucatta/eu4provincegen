import csv
import json
import random
provinces = []
with open("regionids.csv",mode="r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        provinces.append(row)
regionareaids = []
regionnames = []
for i,row in enumerate(provinces): 
    temp = []
    # print(row)
    regionnames.append(row[0])
    for j,item in enumerate(row[1:22]):
        if(int(item) or (j==0 and i==0)):
            # print()
            temp.append(int(item))
    regionareaids.append(temp)
diffuculties = []
with open("areadiffuculty.json",mode="r") as f:
    diffuculties = json.load(f)

diffuculties1 = []
with open("regionids.json",mode="r") as f:
    diffuculties1 = json.load(f)

diffucultiesnumbers = []
diffucultiesregions = []
for i,regions in enumerate(diffuculties):
    temp = []
    # temp2 = []
    for j,region in enumerate(regions):
        # temp2.append(regionnames[region])
        # temp.append(region[0])
        # temp+=len(regionareaids[region])
        for area in regionareaids[region]:
            temp.append(area)
        # temp.append(*regionareaids[region])
    diffucultiesnumbers.append(temp)
    # diffucultiesregions.append(temp2)
    diffucultiesnumbers.append(temp)

# for diffucl in diffucultiesnumbers:
#     random.shuffle(diffucl)
print(len(diffucultiesnumbers[0]),len(diffucultiesnumbers[1]),len(diffucultiesnumbers[2]))
with open("areadif.json",mode="w") as f:
    json.dump(diffucultiesnumbers,f,indent=2)
# with open("diffucultynames.json",mode="w") as f:
#     json.dump(diffucultiesregions,f,indent=2)
# print(diffucultiesregions)