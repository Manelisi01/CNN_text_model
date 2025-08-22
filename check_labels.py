import pandas as pd
import argparse

def calculate_abstract_length(input_path, text_column, label_column):
    """
    Calculate the average character length of abstracts in a CSV dataset and verify label distribution.
    
    Args:
        input_path (str): Path to the input CSV file
        text_column (str): Name of the column containing text (abstracts)
        label_column (str): Name of the column containing labels
    """
    try:
        # Load the dataset
        df = pd.read_csv(input_path)
        total_rows = len(df)
        
        # Check if columns exist
        if text_column not in df.columns:
            print(f"Error: Column '{text_column}' not found in the dataset.")
            print(f"Available columns: {list(df.columns)}")
            return
        if label_column not in df.columns:
            print(f"Error: Column '{label_column}' not found in the dataset.")
            print(f"Available columns: {list(df.columns)}")
            return
        
        # Check for missing abstracts
        missing_abstracts = df[text_column].isna().sum()
        if missing_abstracts > 0:
            print(f"Warning: {missing_abstracts} rows have missing abstracts.")
            missing_indices = df.index[df[text_column].isna()].tolist()
            print(f"Rows with missing abstracts: {missing_indices}")
            df = df.dropna(subset=[text_column])
        
        # Calculate character lengths of abstracts
        abstract_lengths = df[text_column].apply(lambda x: len(str(x)) if pd.notnull(x) else 0)
        
        # Compute average, min, max, and median lengths
        avg_length = abstract_lengths.mean()
        min_length = abstract_lengths.min()
        max_length = abstract_lengths.max()
        median_length = abstract_lengths.median()
        
        # Print length statistics
        print(f"\nAbstract length statistics (in characters):")
        print(f"Average length: {avg_length:.2f}")
        print(f"Minimum length: {min_length}")
        print(f"Maximum length: {max_length}")
        print(f"Median length: {median_length}")
        
        # Print label distribution
        label_counts = df[label_column].value_counts()
        print(f"\nLabel distribution:")
        print(label_counts)
        print(f"Total number of rows (after dropping missing abstracts): {len(df)}")
        
        # Check for missing labels
        missing_labels = df[label_column].isna().sum()
        if missing_labels > 0:
            print(f"Warning: {missing_labels} rows have missing labels.")
            missing_indices = df.index[df[label_column].isna()].tolist()
            print(f"Rows with missing labels: {missing_indices}")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate average character length of abstracts in a CSV dataset")
    parser.add_argument("--input_path", type=str, default="AI-GA-main/ai-ga-dataset-balanced-1000.csv",
                        help="Path to the input CSV file")
    parser.add_argument("--text_column", type=str, default="abstract",
                        help="Name of the column containing abstracts")
    parser.add_argument("--label_column", type=str, default="label",
                        help="Name of the column containing labels")
    
    args = parser.parse_args()
    
    calculate_abstract_length(args.input_path, args.text_column, args.label_column)