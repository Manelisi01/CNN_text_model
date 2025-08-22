import pandas as pd
import argparse

def reduce_balanced_dataset(input_path, output_path, label_column, target_per_label):
    """
    Create a reduced version of a CSV dataset with an equal number of rows for each label (0 and 1).
    
    Args:
        input_path (str): Path to the input CSV file
        output_path (str): Path to save the reduced CSV file
        label_column (str): Name of the column containing labels
        target_per_label (int): Number of rows to keep for each label (0 and 1)
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
        
        # Check for missing labels
        missing_labels = df[label_column].isna().sum()
        if missing_labels > 0:
            print(f"Warning: {missing_labels} rows have missing labels. These will be excluded.")
            df = df.dropna(subset=[label_column])
        
        # Filter rows for label 0 and label 1
        df_label_0 = df[df[label_column] == 0].head(target_per_label)
        df_label_1 = df[df[label_column] == 1].head(target_per_label)
        
        # Check if we have enough rows for each label
        if len(df_label_0) < target_per_label:
            print(f"Warning: Only {len(df_label_0)} rows available for label 0 (requested {target_per_label}).")
        if len(df_label_1) < target_per_label:
            print(f"Warning: Only {len(df_label_1)} rows available for label 1 (requested {target_per_label}).")
        
        # Combine the balanced dataset
        balanced_df = pd.concat([df_label_0, df_label_1])
        
        # Shuffle the dataset to mix labels
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save the reduced dataset
        balanced_df.to_csv(output_path, index=False)
        print(f"\nSuccessfully created balanced dataset with {len(balanced_df)} rows at {output_path}")
        
        # Print final label distribution
        print("\nLabel distribution in reduced dataset:")
        print(balanced_df[label_column].value_counts())
        
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a balanced reduced version of a CSV dataset with equal labels")
    parser.add_argument("--input_path", type=str, default="AI-GA-main/ai-ga-dataset.csv",
                        help="Path to the input CSV file")
    parser.add_argument("--output_path", type=str, default="AI-GA-main/ai-ga-dataset-balanced-1000.csv",
                        help="Path to save the reduced CSV file")
    parser.add_argument("--label_column", type=str, default="label",
                        help="Name of the column containing labels")
    parser.add_argument("--target_per_label", type=int, default=500,
                        help="Number of rows to keep for each label (0 and 1)")
    
    args = parser.parse_args()
    
    reduce_balanced_dataset(args.input_path, args.output_path, args.label_column, args.target_per_label)