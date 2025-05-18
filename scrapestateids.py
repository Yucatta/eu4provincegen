import re
def extract_area_data(filename):
    """
    Parses the file and returns:
    - list of area names (formatted, no '_area', title cased)
    - list of lists containing province IDs for each area
    """
    state_names = []
    province_id_lists = []

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_block = False
    brace_depth = 0
    current_area = None
    buffer = []

    for line in lines:
        m = re.match(r'\s*([a-zA-Z0-9_]+_area)\s*=\s*\{', line)
        if m and not in_block:
            current_area = m.group(1)
            formatted_name = current_area.replace('_area', '').replace('_', ' ').title()
            state_names.append(formatted_name)

            in_block = True
            brace_depth = 1
            buffer = [line.split('{', 1)[1]]
            continue

        if in_block:
            brace_depth += line.count('{')
            brace_depth -= line.count('}')
            buffer.append(line)

            if brace_depth == 0:
                province_lines = [l for l in buffer if re.match(r'^\s*\d+', l)]
                nums = re.findall(r'\b\d+\b', ''.join(province_lines))
                province_id_lists.append([int(n) for n in nums])
                in_block = False

    return state_names, province_id_lists

names, ids = extract_area_data("states.txt")


# if __name__ == "__main__":
#     areas = extract_areas('states.txt')
#     # Now `areas` is your dict. For example, to inspect:
#     print(areas)
#     # for name, provinces in list(areas.items())[:5]:
#     #     print(f"{name} → {provinces}")
#     # print(f"...and {len(areas)} total areas.")

def get_all_rgb(csvloc,emptylands):
    with open(csvloc, encoding="windows-1254", errors="replace") as f:
        csv = pd.read_csv(f, delimiter=';')
    for i in range(len(csv)):
        currentprovinceid = csv.iloc[i,0]
        # if(currentprovinceid>1170 and currentprovinceid<2003):
        #     skip = False
        #     for j in range(0,574):
        #         currentwastelandid = emptylands[j]
        #         if(currentprovinceid ==currentwastelandid):
        #             skip = True
        #             break
        #     if(skip):
        #         continue
        # if(currentprovinceid>2125 and currentprovinceid<2960):
        #     skip = False
        #     for j in range(572,586):
        #         currentwastelandid = emptylands[j]
        #         if(currentprovinceid ==currentwastelandid):
        #             skip = True
        #             break
        #     if(skip):
        #         continue
        # if(currentprovinceid>4130 and currentprovinceid<4950):
        #     skip = False
        #     for j in range(584,len(emptylands)):
        #         currentwastelandid = emptylands[j]
        #         if(currentprovinceid ==currentwastelandid):
        #             skip = True
        #             break
        #     if(skip):
        #         continue
        land_rgbs["id"].append(currentprovinceid)
        land_rgbs["red"].append(csv.iloc[i,1])   
        land_rgbs["green"].append(csv.iloc[i,2])   
        land_rgbs["blue"].append(csv.iloc[i,3]) 
