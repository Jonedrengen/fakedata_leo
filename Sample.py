from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime, timedelta
import time
from id_generators import GenerateUniqueSampleID, GenerateUniqueConsensusID
from utility import write_to_csv, generate_ct_value
import pandas as pd
from utility import gen_whovariant_samplingdate

fake = Faker()

def SampleData(record_amount, sample_ids, consensus_ids):
    Sample_data = []
    starting_time = time.time()
    update_time = 0.15
    
    Nextclade_pango_essentials = pd.read_csv('important_files/Nextclade_pango_essentials.csv')
    weights_essentials = Nextclade_pango_essentials.iloc[:, -1].tolist()
    

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} sample records')
        
        sample_id = sample_ids[i]
        consensus_id = consensus_ids[i]

        # Get lineage info
        essentials = Nextclade_pango_essentials.sample(n=1, weights=weights_essentials).iloc[0]

        # Generate date based on LineagesOfInterest
        if essentials['LineagesOfInterest'] == "Alpha":
            random_date = gen_whovariant_samplingdate("2020-09-18", "2022-02-01", "2021-04-22", 501)
        elif essentials['LineagesOfInterest'] == "Beta":
            random_date = gen_whovariant_samplingdate("2021-01-10", "2021-07-19", "2021-04-03", 190)
        elif essentials['LineagesOfInterest'] == "Gamma":
            random_date = gen_whovariant_samplingdate("2020-10-12", "2021-07-30", "2021-04-22", 291)
        elif essentials['LineagesOfInterest'] == "Delta":
            random_date = gen_whovariant_samplingdate("2021-03-30", "2022-02-27", "2021-10-12", 334)
        elif essentials['LineagesOfInterest'] == "Eta":
            random_date = gen_whovariant_samplingdate("2021-01-14", "2021-07-21", "2021-03-12", 188)
        elif essentials['LineagesOfInterest'] == "Omicron":
            random_date = gen_whovariant_samplingdate("2021-02-20", "2022-03-01", "2022-01-26", 374)
        elif essentials['LineagesOfInterest'] == "BA.2":
            random_date = gen_whovariant_samplingdate("2021-02-20", "2022-03-01", "2022-02-03", 374)
        elif essentials['LineagesOfInterest'] == "BA.1":
            random_date = gen_whovariant_samplingdate("2021-11-22", "2022-03-01", "2022-01-17", 99)
        else:
            # Default case if no specific lineage
            random_date = gen_whovariant_samplingdate("2020-09-18", "2022-03-01", "2021-04-22", 501)
            #print(f"bad one used {i}")

        formatted_date = random_date.strftime("%Y-%m-%d")
        # Generate a random time of day
        random_time = fake.time_object()
        # Combine date and time to create a datetime object (TODO maybe change so that only first 2 pairs of numbers show)
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
    
    record_amount = 50000

    Sample_headers = ["SampleID", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated", "SampleDateTime"]

    existing_sample_ids = set()
    existing_consensus_ids = set()

    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]

    sample_data = SampleData(record_amount, sample_ids, consensus_ids) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('Sample_data.csv', sample_data, Sample_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")