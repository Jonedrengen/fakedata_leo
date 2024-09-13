from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2
import datetime as datetime1
import time

fake = Faker()

# Global Variables #
record_amount = 10000 ## Change for desired record amount
# Global Variables #

NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                           "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                           "pcrPrimerChanges", "qc_mixedSites_totalMixedSited", "qc_overallScore", "qc_overallStatus", "qc_frameShifts_status", 
                           "qc_frameShifts_frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]

def GenerateUniqueNextcladeResultID(existing_ids):
    while True:
        NextcladeResult_id = "Nextclade-" + str(random.randint(0, 999999)).zfill(6)
        if NextcladeResult_id not in existing_ids:
            return NextcladeResult_id

def NextcladeResult(record_amount):
    NextcladeResult_data = []
    existing_Nextclade_ids = set()
    for i in range(record_amount):
        nextcladeresult_id = GenerateUniqueNextcladeResultID(existing_Nextclade_ids)
        existing_Nextclade_ids.add(nextcladeresult_id)
        record = {
            "NextcladeResultID": nextcladeresult_id
        }
        NextcladeResult_data.append(record)
    print(f"Sample data generated {record_amount} times")
    return NextcladeResult_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")

if __name__ == '__main__':
    start_time = time.time()
    
    NextcladeResult_data = NextcladeResult(record_amount) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")