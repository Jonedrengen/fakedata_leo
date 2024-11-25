
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

def generate_ct_value():
    # 21.26% chance to return NA (21,260/100,000 from a sample of original data)
    if random.random() < 0.2126: #random() generates random number between 0 and 1
        return None
        
    #NOTE to

    # Generate value following normal distribution, based on summary function in r
    # loc is the mean, which matches the summary of 100000 datapoints
    # scale=5.0 (most values between 22.91-32.91), lower scale is more tight around the mean, while higher scale is a wider spread. we chose 5, because it roughly matches the 1'st and 3'rd quartile

    ct = np.random.normal(loc=27.91, scale=5.0) #loc=mean, scale=(standard deviation)
    
    # ensure values stay within bounds (highest and lowest)
    ct = np.clip(ct, 0.0, 43.97)
    
    return round(ct, 5)

def generate_ncount_value():
    if random.random() < 0.01306: #if random number between 0 and 1 smaller than 0.01306, then return None
        return None
    
    #IQR = 1.35σ = 3'rd - 1'st quartile range (599-121=478)
    #σ = IQR/1.35 ≈ 354
    ncount = np.random.normal(loc=2857, scale=354) 

    #clipping max and min values
    ncount = np.clip(ncount, 0, 29903)

    return round(ncount)

# numbers 0-29 or NA generated for ambiguoussites
ambiguous_values = list(range(30)) + [None]
ambiguous_values_frequencies = [60331, 18876, 8753, 4384, 2218, 1106, 626, 432, 293, 236,
                                218, 185, 126, 100, 80, 76, 52, 70, 44, 39,
                                37, 28, 32, 26, 29, 22, 19, 18, 15, 15, 1306]
def generate_ambiguoussites():
    return random.choices(ambiguous_values, ambiguous_values_frequencies)[0]


