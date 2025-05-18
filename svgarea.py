from PIL import Image
import pandas as pd
import cv2
import numpy as np
import csv
import math

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
# def get_all_empty_lands(csvloc):
#     csv = pd.read_csv(f"{csvloc}")
#     for i in range(len(csv)):
#         emptylands.append(csv.iloc[i,0])
# get_all_empty_lands(emptylands_path)
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

def turnsvg():
    img = Image.open(f"provinces.bmp").convert("RGB")
    for i in range(0,4938):
        # for id in ids[i]:
        # mask = rgb_mask(img, rgb)
        rgb_color = (land_rgbs["red"][i], land_rgbs["green"][i], land_rgbs["blue"][i])
        # newred = min(int(rgb_color[1]  + 20),255)
        # newgreen= int(rgb_color[1] *0.8 + 15)
        # newblue = int(rgb_color[1] *0.6 + 10)
        mask = rgb_mask(img, rgb_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        svg_paths = [contour_to_svg_path(c) for c in contours]

        save_svg(svg_paths, img.width, img.height,f"fullmap/{i}.svg")
        print(f"fullmap/{i}.svg")

    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # svg_paths = [contour_to_svg_path(c) for c in contours]

    # print("SVG saved as province.svg")




def rgb_mask(image, rgb_color):
    data = np.array(image)
    return (np.all(data == rgb_color, axis=-1).astype(np.uint8)) * 255

def contour_to_svg_path(contour):
    points = contour.squeeze()
    path_data = "M " + " L ".join(f"{x},{y}" for x, y in points) + " Z"
    return f'<path d="{path_data}" fill="none" stroke="black" stroke-width="1"/>'

def save_svg(paths, width, height, filename):
    with open(filename, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
        for path in paths:
            f.write(f"  {path}\n")
        f.write("</svg>")

turnsvg()
# print(areas,states)
# print(ids)
# --- Main Example ---
# img = Image.open("provinces.bmp").convert("RGB")
# mask = rgb_mask(img, rgb)
# print(mask)
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# svg_paths = [contour_to_svg_path(c) for c in contours]

# save_svg(svg_paths, img.width, img.height)
# print("SVG saved as province.svg")
