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
        # print(csv.iloc[i,0])
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
print(states[184])
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
print(len(emptylands))
print(len(land_rgbs["id"]),len(land_rgbs["red"]),len(land_rgbs["green"]),len(land_rgbs["blue"]))


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
widths = []
heights = []
def extract_and_resize():
    img = Image.open(PROVINCES_BMP_PATH).convert("RGB")
    width, height = img.size
        # for i in range(len(states)):
    # for i in range(len(regions)):
    # for i in range(1):
    #     region_provinces = []  

    #     for area in areas[i]:
    #         for j in range(len(states)):
    #             if states[j] == area:
    #                 region_provinces.extend(ids[j])
    #                 break
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

                graytone = math.floor(0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])
                for j in land_pixels_for_province:
                    mask.putpixel(j, (graytone, graytone, graytone, 255))
        for area in areas[i]:
            for j in range(len(states)):
                if states[j] == area:
                    thatsdumb = []
                    for id in ids[j]:
                         # print()
                        thatsdumb.append(id)
                        rgb_color = (land_rgbs["red"][id-1], land_rgbs["green"][id-1], land_rgbs["blue"][id-1])
                        # print(rgb_color,id)
                        land_pixels_for_province = land_pixel_data.get(rgb_color, [])
                        # print(land_pixels_for_province)
                        if not land_pixels_for_province:
                            print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
                            continue
                        
                        # graytone = math.floor(0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])
                        lightness = (0.2126 * land_rgbs["red"][id-1] + 0.7152 * land_rgbs["green"][id-1] + 0.0722 * land_rgbs["blue"][id-1])/255
                        for k in land_pixels_for_province:
                            mask.putpixel(k, (math.floor(140*lightness),math.floor(140*lightness),255, 255))
                   
                    bbox = mask.getbbox()
                    cropped = mask.crop(bbox)
                    width, height = cropped.size
                    widths.append(width)
                    heights.append(height)
                    # Resize and center
                    cropped.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
                    centered = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
                    paste_x = (TARGET_WIDTH - cropped.width) // 2
                    paste_y = (TARGET_HEIGHT - cropped.height) // 2
                    centered.paste(cropped, (paste_x, paste_y))
                    # cropped = mask.crop(bbox)
                    centered.save(f"states/{j}.png")
                    print(f"Saved states/{j}.png")
                    # print(ids)
                    for id in thatsdumb:
                         # print()
                        rgb_color = (land_rgbs["red"][id-1], land_rgbs["green"][id-1], land_rgbs["blue"][id-1])
                        # print(rgb_color,id)
                        land_pixels_for_province = land_pixel_data.get(rgb_color, [])
                        # print(land_pixels_for_province)
                        if not land_pixels_for_province:
                            print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
                            continue

                        graytone = math.floor(0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])
                        for k in land_pixels_for_province:
                            mask.putpixel(k, (graytone, graytone, graytone, 255))
                    break
        
        # for j in range(len(states)):  # For each state
        #     # graytone = 
        #     for id in ids[j]:  # Each province in that state
        #         # print()
        #         rgb_color = (land_rgbs["red"][id-1], land_rgbs["green"][id-1], land_rgbs["blue"][id-1])
        #         # print(rgb_color,id)
        #         land_pixels_for_province = land_pixel_data.get(rgb_color, [])
        #         # print(land_pixels_for_province)
        #         if not land_pixels_for_province:
        #             print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
        #             continue

        #         graytone = math.floor(0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])
        #         for j in land_pixels_for_province:
        #             mask.putpixel(j, (graytone, graytone, graytone, 255))  # keep original positions for now

        #     # Once all provinces in the state are placed, then crop the total mask
        #     bbox = mask.getbbox()
        #     cropped = mask.crop(bbox)

        #     # Resize and center
        #     cropped.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
        #     centered = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
        #     paste_x = (TARGET_WIDTH - cropped.width) // 2
        #     paste_y = (TARGET_HEIGHT - cropped.height) // 2
        #     centered.paste(cropped, (paste_x, paste_y))
        #     # cropped = mask.crop(bbox)
        #     centered.save(f"states/{j}.png")
        #     print(f"Saved states/{j}.png")

# Run the functions



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
                    region_provinces.extend(ids[j])
                    break  

        regionids.append(region_provinces)
foundidsforregion()
# print(regionids)
# for i in range(len(regions)):             
#         for area in areas[i]:
#             # print(area)
#             for j in range(len(states)):
#                 if states[j] == area:
#                     # print(states[j],area,ids[j])
#                     # print(ids[j])
#                     for id in ids[j]:
#                         print(id-1)

land_pixel_data = extract_land_pixels()
print("Found all land pixels.")
# print(regions[58])
extract_and_resize()
# print(max(widths),max(heights))