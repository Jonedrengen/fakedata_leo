from faker import Faker
import random
import csv
import datetime as datetime1
from datetime import datetime as datetime2, timedelta
import time
import pandas as pd
from id_generators import GenerateUniqueBatchID
from utility import write_to_csv

fake = Faker()

def BatchData(record_amount, batch_ids):
    Batch_data = []
    starting_time = time.time()
    update_time = 0.15

    # Random date 2 years back for BatchDate
    two_years_BatchDate = datetime2.now() - timedelta(days=2*365)

    # Variables and their weights for batch_data
    platforms = [None, 'illumina qiaseq', 'nanopore', 'Illumina']
    platform_weights = [17, 20, 879, 1044]
    Batch_sources = ['Neverland', 'Gilead', 'Asgard', 'Agrabah', 'Panem', 'Narnia', 'Hogwarts', 'Middle-Earth', 'Wakanda', 'Pandora', 'Westeros']
    Batch_sources_weights = [41, 286, 100, 106, 16, 271, 865, 66, 127, 98, 2]

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} batch records')
        batch_id = batch_ids[i]

        # Random date for BatchDate
        random_date_BatchDate = fake.date_between(start_date=two_years_BatchDate, end_date='today')
        formatted_date_BatchDate = random_date_BatchDate.strftime("%Y-%m-%d")

        # Selecting platform based on weight
        Batch_platform = random.choices(platforms, platform_weights)[0]
        Batch_source = random.choices(Batch_sources, Batch_sources_weights)[0]

        record = {
            "BatchID": batch_id,
            "BatchDate": formatted_date_BatchDate,
            "Platform": Batch_platform,
            "BatchSource": Batch_source,
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        }
        Batch_data.append(record)
    print(f'generated {i + 1} batch records in total')
    return Batch_data

if __name__ == '__main__':
    start_time = time.time()

    record_amount = 1000  # Change for desired record amount

    Batch_headers = ["BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"]

    existing_batch_ids = set()
    batch_ids = [GenerateUniqueBatchID(existing_batch_ids) for i in range(record_amount)]

    Batch_data = BatchData(record_amount, batch_ids)

    write_to_csv('Batch_data.csv', Batch_data, Batch_headers)