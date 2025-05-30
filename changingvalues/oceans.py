import csv
provinces = []
with open("provinces.csv",mode="r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        provinces.append(row)

# print(provinces[4820])
oceans = []
for i in range(len(provinces)) :
    if(provinces[i][6] == "Ocean" or provinces[i][6] =="Inland Ocean" ):
        oceans.append([i+1])
        # provinces[i][3] ="Siamese"
# print(provinces[4820])

with open("seatiles.csv",mode="w",newline="") as f:
    writer = csv.writer(f)
    for row in oceans:
        writer.writerow(row)

        
