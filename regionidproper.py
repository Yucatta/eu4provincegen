import pandas as pd

# Load the CSV file
file_path = 'region_ids2.csv'
df = pd.read_csv(file_path, header=None)

# Define a function to process each first element
def clean_first_element(text):
    if pd.isna(text):
        return text
    text = str(text).replace('_', ' ')
    text = text.replace('region', '')
    text = ' '.join(word.capitalize() for word in text.split())
    return text

# Apply the function to the first column
df[0] = df[0].apply(clean_first_element)

# Save the modified CSV
output_path = 'regionids.csv'
df.to_csv(output_path, index=False, header=False)

output_path
