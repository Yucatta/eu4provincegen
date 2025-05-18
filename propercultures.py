import csv
import re

def clean_and_capitalize_text(text):
    """
    Cleans and capitalizes text according to specified rules.
    1. Removes '_new'.
    2. Removes '_culture'.
    3. Replaces '_' with a space.
    4. Capitalizes the start of each word (title case).
    5. Cleans up multiple spaces.
    """
    if not isinstance(text, str):
        return text # Return non-string data as is

    # 1. Remove '_new'
    text = text.replace('_new', '')
    # 2. Remove '_culture'
    text = text.replace('_culture', '')
    # 3. Replace '_' with a space
    text = text.replace('_', ' ')
    
    # 4. Capitalize the start of each word
    # The str.title() method handles this well.
    text = text.title()
    
    # 5. Clean up multiple spaces and strip leading/trailing spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def process_csv(input_filepath, output_filepath):
    """
    Reads a CSV file, applies cleaning and capitalization to each field,
    and writes the result to a new CSV file.
    """
    try:
        with open(input_filepath, mode='r', newline='', encoding='utf-8') as infile, \
             open(output_filepath, mode='w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            header = next(reader, None) # Read the header row
            if header:
                # Clean and write the header
                cleaned_header = [clean_and_capitalize_text(cell) for cell in header]
                writer.writerow(cleaned_header)
            
            # Process and write the rest of the rows
            for row in reader:
                cleaned_row = [clean_and_capitalize_text(cell) for cell in row]
                writer.writerow(cleaned_row)
                
        print(f"Successfully processed '{input_filepath}' and saved the output to '{output_filepath}'")
        
    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Define the input and output file paths
    # The user uploaded 'parsed_cultures_from_file.csv'
    input_csv_file = 'parsed_cultures_from_file.csv' 
    output_csv_file = 'cleaned_parsed_cultures.csv'
    
    # Process the CSV file
    process_csv(input_csv_file, output_csv_file)

    # Example usage of the cleaning function (for testing individual strings):
    # test_strings = [
    #     "hello_world_new_culture_test_value",
    #     "some_value_new",
    #     "another_culture_example",
    #     "just_an_underscore",
    #     "already Cleaned NoUnderscore",
    #     " leading_and_trailing_spaces_new ",
    #     "multiple___underscores_culture"
    # ]
    # print("\nTesting the cleaning function:")
    # for s in test_strings:
    #     print(f"Original: '{s}' -> Cleaned: '{clean_and_capitalize_text(s)}'")
