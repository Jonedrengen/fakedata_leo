
import csv
import time
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, 
                              fieldnames=headers,
                              quoting=csv.QUOTE_NONE,  # Don't quote any fields
                              escapechar='\\',         # Use backslash to escape special characters
                              quotechar='"')           # Empty quote character
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")

def clean_string_fields(record):
    for key, value in record.items():
        if isinstance(value, str):
            record[key] = value.replace(',', ';')
    return record

def progress_update(total_records, update_interval=0.5):
    starting_time = time.time()
    update_time = 0
    for i in range(total_records):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += update_interval
            print(f'generated {i} records')

def extract_column(data, column_header):
    column = [record[column_header] for record in data]
    return column

#Ct
def generate_ct_value():
    # 21.26% chance to return NA (21,260/100,000 from a sample of original data)
    if random.random() < 0.2126: #random() generates random number between 0 and 1
        return None


    # Generate value following normal distribution, based on summary function in r
    # loc is the mean, which matches the summary of 100000 datapoints
    # scale=5.0 (most values between 22.91-32.91), lower scale is more tight around the mean, while higher scale is a wider spread. we chose 5, because it roughly matches the 1'st and 3'rd quartile

    ct = np.random.normal(loc=27.91, scale=5.0) #loc=mean, scale=(standard deviation)
    
    # ensure values stay within bounds (highest and lowest)
    ct = np.clip(ct, 0.0, 43.97)
    
    return round(ct, 5)

#Ncount 
# only NCount values that occured more than 30 times in real data
def generate_ncount_value(file="important_files/NCount_details_above30.csv"):
    NCount_values = pd.read_csv(file)
    NCount = NCount_values.sample(n=1, weights=NCount_values['amount_seen']).iloc[0]
    if pd.isna(NCount['NCount']):
        return None
    return int(NCount['NCount'])

#Ambiguoussites
def generate_ambiguoussites(file="important_files/AmbiguousSites_details.csv"):
    ambiguous_values = pd.read_csv(file)
    AmbiguousSite = ambiguous_values.sample(n=1, weights=ambiguous_values['amount_seen']).iloc[0]
    if pd.isna(AmbiguousSite['AmbiguousSites']):
        return None
    return int(AmbiguousSite['AmbiguousSites'])



def generate_NumbAlignedReads():
    # NumbAlignedReads
    #characteristics, based on R summary
    numbalignedreads_min = 0
    numbalignedreads_first_quartile = 869132
    numbalignedreads_median = 1890218
    numbalignedreads_mean = 2415394
    numbalignedreads_third_quartile = 3346942
    numbalignedreads_max = 40280538

    # 1. Calculate σ (Standard Deviation) σ Calculation:
    # 1.1 Convert Q1 and Q3 to their logarithms.
    # 1.2 Find the difference between these logarithms.
    # 1.3 Divide by 1.35 (IQR) to get σ.
    numbalignedreads_sigma = (np.log(numbalignedreads_third_quartile) - np.log(numbalignedreads_first_quartile)) / 1.35 #1.35 is IQR
    # 2. Calculate μ (Mean)
    # 2.1 Convert the median to its logarithm.
    # 2.2 Adjust this logarithm by subtracting half of σ squared to get μ.
    numbalignedreads_mu = np.log(numbalignedreads_median) - (numbalignedreads_sigma**2 / 2)
    value = np.random.lognormal(mean=numbalignedreads_mu, sigma=numbalignedreads_sigma)
    
    # values should stay within bounds
    value = np.clip(value, numbalignedreads_min, numbalignedreads_max)
    
    return round(value)


def generate_qc_values(csv_file):
    # Remove .dropna() to keep NULL values
    dataframe = pd.read_csv(csv_file, na_values=['NULL'])
    
    # extract the weights (last column)
    qc_sites_weights = dataframe['counted']

    # Sample a row from the dataframe based on the weights
    sample = dataframe.sample(n=1, weights=qc_sites_weights).iloc[0]

    # Extract the values from the sampled row, checking for NULL/NaN
    if pd.isna(sample['qc.mixedSites.totalMixedSites']):
        qc_mixedsites_totalmixedsites = None
    else:
        qc_mixedsites_totalmixedsites = int(sample['qc.mixedSites.totalMixedSites'])
    
    # Only generate status if we have mixedsites
    if qc_mixedsites_totalmixedsites is None:
        qc_overallscore = None
        qc_overallstatus = None
    else:
        qc_overallstatus = random.choices(['good', 'mediocre', 'bad'],
                                      weights=[0.806, 0.140, 0.038],
                                      k=1)[0]
        if qc_overallstatus == 'good':
            qc_overallscore = random.randint(0, 29)
        elif qc_overallstatus == 'mediocre':
            qc_overallscore = random.randint(30, 99)
        else:
            qc_overallscore = random.randint(100, 24702)

    return qc_mixedsites_totalmixedsites, qc_overallscore, qc_overallstatus


def gen_whovariant_datesampling(LineageOfInterest, reference_data):
    """
    Generates a sampling date for a given virus lineage based on weighted real data (directly from SSI).

    Args:
        LineageOfInterest (str or None): The lineage to generate a date for, such as 'Alpha', 'Beta', etc.
            Can be None to generate dates for pre-WHO naming samples.
        reference_data (pandas.DataFrame - "Complete_reference_data.csv"): Reference dataset containing columns:
            - LineagesOfInterest: The virus lineage
            - DateSampling: Date in 'YYYY-MM-DD' format
            - weight: Numerical weight for sampling probability

    Returns:
        datetime: A datetime object representing the sampling date.
            Returns None if no matching data found for the lineage.

    Example:
        >>> date = gen_whovariant_datesampling('Alpha', reference_df)
        >>> print(date)
        2021-02-15 00:00:00
    """
    if LineageOfInterest is None or pd.isna(LineageOfInterest):
        subset = reference_data[reference_data['LineagesOfInterest'].isna()]
    else:
        subset = reference_data[reference_data['LineagesOfInterest'] == LineageOfInterest]
        if subset.empty:
            return None
    
    selected_row = subset.sample(n=1, weights=subset['weight']).iloc[0]
    return datetime.strptime(selected_row['DateSampling'], '%Y-%m-%d')

def generate_exclusion_values(ncount=None, ambiguous_sites=None, csv_file="important_files/NCount_Amb_Seq_Split.csv"):
    """
    Generates exclusion values based on NCount and AmbiguousSites thresholds.

    Args:
        ncount (int, optional): Number of N's in sequence. Defaults to None.
        ambiguous_sites (int, optional): Number of ambiguous sites. Defaults to None.
        csv_file (str, optional): Path to CSV file containing exclusion combinations and their weights.
            Defaults to "important_files/NCount_Amb_Seq_Split.csv"

    Returns:
        dict: Dictionary containing three exclusion values:
            - manual_exclude: Manual exclusion flag or None if NA
            - sequence_exclude: Sequence exclusion flag or None if NA
            - qc_score: Quality control score

    Example:
        >>> exclusions = generate_exclusion_values(ncount=3500, ambiguous_sites=3)
        >>> print(exclusions)
        {'manual_exclude': None, 'sequence_exclude': 'TooManyNs', 'qc_score': 'Fail: Too many Ns'}
    """
    data = pd.read_csv(csv_file, na_values=['NULL'])
    
    # Determine which weight column to use based on NCount and AmbiguousSites values
    if ncount is not None and ambiguous_sites is not None:
        if ambiguous_sites <= 5 and ncount <= 3000:
            weights = data['Amb_low_NCount_low']
        elif ambiguous_sites <= 5 and ncount > 3000:
            weights = data['Amb_low_NCount_high']
        elif ambiguous_sites > 5 and ncount <= 3000:
            weights = data['Amb_high_NCount_low']
        else:  # ambiguous_sites > 5 and ncount > 3000
            weights = data['Amb_high_NCount_high']
    else:
        # If either value is None, use Amb_low_NCount_low as default
        weights = data['Amb_low_NCount_low']
    
    # Filter out rows where weight is 0
    mask = weights > 0
    filtered_data = data[mask]
    filtered_weights = weights[mask]
    if filtered_data.empty:
        return {
            'ManuelExlude': None,
            'SequenceExclude': None,
            'QcScore': None
        }
    # Sample a row based on the weights
    selected_row = filtered_data.sample(n=1, weights=filtered_weights).iloc[0]
    return {
        'ManualExclude': None if pd.isna(selected_row['ManualExclude']) else selected_row['ManualExclude'],
        'SequenceExclude': None if pd.isna(selected_row['SequenceExclude']) else selected_row['SequenceExclude'],
        'QcScore': None if pd.isna(selected_row['QcScore']) else selected_row['QcScore']
    }

def gen_SequencingType(BatchSource, csv_file="important_files/BatchSource_SequencingType_combinations.csv"):
    ref_data = pd.read_csv(csv_file)
    matching_rows = ref_data[ref_data['BatchSource'] == BatchSource]
    if matching_rows.empty:
        return 'hospital_sequencing'
    selected_type = matching_rows.sample(n=1, weights=matching_rows['weight']).iloc[0]
    return selected_type['SequencingType']

def generate_BatchSource(LineageOfInterest, DateSampling, reference_data):
    """
    Generates a batch source based on a LineageOfInterest and sampling date.
    all rows from "Complete_reference_data.csv" with a matching LineageOfInterest AND Date, will be filtered from the reference data
    Then, a random row, based on weights is taken. This row will contain the BatchSource that will be generated

    Args:
        LineageOfInterest (str or None): The lineage to match, such as 'Alpha', 'Beta', etc.
        DateSampling (datetime): The sampling date to match with batch sources
        reference_data (pandas.DataFrame): Reference dataset containing columns:
            - LineagesOfInterest: The virus lineage
            - DateSampling: Date in 'YYYY-MM-DD' format 
            - BatchSource: The batch source identifier to select from
            - weight: Numerical weight for sampling probability

    Returns:
        str: A batch source identifier (e.g., 'Panem', 'Hogwarts', etc.) selected based on a lineageofinterest and a DateSampling date.
            If no exact match found, returns a batch source from pre-WHO naming samples.

    Example:
        >>> reference_df = pd.read_csv('Complete_reference_data.csv')
        >>> date = datetime(2021, 2, 15)
        >>> batch = generate_BatchSource('Alpha', date, reference_df)
        >>> print(batch)
        'Panem'
    """

    mask = (reference_data['LineagesOfInterest'] == LineageOfInterest) & \
           (pd.to_datetime(reference_data['DateSampling']) == DateSampling)
    subset = reference_data[mask]
    
    if subset.empty:
        subset = reference_data[reference_data['LineagesOfInterest'].isna()]
    
    selected_row = subset.sample(n=1, weights=subset['weight']).iloc[0]
    return selected_row['BatchSource']
                            