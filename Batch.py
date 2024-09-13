from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time

fake = Faker()

# Global variables #
record_amount = 1000

# Global variables #
#BatchID is primary key
Batch_headers = ["BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"]

def GenerateUniqueBatchID(existing_ids):
    while True:
        batch_id = "Batch-" + str(random.randint(0, 999999)).zfill(6)
        if batch_id not in existing_ids:
            return batch_id

def BatchData(record_amount):
    Batch_data = []
    existing_ids = set()
    for i in range(record_amount):
        batch_id = GenerateUniqueBatchID(existing_ids)
        existing_ids.add(batch_id)
        record = {
            "BatchID": batch_id,
            "BatchDate": fake.date(),
            "Platform": fake.random_element(elements=('labA','labB','labC')),
            "BatchSource": fake.random_element(elements=('SourceA','SourceB','SourceC')),
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Batch_data.append(record)
    print(f"Batch data generated {record_amount} times")
    return Batch_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")


if __name__ == "__main__":
    start_time = time.time()
    
    batch_data = BatchData(record_amount)
    write_to_csv('batch_data.csv', batch_data, Batch_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")