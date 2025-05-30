import json,csv

provinces = []
provinces2 = []
with open("main3.csv",mode="r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        provinces.append(row)
with open("provinces2.csv",mode="r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        provinces2.append(row)


# print(provinces[0:100])
# print(provinces[5][0:6])
# for i,province in enumerate(provinces2):
#     for j in range(8,12):
#         province.append(provinces[i][j])
    # province.append(*provinces[i][8:11])
numberofmon = 0
# print(not not "")
# locations = []
# for row in provinces:
#     # if()
#     if(row[11] and int(row[11])):
#         numberofmon += int(row[11])
#         # locations.append(row[1])
# # print(numberofmon)
# # print(locations)
for row in provinces2:
    if(row[9] == "na"):
        row[9] = "0"
# print(provinces2)
    # newlist.append([int(province[0]),*province[1:14]])
    # print(provinces[i])

with open("provinces3.csv",mode="w",newline="") as f:
    writer = csv.writer(f)
    for row in provinces2:
        writer.writerow(row)
# print(newlist[0:40])