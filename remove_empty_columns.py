import pandas as pd
from utility_V2 import write_to_csv
import csv

Nextclade_data = pd.read_csv("output/ResultsNextclade_data.csv")
#print(Nextclade_data)

Nextclade_data = Nextclade_data.drop(["frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "substitutions",
                                      "deletions", "insertions", "missing", "nonACGTNs", "pcrPrimerChanges", 
                                      "qc.frameShifts.status", "qc.frameShifts.frameShiftsIgnored"], axis=1)

print(Nextclade_data[:3])


def remove_unused_columns(file="output/ResultsNextclade_data.csv"):
    """
    Removes unused columns from Nextclade data and writes back to CSV.
    
    Args:
        file (str): Path to Nextclade CSV file
        
    Returns:
        None: Writes cleaned data directly to CSV
    """
    # Define columns to drop
    columns_to_drop = [
        "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", 
        "substitutions", "deletions", "insertions", "missing", 
        "nonACGTNs", "pcrPrimerChanges", "qc.frameShifts.status", 
        "qc.frameShifts.frameShiftsIgnored"
    ]
    
    # Read with appropriate dtypes for critical columns
    dtypes = {
        "qc.mixedSites.totalMixedSites": "Int64",
        "qc.overallScore": "Int64",
        "alignmentScore": "Int64",
        "IsCurrent": "Int64"
    }
    
    # Read data - recognize both NULL and nan as NaN values
    nextclade_data = pd.read_csv(file, dtype=dtypes)
    
    # Drop unwanted columns (only if they exist)
    columns_to_drop = [col for col in columns_to_drop if col in nextclade_data.columns]
    nextclade_data = nextclade_data.drop(columns_to_drop, axis=1)
    
    # Write back with appropriate formatting - leave NA values as empty strings
    nextclade_data.to_csv(file, index=False, na_rep='')


if __name__ == "__main__":
    remove_unused_columns()