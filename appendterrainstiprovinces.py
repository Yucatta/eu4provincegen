import json
import csv
# json.lo
terrains  =[]
with open("terrains2.json",mode="r") as f:
    terrains = json.load(f)
provinces = []
with open("provinces.csv",mode="r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        # print(reader)
        provinces.append(row)
# print(provinces)
for i in range(0,4940):
    provinces[i].append(terrains[i][1])
# print(provinces)
with open("provinceswithterrains.csv",mode="w",newline="") as f:
    writer = csv.writer(f)
    for line in provinces:
        writer.writerow(line)

    # print("a")