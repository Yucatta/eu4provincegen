import os
import csv
import re

input_folder = os.path.join(os.path.dirname(__file__), "provinces")  # Dynamically locate the 'provinces' folder
output_csv = "provinces.csv"
all_rows = []
def extract_info(file_path):
    with open(file_path, encoding='ISO-8859-1') as f:
        content = f.read()

    # Basic regex patterns
    base_tax = re.search(r'base_tax\s*=\s*(\d+)', content)
    base_prod = re.search(r'base_production\s*=\s*(\d+)', content)
    base_mp = re.search(r'base_manpower\s*=\s*(\d+)', content)
    culture = re.search(r'culture\s*=\s*(\w+)', content)
    religion = re.search(r'religion\s*=\s*(\w+)', content)
    trade_good = re.search(r'(?<!latent_)trade_goods\s*=\s*(\w+)', content)

    development = sum(int(x.group(1)) for x in [base_tax, base_prod, base_mp] if x)
    return {
        "development": development,
        "culture": culture.group(1) if culture else "",
        "religion": religion.group(1) if religion else "",
        "trade_good": trade_good.group(1) if trade_good else ""
    }

with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "Province name", "development", "culture", "religion", "Trade Goods"])

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            match = re.match(r"(\d+)\s*-\s*(.+)\.txt", filename)
            if not match:
                continue
            prov_id, prov_name = match.groups()
            file_path = os.path.join(input_folder, filename)
            info = extract_info(file_path)

            all_rows.append([
            int(prov_id),  # store as int to sort properly
            prov_name.strip(),
            info["development"],
            info["culture"],
            info["religion"],
            info["trade_good"]
        ])

# Sort by the numeric ID before writing
all_rows.sort(key=lambda x: x[0])
print(all_rows)

for i in range(len(all_rows)) :
    for j in range(3,len(all_rows[i])):
        # if
        text = all_rows[i][j]
        if(text == "shamanism"):
            text = "Fetishist"
        elif(text == "tengri_pagan_reformed"):
            text = "Tengri"
        elif(text == "mesoamerican_religion"):
            text = "Mayan"
        elif(text == ""):
            text = "a"
        else:
            text = str(text).replace('_', ' ')
            # text = text.replace('region', '')
            text = ' '.join(word.capitalize() for word in text.split())
        all_rows[i][j] = text

with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "Province name", "development", "culture", "religion", "Trade Goods"])
    for row in all_rows:
        writer.writerow(row)
