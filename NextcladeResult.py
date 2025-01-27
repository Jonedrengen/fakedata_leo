from faker import Faker
import random
import csv
from datetime import datetime as datetime2, timedelta
import datetime as datetime1
import time
import pandas as pd
from id_generators import GenerateUniqueNextcladeResultID, GenerateUniqueConsensusID
from utility import write_to_csv, generate_ct_value, generate_ncount_value, generate_ambiguoussites, generate_NumbAlignedReads, generate_qc_values, gen_whovariant_samplingdate

fake = Faker()



def NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids):
    essentials_list = []
    
    NextcladeResult_data = []
    starting_time = time.time()
    update_time = 0.15

    Nextclade_pango_essentials = pd.read_csv('important_files/Nextclade_pango_essentials.csv')
    weights_essentials = Nextclade_pango_essentials.iloc[:, -1].tolist()

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} nextclade records')
        nextcladeresult_id = nextcladeresult_ids[i]
        consensus_id = consensus_ids[i]

        essentials = Nextclade_pango_essentials.sample(n=1, weights=weights_essentials).iloc[0]
        if pd.isna(essentials["clade"]):
            essentials['clade'] = None
        if pd.isna(essentials["Nextclade_pango"]):
            essentials['Nextclade_pango'] = None
        essentials_list.append(dict(essentials))
        

        nextclade_pango = essentials['Nextclade_pango']
        
        nextclade_version = fake.random_element(elements=("nextclade 2.5.0", "nextclade 2.6.0", "nextclade 2.4.0"))

        qc_data = generate_qc_values('important_files/qc_mixedsites_possibilities.csv')
        qc_mixedsites_totalmixedsites = qc_data[0]
        qc_overallscore = qc_data[1]
        qc_ocerallstatus = qc_data[2]

        record = {
            "NextcladeResultID": nextcladeresult_id,
            "frameShifts": None, #excluded
            "aaSubstitutions": None, #excluded
            "aaDeletions": None, #excluded
            "aaInsertions": None, #excluded
            "alignmentScore": random.randint(87816, 89709), #min and max values from real data
            "clade": essentials["clade"],
            "Nextclade_pango": nextclade_pango,
            "substitutions": None, #excluded
            "deletions": None, #excluded
            "insertions": None, #excluded
            "missing": None, #excluded
            "nonACGTNs": None, #excluded
            "pcrPrimerChanges": None, #excluded
            "qc.mixedSites.totalMixedSites": qc_mixedsites_totalmixedsites,
            "qc.overallScore": qc_overallscore,
            "qc.overallStatus": qc_ocerallstatus,
            "qc.frameShifts.status": None, #excluded
            "qc.frameShifts.frameShiftsIgnored": None, #excluded
            "NextcladeVersion": nextclade_version,
            "ConsensusID": consensus_id,
            "IsCurrent": '1',
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        }
        NextcladeResult_data.append(record)
    print(f'generated {i + 1} nextclade records in total')
    return NextcladeResult_data, essentials_list

if __name__ == '__main__':
    start_time = time.time()

    record_amount = 1000 ## Change for desired record amount

    NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                               "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                               "pcrPrimerChanges", "qc.mixedSites.totalMixedSites", "qc.overallScore", "qc.overallStatus", "qc.frameShifts.status", 
                               "qc.frameShifts.frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]

    existing_nextcladeresult_ids = set()
    existing_consensus_ids = set()

    nextcladeresult_ids = [GenerateUniqueNextcladeResultID(existing_nextcladeresult_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]

    NextcladeResult_data, essentials_list = NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids) #warning: do not make more that 1000000 records (not enough unique IDs)
    
    

    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)