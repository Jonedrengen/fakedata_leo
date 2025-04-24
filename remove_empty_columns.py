import pandas as pd
from utility import write_to_csv
import csv

Nextclade_data = pd.read_csv("output/ResultsNextclade_data.csv")
#print(Nextclade_data)

Nextclade_data = Nextclade_data.drop(["frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "substitutions",
                                      "deletions", "insertions", "missing", "nonACGTNs", "pcrPrimerChanges", 
                                      "qc.frameShifts.status", "qc.frameShifts.frameShiftsIgnored"],axis=1)

print(Nextclade_data[:3])


def remove_unused_columns(file="output/ResultsNextclade_data.csv"):
    """
    Removes unused columns from Nextclade data and writes back to CSV.
    
    Args:
        file (str): Path to Nextclade CSV file
        
    Returns:
        None: Writes cleaned data directly to CSV
    """
    # Define columns to keep
    nextclade_headers = [
        "ResultsNextcladeID", "alignmentScore",
        "clade", "Nextclade_pango", "qc.mixedSites.totalMixedSites", 
        "qc.overallScore", "qc.overallStatus",
        "NextcladeVersion", "QcVariantConsensusID", 
        "IsCurrent", "TimestampCreated", "TimestampUpdated"
    ]
    
    # Read and filter data
    nextclade_data = pd.read_csv(file)
    nextclade_data = nextclade_data[nextclade_headers]
    
    # Write to CSV manually
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=nextclade_headers)
        writer.writeheader()
        for i, row in nextclade_data.iterrows():
            writer.writerow(row.to_dict())

if __name__ == "__main__":
    remove_unused_columns()