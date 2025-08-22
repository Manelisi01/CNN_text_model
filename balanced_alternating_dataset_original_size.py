import pandas as pd
import argparse

def alternate_balanced_dataset(input_path, output_path, label_column):
    """
    Reorganize a CSV dataset to alternate rows between labels 0 and 1, using all available rows
    while maintaining a balanced dataset limited by the smaller label count.
    
    Args:
        input_path (str): Path to the input CSV file
        output_path (str): Path to save the reorganized CSV file
        label_column (str): Name of the column containing labels (0 and 1)
    """
    try:
        # Load the dataset
        df = pd.read_csv(input_path)
        
        # Check if the label column exists
        if label_column not in df.columns:
            print(f"Error: Column '{label_column}' not found in the dataset.")
            print(f"Available columns: {list(df.columns)}")
            return
        
        # Get label distribution
        label_counts = df[label_column].value_counts()
        print(f"\nOriginal label distribution in {input_path}:")
        print(label_counts)
        print(f"Total number of rows: {len(df)}")
        
        # Verify only labels 0 and 1 exist
        if not set(label_counts.index).issubset({0, 1}):
            print(f"Error: Found labels other than 0 and 1: {list(label_counts.index)}")
            return
        
        # Check for missing labels
        missing_labels = df[label_column].isna().sum()
        if missing_labels > 0:
            print(f"Warning: {missing_labels} rows have missing labels. These will be excluded.")
            df = df.dropna(subset=[label_column])
        
        # Filter rows for label 0 and label 1
        df_label_0 = df[df[label_column] == 0]
        df_label_1 = df[df[label_column] == 1]
        
        # Determine the number of pairs based on the minimum available rows
        num_pairs = min(len(df_label_0), len(df_label_1))
        print(f"\nUsing {num_pairs} rows per label to create alternating pattern (0,1,0,1...).")
        
        # Create an alternating pattern (0,1,0,1...)
        alternated_rows = []
        for i in range(num_pairs):
            alternated_rows.append(df_label_0.iloc[i])
            alternated_rows.append(df_label_1.iloc[i])
        
        # Convert to DataFrame
        alternated_df = pd.DataFrame(alternated_rows).reset_index(drop=True)
        
        # Save the reorganized dataset
        alternated_df.to_csv(output_path, index=False)
        print(f"\nSuccessfully created alternated balanced dataset with {len(alternated_df)} rows at {output_path}")
        
        # Print final label distribution
        print("\nLabel distribution in reorganized dataset:")
        print(alternated_df[label_column].value_counts())
        
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reorganize a CSV dataset to alternate labels (0,1,0,1...) using all available rows")
    parser.add_argument("--input_path", type=str, default="AI-GA-main/ai-ga-dataset.csv",
                        help="Path to the input CSV file")
    parser.add_argument("--output_path", type=str, default="AI-GA-main/ai-ga-dataset-alternated-full.csv",
                        help="Path to save the reorganized CSV file")
    parser.add_argument("--label_column", type=str, default="label",
                        help="Name of the column containing labels (0 and 1)")
    
    args = parser.parse_args()
    
    alternate_balanced_dataset(args.input_path, args.output_path, args.label_column)