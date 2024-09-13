from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time

fake = Faker()


Sample_headers = ["SampleID", "SampleDateTime", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated"]

def GenerateUniqueConsensusID(existing_Consensus_ids):
    while True:
        consensus_id = "Consensus-" + str(random.randint(0, 999999)).zfill(6)
        if consensus_id not in existing_Consensus_ids:
            return consensus_id

def GenerateUniqueSampleID(existing_ids):
    while True:
        sample_id = "Sample-" + str(random.randint(0, 999999)).zfill(6)
        if sample_id not in existing_ids:
            return sample_id

def SampleData(record_amount):
    Sample_data = []
    existing_sample_ids = set()
    existing_consensus_ids = set() # roughly 1 consensusID per 10 SampleIDs
    for i in range(record_amount):
        sample_id = GenerateUniqueSampleID(existing_sample_ids)
        consensus_id = GenerateUniqueConsensusID(existing_consensus_ids)
        existing_sample_ids.add(sample_id)
        existing_consensus_ids.add(consensus_id)
        record = {
            "SampleID": sample_id,
            "SampleDateTime": fake.date(),
            "Host": fake.random_element(elements=("HostA", "HostB", "HostC")),
            "Ct": fake.random_element(elements=("CtA", "CtB", "CtC")),
            "DateSampling": fake.random_element(elements=("DateSamplingX", "DateSamplingY", "DateSamplingZ")),
            "CurrentConsensusID": consensus_id,
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Sample_data.append(record)
    print(f"Sample data generated {record_amount} times")
    return Sample_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")

if __name__ == "__main__":
    start_time = time.time()
    
    sample_data = SampleData(100) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('Sample_data.csv', sample_data, Sample_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")