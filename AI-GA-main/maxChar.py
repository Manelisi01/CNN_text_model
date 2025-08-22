import pandas as pd

# Load the dataset
df = pd.read_csv("ai-ga-dataset.csv")

# Calculate the length of each abstract
df['abstract_length'] = df['abstract'].apply(len)

# Find the maximum length
max_length = df['abstract_length'].max()
print(f"The largest number of characters in an abstract is: {max_length}")