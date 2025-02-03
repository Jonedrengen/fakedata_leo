

import pandas as pd

# Adjust the file path if necessary
df = pd.read_csv("Consensus_data.csv", na_values=["NULL"])

# Filter out rows where SequenceExclude is not NaN (keep those where it is NaN)
df_filtered = df[df["SequenceExclude"].isna()]

# Count None/NaN values in WhoVariant and LineagesOfInterest columns
who_variant_none_count = df_filtered["WhoVariant"].isna().sum()
lineages_of_interest_none_count = df_filtered["LineagesOfInterest"].isna().sum()

print(f"WhoVariant is None: {who_variant_none_count}")
print(f"LineagesOfInterest is None: {lineages_of_interest_none_count}")

