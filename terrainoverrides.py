


def parse_terrain_txt(file_path):
    terrain_data = {}
    current_terrain_type = None
    in_terrain_override_section = False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            
            # Skip empty lines and comments
            if not stripped_line or stripped_line.startswith('#'):
                continue

            # Check for terrain category start
            if stripped_line.endswith('{'):
                parts = stripped_line.split('=', 1)
                category_name = parts[0].strip()
                if category_name in ["ocean", "inland_ocean", "glacier", "farmlands", "forest", "hills", "woods", "mountain", "impassable_mountains", "grasslands", "jungle", "marsh", "desert", "coastal_desert", "coastline", "drylands", "savannah", "highlands", "dry_highlands", "snow"]:
                    current_terrain_type = category_name
                    print(current_terrain_type)
                    terrain_data[current_terrain_type] = {
                        'type': '',
                        'color': None,
                        'terrain_override': []
                    }
                    in_terrain_override_section = False # Reset for new terrain block
            
            # Check for terrain attributes (like color or type)
            elif current_terrain_type:
                # if 'color = {' in stripped_line:
                #     # Extract color - assuming it's the simple { R G B } or { Index } format
                #     color_str = stripped_line.split('color = {', 1)[1].split('}', 1)[0].strip()
                #     # Convert to tuple of ints if RGB, or single int if indexed
                #     try:
                #         color_values = tuple(map(int, color_str.split()))
                #         if len(color_values) == 1: # Indexed color
                #             terrain_data[current_terrain_type]['color'] = color_values[0]
                #         elif len(color_values) == 3: # RGB color
                #             terrain_data[current_terrain_type]['color'] = color_values
                #     except ValueError:
                #         pass # Handle cases where color format might be unexpected

                # elif 'type =' in stripped_line:
                #     terrain_type_val = stripped_line.split('type =', 1)[1].strip()
                #     # Remove trailing '{' if present
                #     if terrain_type_val.endswith('{'):
                #         terrain_type_val = terrain_type_val[:-1].strip()
                #     terrain_data[current_terrain_type]['type'] = terrain_type_val

                # Check for terrain_override section
                if 'terrain_override = {' in stripped_line:
                    in_terrain_override_section = True
                    
                elif in_terrain_override_section:
                    print("aaa")
                    if '}' in stripped_line and not stripped_line.startswith('}'): # End of section
                        # If '}' is on the same line as the data, process data then end
                        if '}' != stripped_line.strip():
                             province_ids = list(map(int, stripped_line.replace('}', '').strip().split()))
                             terrain_data[current_terrain_type]['terrain_override'].extend(province_ids)
                        in_terrain_override_section = False
                    elif stripped_line == '}': # End of section on its own line
                        in_terrain_override_section = False
                    else: # Inside the terrain_override section
                        for word in line:
                            print(word)
                            # if(word ==)
                        # try:
                        #     province_ids = list(map(int, stripped_line.split()))
                        #     terrain_data[current_terrain_type]['terrain_override'].extend(province_ids)
                        # except ValueError:
                        #     # Handle cases where line might not be pure numbers (e.g., comments inside)
                        #     pass
    return terrain_data

# Example usage:
file_path = 'terrain.txt' # Make sure this path is correct for your file location
parsed_data = parse_terrain_txt(file_path)
print(parsed_data)
# To see all terrain_override entries:
print("Terrain Overrides:")
for terrain_name, data in parsed_data.items():
    if data['terrain_override']:
        print(f"  {terrain_name}: {data['terrain_override']}")