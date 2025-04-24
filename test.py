import pandas as pd
from collections import Counter

def check_duplicates_in_file(filename, id_column):
    """Check for duplicate IDs in a CSV file."""
    print(f"\nChecking {filename} for duplicate {id_column} values...")
    
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Get all values of the ID column
    all_ids = list(df[id_column])
    unique_ids = set(all_ids)
    
    print(f"Total records: {len(all_ids)}")
    print(f"Unique IDs: {len(unique_ids)}")
    
    # Check for duplicates
    if len(all_ids) != len(unique_ids):
        print(f"WARNING: Found {len(all_ids) - len(unique_ids)} duplicate IDs!")
        
        # Find which IDs are duplicated
        id_counts = Counter(all_ids)
        duplicates = [id_val for id_val, count in id_counts.items() if count > 1]
        
        print(f"First 5 duplicate IDs: {duplicates[:5]}")
        
        # Show details for the first duplicate
        if duplicates:
            first_dup = duplicates[0]
            dup_rows = df[df[id_column] == first_dup]
            print(f"\nDetails for duplicate ID {first_dup}:")
            for i, row in dup_rows.iterrows():
                print(f"Row {i}:")
                # Print a few key columns to help identify the records
                for col in list(dup_rows.columns)[:5]:
                    print(f"  {col}: {row[col]}")
                print("  ...")
    else:
        print("No duplicates found. All IDs are unique!")
    
    return len(all_ids) - len(unique_ids)  # Return number of duplicates

def main():
    """Check all data files for duplicates."""
    print("Checking for duplicate IDs in all CSV files...\n")
    
    # Define files and their ID columns
    files_to_check = [
        ("output/QcVariantConsensus_data.csv", "QcVariantConsensusID"),
        ("output/ResultsNextclade_data.csv", "ResultsNextcladeID"),
        ("output/ResultsPangolin_data.csv", "PangolinID"),
        ("output/SampleSequenced_data.csv", "SampleSequencedID"),
        ("output/Run_data.csv", "RunID"),
        ("output/CaseSample_data.csv", "CaseSampleID")
    ]
    
    # Check each file for duplicates
    total_duplicates = 0
    for filename, id_column in files_to_check:
        duplicates = check_duplicates_in_file(filename, id_column)
        total_duplicates += duplicates
    
    # Summary
    if total_duplicates > 0:
        print(f"\nFOUND {total_duplicates} TOTAL DUPLICATES across all files!")
        print("Please fix these issues before proceeding with analysis.")
    else:
        print("\nAll files checked successfully. No duplicate IDs found!")

if __name__ == "__main__":
    main()