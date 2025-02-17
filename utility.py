
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

#Ncount (Right skewed generation)
def generate_ncount_value():
    # Log-normal parameters based on the given dataset
    median = 133
    q1 = 121
    q3 = 599

    # Calculate mu and sigma for the log-normal distribution
    mu = np.log(median)
    sigma = (np.log(q3) - np.log(q1)) / 1.35

    # Generate log-normal value
    ncount = np.random.lognormal(mean=mu, sigma=sigma)

    # Clip to match observed range
    ncount = np.clip(ncount, 0, 29903)

    return round(ncount)


def generate_ambiguoussites():
    #Ambiguoussites
    # numbers 0-29 or NA generated for ambiguoussites
    ambiguous_values = list(range(30))
    ambiguous_values_frequencies = [60331, 18876, 8753, 4384, 2218, 1106, 626, 432, 293, 236,
                                    218, 185, 126, 100, 80, 76, 52, 70, 44, 39,
                                    37, 28, 32, 26, 29, 22, 19, 18, 15, 15]
    return random.choices(ambiguous_values, ambiguous_values_frequencies)[0]



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
    dataframe = pd.read_csv(csv_file).dropna()

    # extract the weights (last column)
    qc_sites_weights = dataframe['counted']

    # Sample a row from the dataframe based on the weights
    sample = dataframe.sample(n=1, weights=qc_sites_weights).iloc[0]

    # Extract the values from the sampled row
    qc_mixedsites_totalmixedsites = int(sample['qc.mixedSites.totalMixedSites'])
    
    #random overall score based on the distribution from real data
    qc_overallstatus = random.choices(['good', 'mediocre', 'bad'],
                                    weights=[0.806, 0.140, 0.038], #weights based on real data
                                    k=1)[0] # k=take only 1
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

def generate_exclusion_values(csv_file="important_files/ManualExclude_SequenceExclude_QcScore.csv"):
    """
    Generates a random row of data, based on the data in ManualExclude_SequenceExclude_QcScore.csv
    The fourth column "weight" decides which row is chosen

    Args:
        csv_file (str, optional): Path to CSV file containing exclusion data with columns:
            - ManualExclude: Manual exclusion flag
            - SequenceExclude: Sequence exclusion flag  
            - QcScore: Quality control score
            - weight: Numerical weight for sampling probability
            Defaults to "important_files/ManualExclude_SequenceExclude_QcScore.csv"

    Returns:
        dict: Dictionary containing three exclusion values:
            - manual_exclude: Manual exclusion flag or None if NA
            - sequence_exclude: Sequence exclusion flag or None if NA
            - qc_score: Quality control score or None if NA

    Example:
        >>> exclusions = generate_exclusion_values()
        >>> print(exclusions)
        {'manual_exclude': None, 'sequence_exclude': 'Failed', 'qc_score': 25}
    """
    data = pd.read_csv(csv_file)
    indices = range(len(data))
    
    weights = data['weight'].values

    selected_index = random.choices(indices, weights=weights, k=1)[0]
    selected_row = data.iloc[selected_index]
    
    return {
        'manual_exclude': None if pd.isna(selected_row['ManualExclude']) else selected_row['ManualExclude'],
        'sequence_exclude': None if pd.isna(selected_row['SequenceExclude']) else selected_row['SequenceExclude'],
        'qc_score': None if pd.isna(selected_row['QcScore']) else selected_row['QcScore']
    }

def generate_BatchSource(LineageOfInterest, DateSampling, reference_data):
    """
    Generates a batch source based on a virus lineage and sampling date.
    all rows from "Complete_reference_data.csv" with a matching LineageOfInterest AND Date, will be filtered from the reference data
    Then, a random row, based on weights is taken. This row will contain the BatchSource that will be generated

    Args:
        LineageOfInterest (str or None): The virus lineage to match, such as 'Alpha', 'Beta', etc.
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
                            