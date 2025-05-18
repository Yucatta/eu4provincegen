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
    # for i in range(57,60):
        # if(i == 58):
        #     mask = Image.new("RGBA", (width, height), (0, 0, 0, 0)) 
        #     for regionid in regionids[i]:
        #             # print()
        #             rgb_color = (land_rgbs["red"][regionid-1], land_rgbs["green"][regionid-1], land_rgbs["blue"][regionid-1])
        #             # print(rgb_color,id)
        #             land_pixels_for_province = land_pixel_data.get(rgb_color, [])
        #             # print(land_pixels_for_province)
        #             if not land_pixels_for_province:
        #                 print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
        #                 continue

        #             graytone = 255 - math.floor((0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])/2)
        #             for j in land_pixels_for_province:
        #                 anotherone = (j[0]-2000,j[1])
        #                 mask.putpixel(anotherone, (graytone, graytone, graytone, 255))
        #     mask.size
        #     bbox = mask.getbbox()
        #     cropped = mask.crop(bbox)
        #     notwidth,notheight = cropped.size
        #     widths.append(notwidth)
        #     heights.append(notheight)
        #     for area in areas[i]:
        #         for j in range(len(states)):
        #             if states[j] == area:
        #                 thatsdumb = []
        #                 for id in ids[j]:
        #                     # print()
        #                     thatsdumb.append(id)
        #                     rgb_color = (land_rgbs["red"][id-1], land_rgbs["green"][id-1], land_rgbs["blue"][id-1])
        #                     # print(rgb_color,id)
        #                     land_pixels_for_province = land_pixel_data.get(rgb_color, [])
        #                     # print(land_pixels_for_province)
        #                     if not land_pixels_for_province:
        #                         print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
        #                         continue
                            
        #                     # graytone = math.floor(0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])
        #                     lightness = (0.2126 * land_rgbs["red"][id-1] + 0.7152 * land_rgbs["green"][id-1] + 0.0722 * land_rgbs["blue"][id-1])/255
        #                     for k in land_pixels_for_province:
        #                         another = (k[0]-2000,k[1])
        #                         mask.putpixel(another, (math.floor(140*lightness),math.floor(140*lightness),255, 255))
                    
        #                 bbox = mask.getbbox()
        #                 cropped = mask.crop(bbox)
        #                 # notwidth,notheight = cropped.size
        #                 # widths.append(notwidth)
        #                 # heights.append(notheight)
        #                 # # Resize and center
        #                 # cropped.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
        #                 # centered = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
        #                 # paste_x = (TARGET_WIDTH - cropped.width) // 2
        #                 # paste_y = (TARGET_HEIGHT - cropped.height) // 2
        #                 # centered.paste(cropped, (paste_x, paste_y))
        #                 # cropped = mask.crop(bbox)
        #                 cropped.save(f"states/{j}.png")
        #                 print(f"Saved states/{j}.png",notwidth,notheight,area,regions[i])
        #                 # print(ids)
        #                 for id in thatsdumb:
        #                     # print()
        #                     rgb_color = (land_rgbs["red"][id-1], land_rgbs["green"][id-1], land_rgbs["blue"][id-1])
        #                     # print(rgb_color,id)
        #                     land_pixels_for_province = land_pixel_data.get(rgb_color, [])
        #                     # print(land_pixels_for_province)
        #                     if not land_pixels_for_province:
        #                         print(f"Warning: No land pixels found for color {rgb_color}. Skipping this province.")
        #                         continue

        #                     graytone = math.floor(0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])
        #                     a = 0
        #                     b = 0
        #                     for k in land_pixels_for_province:
        #                         anotheroneone = (k[0]-2000,k[1])
        #                         a +=k[0]
        #                         b +=k[1]
        #                         mask.putpixel(anotherone, (math.floor(140*lightness),math.floor(140*lightness),255, 255))
        #                     a/=len(ids[j])
        #                     b/=len(ids[j])
        #                     ids[j].append(a)
        #                     ids[j].append(b)
        #                 break
        # else:
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

                # graytone = math.floor(0.299 * rgb_color[0] + 0.587 * rgb_color[1] + 0.114 * rgb_color[2])
                graytone = math.floor(((rgb_color[0] +rgb_color[1]+rgb_color[2])/3*0.9))
                # newred = min(int(rgb_color[1]  + 20),255)
                # newgreen= int(rgb_color[1] *0.8 + 15)
                # newblue = int(rgb_color[1] *0.6 + 10)
                if(i== 58):
                    for j in land_pixels_for_province:
                        mask.putpixel((j[0]-2000,j[1]), (rgb_color[0],rgb_color[1],rgb_color[2], 255))
                else:
                    for j in land_pixels_for_province:
                        mask.putpixel(j, (rgb_color[0],rgb_color[1],rgb_color[2],255))
        mask.size
        bbox = mask.getbbox()
        cropped = mask.crop(bbox)
        notwidth,notheight = cropped.size
        widths.append(notwidth)
        heights.append(notheight)
        for area in areas[i]:
            for j in range(len(states)):
                if states[j] == area:
                    thatsdumb = []
                    a = 0
                    b = 0
                    c = 0
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
                        # lightness = (0.2126 * land_rgbs["red"][id-1] + 0.7152 * land_rgbs["green"][id-1] + 0.0722 * land_rgbs["blue"][id-1])/255
                        newred = int(rgb_color[0] *0.5 + 50*0.5)
                        newgreen= int(rgb_color[1] *0.5 + 100*0.5)
                        newblue = int(rgb_color[2] *0.2 + 255*0.8)
                        
                        if(i ==58):
                            for k in land_pixels_for_province:
                                a +=k[0]
                                b +=k[1]
                                c +=1
                                mask.putpixel((k[0]-2000,k[1]), (rgb_color[0],rgb_color[1],rgb_color[2], 255))
                        else:
                            for k in land_pixels_for_province:
                                a +=k[0]
                                b +=k[1]
                                c +=1
                                mask.putpixel(k, (rgb_color[0],rgb_color[1],rgb_color[2], 255))    
                    a= math.floor(a/c)
                    b= math.floor(b/c)
                    # print(a,b)
                    # equator is 1400 1177
                    # americas asia europa 56S 44 S and 40S  64N and 66N and 72N 
                    # africa 37N 780 35S 2000
                    # asia 9N 140 20N 330 30N 500 40N 660 50N
                    # america 56S 2048 12N 985 64N 0
                    # europa 36N 800 45N 630 54N 445 60N 313 66N 165 72N 0 3650x
                    if(a<2300):
                        if(b<985):
                                b = 12 + (985-b)/985 * 52
                        else:
                            b= (1177-b)/2048 * 68

                    else:
                        if(a<3650 and b<800):
                            b= (800-b)/800 *  36
                        else:
                            b= (1400-b)/2048 * 110
                    a= (2816-a)/2816 * 180
                    anotherpythonL = 7-len(ids[j])
                    for q in range(anotherpythonL):
                        if(anotherpythonL - q== 2):
                            ids[j].append(a)
                        elif(anotherpythonL -q== 1):
                            ids[j].append(b)
                        else:
                            ids[j].append(0)
                    print(ids[j],a,b)
                    
                        
                
                    bbox = mask.getbbox()
                    cropped = mask.crop(bbox)
                    # notwidth,notheight = cropped.size
                    # widths.append(notwidth)
                    # # Resize and center
                    # cropped.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
                    # centered = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
                    # paste_x = (TARGET_WIDTH - cropped.width) // 2
                    # paste_y = (TARGET_HEIGHT - cropped.height) // 2
                    # centered.paste(cropped, (paste_x, paste_y))
                    # cropped = mask.crop(bbox)
                    cropped.save(f"states/{j}.png")
                    print(f"Saved states/{j}.png",notwidth,notheight,area,regions[i])
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

                        graytone = math.floor(((rgb_color[0] +rgb_color[1]+rgb_color[2])/3*0.9))
                        # newred = min(int(rgb_color[1]  + 20),255)
                        # newgreen= int(rgb_color[1] *0.8 + 15)
                        # newblue = int(rgb_color[1] *0.6 + 10)
                        if(i== 58):
                            for j in land_pixels_for_province:
                                mask.putpixel((j[0]-2000,j[1]), (rgb_color[0],rgb_color[1],rgb_color[2], 255))
                        else:
                            for j in land_pixels_for_province:
                                mask.putpixel(j, (rgb_color[0],rgb_color[1],rgb_color[2],255))
                    break



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

widths = []
heights = []
land_pixel_data = extract_land_pixels()
print("Found all land pixels.")
extract_and_resize()


# with open("region_ids.csv", "w", newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     # for region, id in states,ids:
#     for i in range(len(states)):
#         padded_ids = ids[i][:7] + [0] * (7 - len(ids[i]))  # Ensure exactly 6 IDs
#         row = [states[i]] + padded_ids
#         writer.writerow(row)
# print(regions)
# print(areas)
# print(max())
max = 0
index = 0
# for i in range(len(areas)):
#     if(len(areas[i])>max):
#         index = i
#         max = len(areas[i])

# print(max,index,areas[index],regions[index])
regionareasids = []
# for i in range(len(areas)):
#     currentareas = [regions[i]]
#     for j in range(len(areas[i])):
#         for k in range(len(states)):
#             if(areas[i][j]==states[k]):
#                 currentareas.append(k)
#                 break
    # regionareasids.append(currentareas)
    # print(regionareasids[i])

# data = []
# with open('areaids.csv', mode='r', newline='') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         data.append(row)

# Now 'data' is a list of lists

            # newred = int(rgb_color[0] *0.5 + 50*0.5)
            # newgreen= int(rgb_color[1] *0.2 + 255*0.8)
            # newblue = int(rgb_color[2] *0.5 + 100*0.5)