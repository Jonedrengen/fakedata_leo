from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2
import datetime as datetime1
import time
import pandas as pd
from Consensus import GenerateUniqueConsensusID, GenerateUniquePangolinResultID, GenerateUniqueNextcladeResultID
from utility import write_to_csv
from NextcladeResult import NextcladeResultData


fake = Faker()



def PangolinResult(record_amount, pangolin_ids, consensus_ids, global_essentials_list):
    
    PangolinResult_data = []
    starting_time = time.time()
    update_time = 0.15

    version_possibilities = pd.read_csv('important_files/versions.csv').dropna()
    print(version_possibilities)
    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} pangolin records')
        pango_id = pangolin_ids[i]
        consensus_id = consensus_ids[i]

        essentials = global_essentials_list[i]
        if pd.isna(essentials["lineage"]):
            essentials['lineage'] = None
        lineage = essentials.get('lineage')

        version = str(version_possibilities['version'].sample(n=1, weights=version_possibilities['amount_nextclade_pangos'].tolist()).values[0])
        
        if lineage is None:
            version = None
            pangolin_version = None
            scopio_version = None
            constellation_version = None
            qc_status = None
            qc_notes = None
            note = None
        else:
            version = version
            pangolin_version = fake.random_element(elements=("4.2", "4.1.2"))
            scopio_version = '0.3.17'
            constellation_version = 'v0.1.10'
            qc_status = 'pass'
            qc_notes = 'some_qc_notes'
            note = 'some_note'



        record = {
            "PangolinResultID": pango_id,
            "lineage": lineage, #skal vælges ud fra Nextclade_Pango
            "version": version,
            "pangolin_version": pangolin_version, #real data: 4.2 = 26, 4.1.2 = 525417, NULL = 85643
            "scorpio_version": scopio_version, #real data: 0.3.17 = 525443, NULL = 85643
            "constellation_version": constellation_version, #real data: v0.1.10 = 525443, NULL = 85643
            "qc_status": qc_status, #real data: pass = 525443, NULL = 85643
            "qc_notes": qc_notes, #TODO if needed
            "note": note, #TODO if needed    
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
    
    record_amount = 1000

    PangolinResult_headers = ["PangolinResultID", "lineage", "version", "pangolin_version", "scorpio_version", "constellation_version", 
                           "qc_status", "qc_notes", "note", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    

    #generating ids
    existing_pango_ids = set()
    existing_consensus_ids = set()
    existing_nextcladeresult_ids = set()

    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pango_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]
    nextcladeresult_ids = [GenerateUniqueNextcladeResultID(existing_nextcladeresult_ids) for i in range(record_amount)]

    NextcladeResult_data, global_essentials_list = NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids)

    PangolinResult_data = PangolinResult(record_amount, pango_ids, consensus_ids, global_essentials_list) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('PangolinResult_data.csv', PangolinResult_data, PangolinResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")