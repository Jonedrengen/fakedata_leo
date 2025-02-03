
import csv
import time
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")


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

#Ambiguoussites
# numbers 0-29 or NA generated for ambiguoussites
ambiguous_values = list(range(30))
ambiguous_values_frequencies = [60331, 18876, 8753, 4384, 2218, 1106, 626, 432, 293, 236,
                                218, 185, 126, 100, 80, 76, 52, 70, 44, 39,
                                37, 28, 32, 26, 29, 22, 19, 18, 15, 15]
def generate_ambiguoussites():
    return random.choices(ambiguous_values, ambiguous_values_frequencies)[0]

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

def generate_NumbAlignedReads():
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

def gen_whovariant_samplingdate(start_date="2020-09-01", end_date="2022-03-01", mean_date="2021-07-11", std_deviation_days=100):
    
    #convert strings to dates
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    mean_date = datetime.strptime(mean_date, "%Y-%m-%d")

    
    mean_timestamp = mean_date.timestamp()
    std_dev_seconds = std_deviation_days * 24 * 60 * 60

    while True:
        random_timestamp = np.random.normal(mean_timestamp, std_dev_seconds)
        random_date = datetime.fromtimestamp(random_timestamp)
        if start_date <= random_date <= end_date:
            return random_date

def gen_whovariant_datesampling(Lineage_of_interest, csv_file = "important_files/DateSampling_LOI_weights.csv"):
    
    data = pd.read_csv(csv_file, na_values=["NULL"])
    
    if Lineage_of_interest is None or pd.isna(Lineage_of_interest):
        # Only select from NULL entries (Pre_WHO_Naming)
        lineage_data = data[data['LineagesOfInterest'].isna()]
    else:
        # Strict matching - only use dates specifically tagged for this lineage
        lineage_data = data[data['LineagesOfInterest'] == Lineage_of_interest]
        if len(lineage_data) == 0:
            return None

    if len(lineage_data) == 0:
        return None
        
    dates = lineage_data['DateSampling'].values
    weights = lineage_data['weight'].values
    
    selected_date = random.choices(dates, weights=weights, k=1)[0]
    return datetime.strptime(selected_date, '%Y-%m-%d')

def generate_exclusion_values(csv_file="important_files/ManualExclude_SequenceExclude_QcScore.csv"):
    """
    Returns: dict with three values
    """
    # Read CSV
    data = pd.read_csv(csv_file)
    indices = range(len(data))
    
    # Get weights
    weights = data['weight'].values
    
    # Select random row based on weights
    selected_index = random.choices(indices, weights=weights, k=1)[0]
    selected_row = data.iloc[selected_index]
    
    return {
        'manual_exclude': None if pd.isna(selected_row['ManualExclude']) else selected_row['ManualExclude'],
        'sequence_exclude': None if pd.isna(selected_row['SequenceExclude']) else selected_row['SequenceExclude'],
        'qc_score': None if pd.isna(selected_row['QcScore']) else selected_row['QcScore']
    }

