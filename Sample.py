from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
from id_generators import GenerateUniqueSampleID, GenerateUniqueConsensusID
from utility import write_to_csv

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
        record = {
            "SampleID": sample_id,
            "SampleDateTime": fake.date(),
            "Host": 'Human',
            "Ct": round(random.uniform(10, 42), 13),
            "DateSampling": fake.random_element(elements=("DateSamplingX", "DateSamplingY", "DateSamplingZ")),
            "CurrentConsensusID": consensus_id,
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Sample_data.append(record)
    print(f'generated {i + 1} sample records in total')
    return Sample_data

if __name__ == "__main__":
    start_time = time.time()
    
    record_amount = 100000

    Sample_headers = ["SampleID", "SampleDateTime", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated"]

    existing_sample_ids = set()
    existing_consensus_ids = set()

    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]

    sample_data = SampleData(record_amount, sample_ids, consensus_ids) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('Sample_data.csv', sample_data, Sample_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")