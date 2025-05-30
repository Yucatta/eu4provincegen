import csv
provinces = []
with open("provinces.csv",mode="r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        provinces.append(row)

# print(provinces[4820])
for i in range(len(provinces)) :
    if(provinces[i][3] == "Central Thai"):
        provinces[i][3] ="Siamese"
# print(provinces[4820])

with open("provinces.csv",mode="w",newline="") as f:
    writer = csv.writer(f)
    for row in provinces:
        writer.writerow(row)

        
