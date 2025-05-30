from pathlib import Path
import json
import re
import csv
from unidecode import unidecode
folder3 = Path("provinces")
pattern = r"^(\d{4})\.(\d{1,2})\.(\d{1,2})$"
# print(countrytags)
capitalos = []
provinces = {}
for k,file in enumerate(folder3.iterdir()):
    if file.is_file():
        with file.open("r", encoding="windows-1254", errors="ignore") as f:
            filename = file.stem
            for asd in f:
                isitowner = False
                line = asd.strip()
                native = False
                colors = []
                words_in_line = line.split() 
                # is
                # wordindex = 0
                for i,word in enumerate(words_in_line):
                    if(word == "fort_15th"):
                        isitowner = True
                        # clean = unidecode(words_in_line[i+2])
                        # clean = clean.replace('"', "").replace("_", "").title()
                        # capitalos.append([filename.split()[0],words_in_line[i+2].replace('"',"").replace("_","").title()])
                        capitalos.append([filename.split()[0],words_in_line[i+2]])
                    else:
                        match = re.match(pattern, word)
                        if match:
                            year = int(match.group(1))
                            if year > 1444 :
                                native = True
                if(native):
                    capitalos.append([filename.split()[0],"no"])
                    break
                if(isitowner ):
                    break
provinces2 = []

with open("provinces4.csv",mode="r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        provinces2.append(row)

for row in capitalos:
    provinces2[int(row[0])-1][7] = row[1]

with open("provinces5.csv",mode="w",newline="")as f:
    writer = csv.writer(f)
    for row in provinces2:
        writer.writerow(row)
# print(capitalos)