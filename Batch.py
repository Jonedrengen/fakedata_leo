from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime, timedelta
import time
from id_generators import GenerateUniqueBatchID
from utility import write_to_csv

fake = Faker()

def BatchData(record_amount, batch_ids):
    Batch_data = []
    starting_time = time.time()
    update_time = 0.015

    #random date 2 years back
    two_years = datetime.now() - timedelta(days=2*365)

    #variables and their weights, based on test_data
    platforms = [None, 'illumina qiaseq', 'nanopore', 'Illumina']
    platform_weights = [17, 20, 879, 1044]

    Batch_sources = ['Neverland', 'Gilead', 'Asgard', 'Agrabah', 'Panem', 'Narnia', 'Hogwarts', 'Middle-Earth', 'Wakanda', 'Pandora', 'Westeros']
    Batch_sources_weights = [41, 286, 100, 106, 16, 271, 865, 66, 127, 98, 2]

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:  
            update_time += 0.015
            print(f'generated {i} batch records')
        batch_id = batch_ids[i]

        #random date
        random_date = fake.date_between(start_date=two_years, end_date='today')
        formatted_date = random_date.strftime("%Y-%m-%d")

        #selecting platform based on weight
        platform = random.choices(platforms, platform_weights)[0]
        Batch_source = random.choices(Batch_sources, Batch_sources_weights)[0]

        record = {
            "BatchID": batch_id,
            "BatchDate": formatted_date,
            "Platform": platform,
            "BatchSource": Batch_source,
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