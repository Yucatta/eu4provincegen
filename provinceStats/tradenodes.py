
import json
tradenodes = []
with open("00_tradenodes.txt", 'r', encoding='utf-8') as f:

    isitradenode = False
    isitcolor = False
    nameofnode = False
    para = 0
    for asd in f:
        line = asd.strip()
        
        # Skip empty lines and comments
        # print(asd)
        # print("a")
        temp = []
        words_in_line = line.split() 
        for word in words_in_line:
            
            if(not nameofnode ):
                nameofnode = word.replace("=","").replace("{","").replace("_"," ").title()
            else:
                if(word =="members={"):
                    isitradenode = True
                elif(isitradenode  ):
                    if(word == "}"):
                        para+=1
                    else:
                        temp.append(int(word))
        if(para==2):
            isitradenode = False
            nameofnode = False
            para = 0
        if(len(temp)):
            tradenodes.append([nameofnode,temp])
            # if(word =="")
with open("tradenodes.json",mode="w") as f:
    json.dump(tradenodes,f,indent=2)
# print(tradenodes)