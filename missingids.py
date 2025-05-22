import json

# json.lo
terrains  =[]
with open("terrains2.json",mode="r") as f:
    terrains = json.load(f)
alreadyfoundids = []
duplicateids = []
skippingids = []
currentcount = 0
for i in range(0,4960):
    if(i<3003 or i>4018):
        print(i)
        # print(alreadyfoundids)
        if ( currentcount>0  ):
            if(terrains[i][0] - alreadyfoundids[currentcount-1] !=1):
                skippingids.append(terrains[i][0])
        if terrains[i] not in alreadyfoundids:
            alreadyfoundids.append(terrains[i][0])
            currentcount+=1
        else:
            duplicateids.append(terrains[i][0])
        
            
print(duplicateids)
print(skippingids)