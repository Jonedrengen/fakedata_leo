from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
import datetime as datetime1 #imported with odd name due to same name issue as below
from datetime import datetime as datetime2
import time
from Batch import BatchData
from Sample import SampleData
from Consensus import ConsensusData
fake = Faker()

# Global variables #
record_amount = 10000 ## Change for desired record amount
Batch_amount = record_amount // 96 + 1 # Ensures enough batch IDs are generated, and save time

# Global variables #

SequencedSample_headers = ["SequencedSampleID", "SequencingType", "DateSequencing", "SampleContent", "BatchID", 
                           "CurrentConsensusID", "SampleID", "TimestampCreated", "TimestampUpdated"]


def extract_column(data, column_header):
    column = [record[column_header] for record in data]
    return column

def GenerateUniqueSequencedSampleID(existing_sequenced_ids):
    while True:
        SequencedSample_id = "SequencedSample-" + str(random.randint(0, 999999)).zfill(6)
        if SequencedSample_id not in existing_sequenced_ids:
            return SequencedSample_id


def SequencedSample(record_amount):
    
    Batch_data = BatchData(Batch_amount) #cross reference
    Consensus_data = ConsensusData(record_amount)
    Sample_data = SampleData(record_amount)
    extracted_BatchIDs = extract_column(Batch_data, "BatchID")
    extracted_SampleIDs = extract_column(Sample_data, "SampleID")
    extracted_ConsensusIDs = extract_column(Consensus_data, "ConsensusID")
    SequencedSample_data = []
    max_samples_per_batch = 96
    batch_index = 0
    batch_id = extracted_BatchIDs[batch_index]

    existing_sequenced_ids = set()

    for i in range(record_amount):
        if i > 0 and i % max_samples_per_batch == 0:
            batch_index += 1
            batch_id = extracted_BatchIDs[batch_index]

        sample_id = extracted_SampleIDs.pop(0)  # Pop the first SampleID
        consensus_id = extracted_ConsensusIDs.pop(0)
        sequenced_sample_id = GenerateUniqueSequencedSampleID(existing_sequenced_ids)
        existing_sequenced_ids.add(sequenced_sample_id)
        record = {
            "SequencedSampleID": sequenced_sample_id,
            "SequencingType": fake.random_element(elements=("hospital_sequencing", "test", "Hogwarts_sequencing_sent_to_Panem", "historic",
                                                            "Panem_sequencing", "live", "project", "hostital")),
            "DateSequencing": fake.date_between(datetime1.date(2020, 9, 17), datetime1.date(2022, 10, 3)), #TODO should match the batch date?
            "SampleContent": "RNA",
            "BatchID": batch_id,  # Assign BatchID from the current batch
            "CurrentConsensusID": consensus_id,
            "SampleID": sample_id,  # Use extracted SampleID
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        }
        SequencedSample_data.append(record)
    return SequencedSample_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")


if __name__ == "__main__":
    start_time = time.time()
    # Use the global record_amount variable
    SequencedSample_data = SequencedSample(record_amount)
    write_to_csv('SequencedSample_data.csv', SequencedSample_data, SequencedSample_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")