from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2, timedelta
import datetime as datetime1
import time
from Consensus import ConsensusData
from id_generators import GenerateUniqueNextcladeResultID, GenerateUniqueConsensusID
from utility import write_to_csv
from NextcladeResult_elements import frameShifts_elements, aaSubstitutions, aaDeletions, aaInsertions, substitutions, deletions, insertions, missing, nonACGTNs, pcrPrimerChanges

fake = Faker()

def NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids):
    NextcladeResult_data = []
    starting_time = time.time()
    update_time = 0.15
    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:  
            update_time += 0.15
            print(f'generated {i} nextclade records')
        nextcladeresult_id = nextcladeresult_ids[i]
        consensus_id = consensus_ids[i]
        
        # Generate Nextclade_pango value
        nextclade_pango = fake.random_element(elements=("AY.4.6", "B.1.177.12", "AY.4.2.3", "AY.60", "BA.1.1.13", "BC.2", "XV", None))
        
        # Set NextcladeVersion based on Nextclade_pango
        if nextclade_pango is None:
            nextclade_version = None
        else:
            nextclade_version = fake.random_element(elements=("nextclade 2.5.0", "nextclade 2.6.0", "nextclade 2.4.0"))
        
        record = {
            "NextcladeResultID": nextcladeresult_id,
            "frameShifts": None, # kan udelades                                              
            "aaSubstitutions": None,# kan udelades    
            "aaDeletions": None,# kan udelades    
            "aaInsertions": None, # kan udelades    
            "alignmentScore": random.randint(89000, 89700),
            "clade": fake.random_element(elements=(None, "20A", "20E (EU1)", "20D", "21F (Iota)", "21H (Mu)", "21G (Lambda)", "20B", "20G", "recombinant", 
                                                   "21D (Eta)", "20I (Alpha; V1)", "21J (Delta)", "21C (Epsilon)", "21L (Omicron)", "20H (Beta; V2)",
                                                   "21M (Omicron)", "21B (Kappa)", "21K (Omicron)", "19B", "21I (Delta)", "20C", "19A", "21A (Delta)",
                                                   "20J (Gamma; V3)")), #contains all possible clades as per dataset from Leo
            "Nextclade_pango": nextclade_pango,
            "substitutions": None,# kan udelades    
            "deletions": None,# kan udelades    
            "insertions": None,# kan udelades    
            "missing": None,# kan udelades    
            "nonACGTNs": None,# kan udelades    
            "pcrPrimerChanges": None, # kan udelades    
            "qc.mixedSites.totalMixedSites": fake.random_element(elements=(None, "0", "1", "2", "3", "7", "11")),
            "qc.overallScore": fake.random_element(elements=(None, "0", "20", "8", "6", "157", "121")),
            "qc.overallStatus": fake.random_element(elements=(None, "good", "mediocre", "bad")),
            "qc.frameShifts.status": None,
            "qc.frameShifts.frameShiftsIgnored": None,
            "NextcladeVersion": nextclade_version,
            "ConsensusID": consensus_id,
            "IsCurrent": '1',
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        }
        NextcladeResult_data.append(record)
    print(f'generated {i + 1} nextclade records in total')
    return NextcladeResult_data

if __name__ == '__main__':
    start_time = time.time()

    record_amount = 100000 ## Change for desired record amount


    NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                            "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                            "pcrPrimerChanges", "qc.mixedSites.totalMixedSites", "qc.overallScore", "qc.overallStatus", "qc.frameShifts.status", 
                            "qc.frameShifts.frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]

    existing_nextcladeresult_ids = set()
    existing_consensus_ids = set()

    nextcladeresult_ids = [GenerateUniqueNextcladeResultID(existing_nextcladeresult_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]

    NextcladeResult_data = NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")