from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
from Batch import BatchData
from Sample import SampleData
fake = Faker()

# Global variables #
record_amount = 10000 ## Change for desired record amount
Batch_amount = record_amount // 96 + 1 # Ensure enough batch IDs are generated, and save time

# Global

SequencedSample_headers = ["SequencedSampleID", "SequencingType", "DateSequencing", "SampleContent", "BatchID", 
                           "CurrentConsensusID", "SampleID", "TimestampCreated", "TimestampUpdated"]


def extract_column(data, column_header):
    column = [record[column_header] for record in data]
    return column


def SequencedSample(record_amount):
    Batch_data = BatchData(Batch_amount) #cross reference
    Sample_data = SampleData(record_amount)
    extracted_BatchIDs = extract_column(Batch_data, "BatchID")
    extracted_SampleIDs = extract_column(Sample_data, "SampleID")
    SequencedSample_data = []
    max_samples_per_batch = 96

    batch_index = 0
    batch_id = extracted_BatchIDs[batch_index]

    for i in range(record_amount):
        if i > 0 and i % max_samples_per_batch == 0:
            batch_index += 1
            batch_id = extracted_BatchIDs[batch_index]

        sample_id = extracted_SampleIDs.pop(0)  # Pop the first SampleID

        record = {
            "SequencedSampleID": fake.random_element(elements=("SequencedID","SequencedSampleID")) + str(random.randint(0, 999999999)).zfill(9),
            "SequencingType": fake.random_element(elements=("SomeSequencingType", "SomeOtherType", "ThirdType")),
            "DateSequencing": fake.random_element(elements=("DatematchingBatchdate?", "SomeDate")), #TODO should match the batch date?
            "SampleContent": fake.random_element(elements=("SomeContent", "SomeotherContent")),
            "BatchID": batch_id,  # Assign BatchID from the current batch
            "CurrentConsensusID": fake.random_element(elements=("ConsensusID1", "ConsensusID2")),
            "SampleID": sample_id,  # Use extracted SampleID
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
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