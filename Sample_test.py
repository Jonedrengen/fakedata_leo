from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime, timedelta
import datetime as datetime1
import time
from id_generators import GenerateUniqueSampleID, GenerateUniqueConsensusID
from utility import write_to_csv, generate_ct_value
import pandas as pd
from utility import gen_whovariant_samplingdate

fake = Faker()

def SampleData(record_amount, sample_ids, consensus_ids):
    Sample_data = []
    starting_time = time.time()
    update_time = 0.15
    

    

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} sample records')
        
        sample_id = sample_ids[i]
        consensus_id = consensus_ids[i]


        two_years = datetime.now() - timedelta(days=2*365)
        random_date = fake.date_between(start_date=two_years, end_date='today')

        # Generate a random time of day
        random_time = fake.time_object()
        # Combine date and time to create a datetime object (TODO maybe change so that only first 2 pairs of numbers show)
        sample_datetime = datetime.combine(random_date, random_time)
        
        record = {
            "SampleID": sample_id,
            "Host": 'Human',
            "Ct": generate_ct_value(), #check korreletion med ncount eller ncountQC eller SeqLength
            "DateSampling": fake.date_between(datetime1.date(2020, 9, 17), datetime1.date(2022, 10, 3)),
            "CurrentConsensusID": consensus_id,
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now()),
            "SampleDateTime": sample_datetime
        }
        Sample_data.append(record)
    print(f'generated {i + 1} sample records in total')
    return Sample_data

if __name__ == "__main__":
    start_time = time.time()
    
    record_amount = 10000 

    Sample_headers = ["SampleID", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated", "SampleDateTime"]

    existing_sample_ids = set()
    existing_consensus_ids = set()

    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]

    sample_data = SampleData(record_amount, sample_ids, consensus_ids) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('Sample_data.csv', sample_data, Sample_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")