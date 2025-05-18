import re
import csv
import io

def parse_cultures_file(file_content_to_parse):
    culture_data = {}
    current_group = None
    # brace_level tracks nesting for the current_group or a top-level ignorable block
    brace_level = 0 
    
    # Keywords for properties/blocks to ignore for name extraction
    properties_to_ignore_for_extraction = [
        "graphical_culture", "second_graphical_culture", "male_names", 
        "female_names", "dynasty_names", "country", "province", "primary",
        "texture_sheet", "sprite_level", "modifier", "color", "sprite", "sound_type",
        "second_texture_sheet", "graphical_culture_sub_group",
        "uses_texture_sheet_from_group", "sprite_sheet_level", "graphical_culture_group",
        "country_modifier", "province_modifier", "heritages", "heritage"
        # Add any other specific block names that are properties and not cultures/groups
    ]

    lines = file_content_to_parse.splitlines()
    
    for line_number, line_text in enumerate(lines):
        line = line_text.strip()
        if not line or line.startswith('#'): # Skip empty lines and comments
            continue

        # Try to match "name = {" pattern, which can be a group, culture, or property block
        match = re.match(r'^([a-zA-Z0-9_]+)\s*=\s*\{', line)

        if match:
            potential_name = match.group(1)
            
            if not current_group and brace_level == 0: # We are at the top level, looking for a culture group
                if potential_name not in properties_to_ignore_for_extraction:
                    current_group = potential_name
                    culture_data[current_group] = []
                    brace_level = line.count('{') - line.count('}') # Start brace count for this group
                    if brace_level <= 0: # Handles one-liners like group = {} correctly
                        current_group = None 
                        brace_level = 0
                else:
                    # This is a top-level property block (e.g., male_names = {} at global scope, if any)
                    # Start counting its braces so we can skip it.
                    brace_level = line.count('{') - line.count('}')
                    if brace_level <= 0: brace_level = 0 # Handled one-liner property
            
            elif current_group and brace_level > 0: # We are inside a group block, looking for cultures or property blocks
                if potential_name not in properties_to_ignore_for_extraction:
                    # This is a culture name within the current group
                    if current_group in culture_data: # Should always be true
                         culture_data[current_group].append(potential_name)
                # Regardless if it's a culture or an ignored property block (like male_names within a group),
                # we update the brace_level for the *current_group's* scope or the property block we are traversing.
                brace_level += line.count('{') 
                brace_level -= line.count('}') # Account for closing brace on the same line
                
                if brace_level <= 0 and current_group: # If this line closed the current_group block
                    current_group = None
                    brace_level = 0
            
            elif brace_level > 0: # Inside a top-level property block we are skipping
                brace_level += line.count('{') 
                brace_level -= line.count('}')
                if brace_level <= 0: brace_level = 0 # Exited the property block

        elif brace_level > 0: # Line does not start a definition, but we are inside some block
            brace_level += line.count('{')
            brace_level -= line.count('}')
            if brace_level <= 0: # Exited the current block (either group or property block)
                if current_group: # If it was a group, nullify it
                    current_group = None
                brace_level = 0 # Reset brace level
            
    return culture_data

file_content = ""
try:
    with open("00_cultures.txt", "r", encoding='ISO-8859-1') as f: # utf-8-sig handles potential BOM
        file_content = f.read()
except FileNotFoundError:
    print("Error: 00_cultures.txt not found. Please place it in the same directory as the script.")
except Exception as e:
    print(f"Error reading 00_cultures.txt: {e}")

if file_content:
    parsed_data = parse_cultures_file(file_content)
    print(parsed_data)
    output = io.StringIO()
    writer = csv.writer(output)

    max_cultures = 0
    if parsed_data:
        # Filter out groups that might have been created but ended up with no cultures
        # and ensure cultures within a group are unique and sorted.
        parsed_data_filtered = {
            group: sorted(list(set(cultures))) 
            for group, cultures in parsed_data.items() if cultures
        }
        if parsed_data_filtered:
             max_cultures = max(len(cultures) for cultures in parsed_data_filtered.values())
        else:
            parsed_data_filtered = {} # Ensure it's an empty dict if all groups were empty
    else:
        parsed_data_filtered = {}

    header = ["Culture Group"]
    if max_cultures > 0:
        header.extend([f"Culture_{i+1}" for i in range(max_cultures)])
    writer.writerow(header)

    # Sort group names for consistent CSV output
    sorted_group_names = sorted(parsed_data_filtered.keys())

    for group_name in sorted_group_names:
        cultures_in_group = parsed_data_filtered[group_name] # Already sorted and unique
        row_data = [group_name] + cultures_in_group
        if max_cultures > 0: # Pad with empty strings if necessary
            row_data.extend([""] * (max_cultures - len(cultures_in_group)))
        writer.writerow(row_data)

    csv_content_output = output.getvalue()
    output.close()

    # Print CSV content to console
    print("\n--- CSV Output ---")
    # print(csv_content_output)
    
    try:
        with open("parsed_cultures_from_file.csv", "w", newline="", encoding="utf-8") as f:
            f.write(csv_content_output)
        print("\nCSV file 'parsed_cultures_from_file.csv' created successfully in the script's directory.")
    except Exception as e:
        print(f"\nError saving CSV to file: {e}")
        print("Please copy the CSV data printed above.")

elif not file_content and "FileNotFoundError" not in str(globals().get("e", "")): 
    # This condition might not be hit if FileNotFoundError above exits or if file_content remains ""
    print("Error: File content for '00_cultures.txt' is empty or another reading error occurred before parsing.")