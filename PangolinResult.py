from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2
import datetime as datetime1
import time


fake = Faker()

# Global Variables #
record_amount = 1000
# Global Variables #

PangolinResult_headers = ["PangolinResultID", "lineage", "version", "pangolin_version", "scorpio_version", "constellation_version", 
                           "qc_status", "qc_notes", "note", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]

def GenerateUniquePangolinResultID(existing_pango_ids):
    while True:
        pango_id = "Pangolin-" + str(random.randint(0, 999999)).zfill(6)
        if pango_id not in existing_pango_ids:
            return pango_id

def PangolinResult(record_amount):
    PangolinResult_data = []
    existing_pango_ids = set()
    for i in range(record_amount):
        pango_id = GenerateUniquePangolinResultID(existing_pango_ids)
        existing_pango_ids.add(pango_id)
        record = {
            "PangolinResultID": pango_id,
            "lineage": fake.random_element(elements=(None, "AY.4.2", "BA.2.14", "AY.43", "BA.1.17.2")),
            
            "version": fake.random_element(elements=(None, "PANGO-v1.12", "PUSHER-v1.18", "PANGO-v1.14", "PUSHER-v1.14", "PANGO-v1.18", "PUSHER-v1.12")),
            "pangolin_version": fake.random_element(elements=(None, "4.2", "4.1.2")),
            "scorpio_version": fake.random_element(elements=(None, "0.3.17")),
            "constellation_version": fake.random_element(elements=(None, "v0.1.10")),
            "qc_status": fake.random_element(elements=(None, "pass")),
            "qc_notes": fake.random_element(elements=(None, "Ambiguous_content:0.02", "Ambiguous_content:0.03", "Ambiguous_content:0.04")),
            "note": fake.random_element(elements=(None, "pass")),
            
            "ConsensusID": fake.random_element(elements=("Consensus-1", "Consensus-2", "Consensus-3")),
            "IsCurrent": fake.boolean(),
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        
        }
        PangolinResult_data.append(record)
    print(f"PangolinResult data generated {record_amount} times")
    return PangolinResult_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")


if __name__ == '__main__':
    start_time = time.time()
    
    PangolinResult_data = PangolinResult(record_amount) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('PangolinResult_data.csv', PangolinResult_data, PangolinResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")