from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime

fake = Faker()

#BatchID is primary key
Batch_headers = ["BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"]


def BatchData(record_amount):
    Batch_data = []
    for i in range(record_amount):
        record = {
            "BatchID": fake.random_element(elements=("someBatchID","someotherBatchID")) + str(random.randint(0, 999999999)).zfill(9),
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
    batch_data = BatchData(1000)

    write_to_csv('batch_data.csv', batch_data, Batch_headers)