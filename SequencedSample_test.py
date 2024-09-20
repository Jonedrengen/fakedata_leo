from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
import datetime as datetime1 #imported with odd name due to same name issue as below
from datetime import datetime as datetime2
import time
from id_generators import GenerateUniqueSequencedSampleID, GenerateUniqueBatchID, GenerateUniqueConsensusID, GenerateUniqueSampleID
from utility import extract_column, write_to_csv


fake = Faker()


def SequencedSampleData(record_amount, sequenced_sample_ids, batch_ids, consensus_ids, sample_ids):
    SequencedSample_data = []

    for i in range(record_amount):
        print(f'generating SequencedSample record nr. {i}')
        sequenced_sample_id = sequenced_sample_ids[i]
        batch_id = batch_ids[i]
        consensus_id = consensus_ids[i]
        sample_id = sample_ids[i]
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
    print(f"SequencedSample data generated {record_amount} times")
    return SequencedSample_data



if __name__ == "__main__":
    start_time = time.time()
    # Use the global record_amount variable
    record_amount = 10000

    SequencedSample_headers = ["SequencedSampleID", "SequencingType", "DateSequencing", "SampleContent", "BatchID", 
                           "CurrentConsensusID", "SampleID", "TimestampCreated", "TimestampUpdated"]
    
    existing_sequenced_ids = set()
    existing_batch_ids = set()
    existing_consensus_ids = set()
    existing_sample_ids = set()

    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    batch_ids = [GenerateUniqueBatchID(existing_batch_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    sequenced_sample_ids = [GenerateUniqueSequencedSampleID(existing_sequenced_ids) for i in range(record_amount)]


    SequencedSample_data = SequencedSampleData(record_amount, sequenced_sample_ids, batch_ids, consensus_ids, sample_ids)
    write_to_csv('SequencedSample_data.csv', SequencedSample_data, SequencedSample_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")