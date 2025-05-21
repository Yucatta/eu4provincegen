from PIL import Image
import pandas as pd
import csv
import math

PROVINCE_ID = 4779  
PROVINCES_BMP_PATH = "provinces.bmp"
DEFINITION_CSV_PATH = "definition.csv"
OUTPUT_IMAGE_PATH = f"province_{PROVINCE_ID}.png"
emptylands_path = "emptylands.csv"

TARGET_WIDTH, TARGET_HEIGHT = 800 , 600
emptylands = []
land_rgbs = {
    "id":[],
    "red":[],
    "green":[],
    "blue":[],
}
import re
def get_all_empty_lands(csvloc):
    # with open(csvloc, encoding="windows-1254", errors="replace") as f:
    #     csv = pd.read_csv(f, delimiter=';')
    csv = pd.read_csv(f"{csvloc}")
    for i in range(len(csv)):
        emptylands.append(csv.iloc[i,0])
get_all_empty_lands(emptylands_path)
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
            # formatted_name = current_area.replace('_area', '').replace('_', ' ').title()
            # state_names.append(formatted_name)
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
    for i in range(oceanea):
        mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))     
        for j in range(len(ids[i])):
            rgb_color = (land_rgbs["red"][ids[i][j]-1], land_rgbs["green"][ids[i][j]-1], land_rgbs["blue"][ids[i][j]-1])
            # print(rgb_color,id)
            land_pixels_for_province = land_pixel_data.get(rgb_color, [])
            # print(land_pixels_for_province)
            if not land_pixels_for_province:
                print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
                continue
            # newred = int(rgb_color[0] *0.5 + 50*0.5)
            # newgreen= int(rgb_color[1] *0.5 + 100*0.5)
            # newblue = int(rgb_color[2] *0.2 + 255*0.8)
            newred = int(rgb_color[0] *0.5 + 50*0.5)
            newgreen= int(rgb_color[1] *0.2 + 255*0.8)
            newblue = int(rgb_color[2] *0.5 + 100*0.5)
            if i in {329, 344, 330, 327, 328, 345, 346, 347, 342, 343}:
                for k in land_pixels_for_province:
                    mask.putpixel((k[0]-2000,k[1]), (rgb_color[0],rgb_color[1],rgb_color[2], 255))
            else:
                for k in land_pixels_for_province:
                    mask.putpixel(k, (rgb_color[0],rgb_color[1],rgb_color[2], 255)) 
        # bbox = mask.getbbox()
        # print(bbox)
        mask.save(f"fullmapsinglecolorstates/{i}.png")
        print(f"fullmapsinglecolorstates/{i}.png saved")
       



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
# print(ids)
widths = []
heights = []
oceanea = [344,329,330,327,328,345,346,347,342,343]
land_pixel_data = extract_land_pixels()
print("Found all land pixels.")
extract_and_resize()

