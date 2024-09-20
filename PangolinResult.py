from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2
import datetime as datetime1
import time
from Consensus import GenerateUniqueConsensusID, GenerateUniquePangolinResultID

fake = Faker()



def PangolinResult(record_amount, pangolin_ids, consensus_ids):
    
    PangolinResult_data = []
    
    for i in range(record_amount):
        print(f'generating PangolinResult record nr. {i}')
        pango_id = pangolin_ids[i]
        consensus_id = consensus_ids[i]
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
            
            "ConsensusID": consensus_id,
            "IsCurrent": '1',
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
    
    record_amount = 19999

    PangolinResult_headers = ["PangolinResultID", "lineage", "version", "pangolin_version", "scorpio_version", "constellation_version", 
                           "qc_status", "qc_notes", "note", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    

    #generating ids
    existing_pango_ids = set()
    existing_consensus_ids = set()

    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pango_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]

    PangolinResult_data = PangolinResult(record_amount, pango_ids, consensus_ids) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('PangolinResult_data.csv', PangolinResult_data, PangolinResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")