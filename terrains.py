from PIL import Image
import pandas as pd
import csv
import math
import json

PROVINCES_BMP_PATH = "provinces.bmp"
DEFINITION_CSV_PATH = "definition.csv"
emptylands_path = "emptylands.csv"

emptylands = []
land_rgbs = {
    "id":[],
    "red":[],
    "green":[],
    "blue":[],
}
import re
def get_all_empty_lands(csvloc):
    csv = pd.read_csv(f"{csvloc}")
    for i in range(len(csv)):
        emptylands.append(csv.iloc[i,0])
get_all_empty_lands(emptylands_path)
def extract_area_data(filename):
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
            state_names.append(current_area)

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

states, ids = extract_area_data("states.txt")

def get_all_rgb(csvloc,emptylands):
    with open(csvloc, encoding="windows-1254", errors="replace") as f:
        csv = pd.read_csv(f, delimiter=';')
    for i in range(len(csv)):
        currentprovinceid = csv.iloc[i,0]
        land_rgbs["id"].append(currentprovinceid)
        land_rgbs["red"].append(csv.iloc[i,1])   
        land_rgbs["green"].append(csv.iloc[i,2])   
        land_rgbs["blue"].append(csv.iloc[i,3])   

get_all_rgb(DEFINITION_CSV_PATH,emptylands)


def extract_land_pixels():
    PROVINCES_BMP_PATH = "provinces.bmp"
    land_colors = set(zip(land_rgbs["red"], land_rgbs["green"], land_rgbs["blue"]))
    img = Image.open(PROVINCES_BMP_PATH).convert("RGB")
    width, height = img.size
    land_pixels = {color: [] for color in land_colors}
    def is_land_pixel(pixel):
        return pixel in land_colors
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if is_land_pixel(pixel):
                land_pixels[pixel].append((x, y))

    return land_pixels

def extract_and_resize():
    img = Image.open(PROVINCES_BMP_PATH).convert("RGB")
    width, height = img.size
    for i in range(len(regions)):
        mask = Image.new("RGBA", (width, height), (0, 0, 0, 0)) 
        for regionid in regionids[i]:
                # print()
                rgb_color = (land_rgbs["red"][regionid-1], land_rgbs["green"][regionid-1], land_rgbs["blue"][regionid-1])
                # print(rgb_color,id)
                land_pixels_for_province = land_pixel_data.get(rgb_color, [])
                # print(land_pixels_for_province)
                if not land_pixels_for_province:
                    print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
                    continue

                if(i== 58):
                    for j in land_pixels_for_province:
                        mask.putpixel((j[0]-2000,j[1]), (40,40,40, 255))
                else:
                    for j in land_pixels_for_province:
                        mask.putpixel(j, (40,40,40,255))
        mask.size
        bbox = mask.getbbox()
        bboxes.append(bbox)
        print(bbox)
        # cropped = mask.crop(bbox)
        # notwidth,notheight = cropped.size
        # widths.append(notwidth)
        # heights.append(notheight)
        mask.save(f"fullmapregion/{i}.png")
        print(f"fullmapregion/{i}.png",regions[i])
        # for area in areas[i]:
        #     for j in range(len(states)):
        #         if states[j] == area:
        #             thatsdumb = []
        #             for id in ids[j]:
        #                 # print()
        #                 thatsdumb.append(id)
        #                 rgb_color = (land_rgbs["red"][id-1], land_rgbs["green"][id-1], land_rgbs["blue"][id-1])
        #                 # print(rgb_color,id)
        #                 land_pixels_for_province = land_pixel_data.get(rgb_color, [])
        #                 # print(land_pixels_for_province)
        #                 if not land_pixels_for_province:
        #                     print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
        #                     continue
        #                 if(i ==58):
        #                     for k in land_pixels_for_province:
        #                         mask.putpixel((k[0]-2000,k[1]), (rgb_color[0],rgb_color[1],rgb_color[2], 255))
        #                 else:
        #                     for k in land_pixels_for_province:
        #                         mask.putpixel(k, (rgb_color[0],rgb_color[1],rgb_color[2], 255))    
                    
                    
                        
                
        #             bbox = mask.getbbox()
        #             cropped = mask.crop(bbox)
        #             # print(ids)
        #             for id in thatsdumb:
        #                 # print()
        #                 rgb_color = (land_rgbs["red"][id-1], land_rgbs["green"][id-1], land_rgbs["blue"][id-1])
        #                 # print(rgb_color,id)
        #                 land_pixels_for_province = land_pixel_data.get(rgb_color, [])
        #                 # print(land_pixels_for_province)
        #                 if not land_pixels_for_province:
        #                     print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
        #                     continue

        #                 graytone = math.floor(((rgb_color[0] +rgb_color[1]+rgb_color[2])/3*0.9))
        #                 # newred = min(int(rgb_color[1]  + 20),255)
        #                 # newgreen= int(rgb_color[1] *0.8 + 15)
        #                 # newblue = int(rgb_color[1] *0.6 + 10)
        #                 if(i== 58):
        #                     for j in land_pixels_for_province:
        #                         mask.putpixel((j[0]-2000,j[1]), (rgb_color[0],rgb_color[1],rgb_color[2], 255))
        #                 else:
        #                     for j in land_pixels_for_province:
        #                         mask.putpixel(j, (rgb_color[0],rgb_color[1],rgb_color[2],255))
        #             break



def extract_regions_and_areas(file_path):
    regions = []
    areas = []

    current_region = None
    current_area_list = []
    block_stack = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue  # skip empty or comment lines

            if line.endswith("= {"):
                key = line.split("=")[0].strip()

                if current_region is None:
                    current_region = key
                    regions.append(current_region)
                    current_area_list = []

                block_stack.append(key)

            elif line == "}":
                if block_stack:
                    popped = block_stack.pop()
                    if popped == "areas":
                        areas.append(current_area_list)
                    elif popped == current_region and not block_stack:
                        current_region = None

            elif block_stack and block_stack[-1] == "areas":
                current_area_list.append(line)

    return regions, areas
regionids = []
regions, areas = extract_regions_and_areas("region.txt")

def foundidsforregion():
    for i in range(len(regions)):
        region_provinces = []  

        for area in areas[i]:
            for j in range(len(states)):
                if states[j] == area:
                    # print(area,states[j])
                    region_provinces.extend(ids[j])
                    break  

        regionids.append(region_provinces)
foundidsforregion()

def findterrain():
    img = Image.open("terrain.bmp").convert("RGB")
    # width, height = img.size
    # for i in range(len(regions)):
    for regionid in range(1,4941):
        if regionid in overwrittenids:
            continue
        # print()
        rgb_color = (land_rgbs["red"][regionid-1], land_rgbs["green"][regionid-1], land_rgbs["blue"][regionid-1])
        land_pixels_for_province = land_pixel_data.get(rgb_color, [])
        if not land_pixels_for_province:
            # print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
            continue
        pixelcolors = [0,0,0,0,0,0,0,0,0,0,0]
        for j in range(len(colors)):
            correctpixelcount = 0
            wrongterrain = 0
            for pixel in land_pixels_for_province:
                # if(wrongterrain == len(colors[j])):
                #     break
                for color in colors[j]:
                    if(color != img.getpixel(pixel)):
                        # print(color)
                        wrongterrain+=1
                        continue
                    pixelcolors[j]+=1
                    # correctpixelcount+=1
                    
            # if(regionid == 1):
            #     print(correctpixelcount,len(land_pixels_for_province))
            #     print(correctpixelcount,terrainnames[j],j,regionid,len(land_pixels_for_province))
        # pixelcolors.index(max(pixelcolors))
            # if(correctpixelcount >= len(land_pixels_for_province)*1/2):
        # if(regionid ==1 ):
        #     print(land_pixels_for_province)
        print(pixelcolors,regionid,terrainnames[ pixelcolors.index(max(pixelcolors))])
        provinceterrains.append([regionid,terrainnames[ pixelcolors.index(max(pixelcolors))]])
            #     break

        if(not regionid%100):        
            print(regionid)
                
        # cropped = mask.crop(bbox)
        # notwidth,notheight = cropped.size
        # widths.append(notwidth)
        # heights.append(notheight)
        # print(f"fullmapregion/{i}.png",regions[i])




widths = []
heights = []
bboxes = []
colors = [  [(86,124,27),(200,214,107),(13,96,62)],[(0,86,6),(53,77,17)],[(112,74,31),(65,42,17)],
          [(206,169,99),(158,130,77)],[(75,147,174)],[(155,155,155)],[(42,55,22),(213,144,199),(127,24,60)],
          [(8,31,130)],[(55,90,220)],[(203,191,103)],
         [{255,247,0}]]

terrainnames = ["Grassland","Hills","Mountain",
                "Desert","Marsh","Farmlands","Forest",
                "Ocean","Inland Ocean","Coastal Desert",
               "Coastline"]
normalarray = []
a = []
with open ("modifiedoverwrittenids.json",mode="r") as f:
    a = json.load(f)
    # for line in f:
overwrittenids = []
overwritten = []
for line in a:
    overwritten.append([int(line[0]),line[1]])
    



# print(overwrittenids)
provinceterrains = []
# print((86, 124, 47)==(86,124,47))
# land_pixel_data = extract_land_pixels()
# print("found all pixels")
# # land_pixels_for_province = land_pixel_data.get((128,34,64), [])
# findterrain()
# print(provinceterrains)

with open("provinceterrain.json",mode="w")as f:
    json.dump(provinceterrains,f,indent=2)

parsed_data = []
with open ("provinceterrains.json",mode="r") as f:
    parsed_data = json.load(f)

for line in overwritten:
    parsed_data.append(line)

for line in normalarray:
    parsed_data.append([int(line[0]),line[1]])

parsed_data.sort(key=lambda x: x[0])

with open("terrains2.json",mode="w") as f:
    json.dump(parsed_data,f,indent=2)
