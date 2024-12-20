
import csv
import time
import random
import numpy as np


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


# PctCoveredBases (left skewed generation)
#cjharacteristics based on R summary
pctcoveredbases_min = 0.00
pctcoveredbases_first_quartile = 98.99
pctcoveredbases_median = 99.55
pctcoveredbases_mean = 90.48
pctcoveredbases_third_quartile = 99.60
pctcoveredbases_max = 100.00

# Calculate the parameters for the beta distribution
# Using method of moments to estimate alpha and beta
mean = pctcoveredbases_mean / 100
variance = ((pctcoveredbases_third_quartile - pctcoveredbases_first_quartile) / 1.35) ** 2
alpha = mean * (mean * (1 - mean) / variance - 1)
beta = (1 - mean) * (mean * (1 - mean) / variance - 1)

def generate_pctcoveredbases():
    # Generate a value from a beta distribution
    value = np.random.beta(alpha, beta)
    
    # Transform the value to the original range
    value = pctcoveredbases_min + value * (pctcoveredbases_max - pctcoveredbases_min)
    
    return round(value, 2)