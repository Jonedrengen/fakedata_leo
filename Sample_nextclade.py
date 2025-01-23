from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
import numpy as np
from datetime import datetime as datetime, timedelta
import datetime as datetime1
import time
from id_generators import GenerateUniqueSampleID, GenerateUniqueConsensusID, GenerateUniqueNextcladeResultID
from utility import write_to_csv, generate_ct_value
import pandas as pd
from utility import gen_whovariant_samplingdate, generate_qc_values

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
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        NextcladeResult_data.append(record)
    print(f'generated {i + 1} nextclade records in total')
    print(type(essentials_list))
    return NextcladeResult_data, essentials_list

def SampleData(record_amount, sample_ids, consensus_ids, essentials_list):
    Sample_data = []
    starting_time = time.time()
    update_time = 0.15
    
    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} sample records')
        
        sample_id = sample_ids[i]
        consensus_id = consensus_ids[i]
        essentials = essentials_list[i]
        lineage_of_interest = essentials['LineagesOfInterest']

        if lineage_of_interest == "Alpha":
            random_date = gen_whovariant_samplingdate("2020-09-18", "2022-02-01", "2021-04-22", 100) #original sd=501
        elif lineage_of_interest == "Beta":
            random_date = gen_whovariant_samplingdate("2021-01-10", "2021-07-19", "2021-04-03", 38) #original sd=190
        elif lineage_of_interest == "Gamma":
            random_date = gen_whovariant_samplingdate("2020-10-12", "2021-07-30", "2021-04-22", 58) #original sd=291
        elif lineage_of_interest == "Delta":
            random_date = gen_whovariant_samplingdate("2021-03-30", "2022-02-27", "2021-10-12", 66) #original sd=334
        elif lineage_of_interest == "Eta":
            random_date = gen_whovariant_samplingdate("2021-01-14", "2021-07-21", "2021-03-12", 36) #original sd=188
        elif lineage_of_interest == "Omicron":
            random_date = gen_whovariant_samplingdate("2021-02-20", "2022-03-01", "2022-01-26", 74) #original sd=374
        elif lineage_of_interest == "BA.2":
            random_date = gen_whovariant_samplingdate("2021-02-20", "2022-03-01", "2022-02-03", 74) #original sd=374
        elif lineage_of_interest == "BA.1":
            random_date = gen_whovariant_samplingdate("2021-11-22", "2022-03-01", "2022-01-17", 18) #original sd=99
        else:
            two_years = datetime.now() - timedelta(days=2*365)
            random_date = fake.date_between(start_date=two_years, end_date='today')

        formatted_date = f"{lineage_of_interest}: {random_date.strftime('%Y-%m-%d')}"
        random_time = fake.time_object()
        sample_datetime = datetime.combine(random_date, random_time)
        
        record = {
            "SampleID": sample_id,
            "Host": 'Human',
            "Ct": generate_ct_value(), #check korreletion med ncount eller ncountQC eller SeqLength
            "DateSampling": formatted_date,
            "CurrentConsensusID": consensus_id,
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now()),
            "SampleDateTime": sample_datetime
        }
        Sample_data.append(record)
    print(f'generated {i + 1} sample records in total')
    return Sample_data


if __name__ == "__main__":
    start_time = time.time()
    
    record_amount = 10000 

    NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                               "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                               "pcrPrimerChanges", "qc.mixedSites.totalMixedSites", "qc.overallScore", "qc.overallStatus", "qc.frameShifts.status", 
                               "qc.frameShifts.frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    Sample_headers = ["SampleID", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated", "SampleDateTime"]
    

    existing_sample_ids = set()
    existing_consensus_ids = set()
    existing_nextcladeresult_ids = set()

    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    nextcladeresult_ids = [GenerateUniqueNextcladeResultID(existing_nextcladeresult_ids) for i in range(record_amount)]

    NextcladeResult_data, essentials_list = NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids) #warning: do not make more that 1000000 records (not enough unique IDs)
    sample_data = SampleData(record_amount, sample_ids, consensus_ids, essentials_list) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('Sample_data.csv', sample_data, Sample_headers)
    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")