import pandas as pd
import ast
from tqdm import tqdm

def parse_cast(cast_str):
    """Parse string representation of cast list into actual list"""
    try:
        return ast.literal_eval(str(cast_str)) if pd.notna(cast_str) else []
    except (ValueError, SyntaxError):
        return []

def clean_list_format(value):
    """Remove list formatting characters and return clean string"""
    if isinstance(value, list):
        # Convert list to string and remove [' and '] 
        return str(value).strip("['']")
    return value

# Read the CSV file
print("Reading CSV file...")
df = pd.read_csv('movies.csv', low_memory=False)

# Convert cast string to actual list
print("Processing cast column...")
tqdm.pandas()
df['cast'] = df['cast'].progress_apply(parse_cast)

print("Normalizing data...")
# Reset index to maintain order
df = df.reset_index()
# Convert NaN values to empty lists
df['cast'] = df['cast'].apply(lambda x: x if isinstance(x, list) else [])

# Explode the cast list into separate rows
df_cast = pd.DataFrame([item for sublist in df['cast'] for item in sublist])
df_cast['index'] = df_cast.index

# Define columns to keep
columns = ['index', 'adult', 'gender', 'id', 'known_for_department', 'name', 
           'original_name', 'popularity', 'profile_path', 'cast_id', 
           'character', 'credit_id', 'order']

print("Grouping data...")
# Group by index to maintain movie relationships
df_cast = df_cast[columns].groupby('index').agg(list)

print("Cleaning list formatting...")
# Clean the list formatting from all columns
for column in df_cast.columns:
    df_cast[column] = df_cast[column].apply(clean_list_format)

print("Saving to file...")
df_cast.to_csv('modified_movies.csv')
print("Done!")