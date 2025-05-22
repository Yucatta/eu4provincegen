
import json

def parse_terrain_txt(file_path):
    # terrain_data = {}
    current_terrain_type = None
    in_terrain_override_section = 0
    terrain_data = []
    another = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for asd in f:
            line = asd.strip()
            
            # Skip empty lines and comments
            # print(asd)
            # print("a")
            words_in_line = line.split() 

            for word in words_in_line:
                # print(word)
                # print(word)
                if "#" in word: 
                    break
                # print("a")
                if word in ["ocean", "inland_ocean",
                            "glacier", "farmlands"
                            , "forest", "hills", "woods",
                            "mountain", "grasslands", "jungle"
                            , "marsh", "desert", "coastal_desert",
                            "coastline", "drylands", "savannah",
                            "highlands", "dry_highlands", "snow",
                            "steppe"]:
                    # progressdata.append([word])
                    current_terrain_type = word
                    print(current_terrain_type.replace("_"," ").title())
                    break
                elif(word == "color"):
                    in_terrain_override_section = 1
                elif(in_terrain_override_section and word == "}"):
                    in_terrain_override_section = 0
                    # print(another)
                    terrain_data.append([[current_terrain_type.replace("_"," ").title()],another])
                    another = []
                    # print(terrain_data)
                elif(in_terrain_override_section and word != "=" and word != "{"):
                    # print(word)
                    # print(word,another)
                    another.append(int(word))
                    # terrain_data.append([word,current_terrain_type.replace("_"," ").title()])
     
    return terrain_data

# Example usage:
file_path = 'modifiedterrain.txt' # Make sure this path is correct for your file location
parsed_data = parse_terrain_txt(file_path)
# print(parsed_data)
# To see all terrain_override entries:
print("Terrain Overrides:")
# for line in parsed_data:
    # print(line[0],line[1])
    # if data['terrain_override']:
    #     print(f"  {terrain_name}: {data['terrain_override']}")

with open("terraincolors.json",mode="w") as f:
    json.dump(parsed_data,f,indent=2)