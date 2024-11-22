from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2
import datetime as datetime1
import time
from Consensus import GenerateUniqueConsensusID, GenerateUniquePangolinResultID
from utility import write_to_csv

fake = Faker()



def PangolinResult(record_amount, pangolin_ids, consensus_ids):
    
    PangolinResult_data = []
    starting_time = time.time()
    update_time = 0.15
    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} pangolin records')
        pango_id = pangolin_ids[i]
        consensus_id = consensus_ids[i]


        lineage = fake.random_element(elements=(None, "AY.4.2", "BA.2.14", "AY.43", "BA.1.17.2"))
        if lineage is None:
            version = None
            pangolin_version = None
            scopio_version = None
            constellation_version = None
            qc_status = None
            qc_notes = None
            note = None
        else:
            version = fake.random_element(elements=("PANGO-v1.12", "PUSHER-v1.18", "PANGO-v1.14", "PUSHER-v1.14", "PANGO-v1.18", "PUSHER-v1.12"))
            pangolin_version = fake.random_element(elements=("4.2", "4.1.2"))
            scopio_version = fake.random_element(elements=("0.3.17", "0.3.14"))
            constellation_version = fake.random_element(elements=("v0.1.10", "v0.1.8"))
            qc_status = 'pass'
            qc_notes = fake.random_element(elements=("Ambiguous_content:0.02", "Ambiguous_content:0.03", "Ambiguous_content:0.04"
                                                     "Ambiguous_content:0.1", "Ambiguous_content:0.05", "Ambiguous_content:0.11"
                                                     "Ambiguous_content:0.06", "Ambiguous_content:0.12", "Ambiguous_content:0.09"
                                                     "Ambiguous_content:0.08", "Ambiguous_content:0.07"))
            note = fake.random_element(elements=("passUsher placements: BA.1.1(2/2)", "Usher placements: B.1.1.7(9/9)", "Usher placements: AY.4.2.1(1/1)"))



        record = {
            "PangolinResultID": pango_id,
            "lineage": lineage,
            "version": version,
            "pangolin_version": pangolin_version,
            "scorpio_version": scopio_version,
            "constellation_version": constellation_version,
            "qc_status": qc_status,
            "qc_notes": qc_notes,
            "note": None, # kan udelades    
            "ConsensusID": consensus_id,
            "IsCurrent": '1',
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        
        }
        PangolinResult_data.append(record)
    print(f'generated {i + 1} pangolin records in total')
    return PangolinResult_data



if __name__ == '__main__':
    start_time = time.time()
    
    record_amount = 100000

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