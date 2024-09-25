from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
from id_generators import GenerateUniqueBatchID
from utility import write_to_csv

fake = Faker()

def BatchData(record_amount, batch_ids):
    Batch_data = []
    starting_time = time.time()
    update_time = 0.015
    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:  
            update_time += 0.015
            print(f'generated {i} batch records so far')
        batch_id = batch_ids[i]
        record = {
            "BatchID": batch_id,
            "BatchDate": fake.date(),
            "Platform": fake.random_element(elements=('labA','labB','labC')),
            "BatchSource": fake.random_element(elements=('SourceA','SourceB','SourceC')),
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Batch_data.append(record)
    print(f'generated {i + 1} batch records in total')
    return Batch_data

if __name__ == "__main__":
    start_time = time.time()
    
    record_amount = 500000

    Batch_headers = ["BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"]

    existing_batch_ids = set()

    batch_ids = [GenerateUniqueBatchID(existing_batch_ids) for i in range(record_amount // 100 + 1)]

    batch_data = BatchData(record_amount // 100 + 1, batch_ids)
    write_to_csv('Batch_data.csv', batch_data, Batch_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")