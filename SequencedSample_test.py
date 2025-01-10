from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
import datetime as datetime1 #imported with odd name due to same name issue as below
from datetime import datetime as datetime2, timedelta
import time
import pandas as pd
from id_generators import GenerateUniqueSequencedSampleID, GenerateUniqueBatchID, GenerateUniqueConsensusID, GenerateUniqueSampleID
from utility import write_to_csv, gen_whovariant_samplingdate

fake = Faker()

def SequencedSampleData(record_amount, sequenced_sample_ids, batch_ids, consensus_ids, sample_ids):
    SequencedSample_data = []
    max_samples_per_batch = 100 #max batch size
    batch_index = 0
    starting_time = time.time()
    update_time = 0.15

    Nextclade_pango_essentials = pd.read_csv('important_files/Nextclade_pango_essentials.csv')
    weights_essentials = Nextclade_pango_essentials.iloc[:, -1].tolist()

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} sequencedsample records')
        
        sequenced_sample_id = sequenced_sample_ids[i]
        consensus_id = consensus_ids[i]
        sample_id = sample_ids[i]

        # Get lineage info
        essentials = Nextclade_pango_essentials.sample(n=1, weights=weights_essentials).iloc[0]

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
            two_years = datetime2.now() - timedelta(days=2*365)
            random_date = fake.date_between(start_date=two_years, end_date='today')

        formatted_date = random_date.strftime("%Y-%m-%d")

        # Assign the same batch_id to every 100 records
        if i > 0 and i % max_samples_per_batch == 0:
            batch_index += 1
        batch_id = batch_ids[batch_index]

        record = {
            "SequencedSampleID": sequenced_sample_id,
            "SequencingType": fake.random_element(elements=("hospital_sequencing", "test", "Hogwarts_sequencing_sent_to_Panem", "historic",
                                                            "Panem_sequencing", "live", "project", "hostital")),
            "DateSequencing": formatted_date, #TODO should match the batch date?
            "SampleContent": "RNA",
            "BatchID": batch_id,  # Assign BatchID from the current batch
            "CurrentConsensusID": consensus_id,
            "SampleID": sample_id,  # Use extracted SampleID
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        }
        SequencedSample_data.append(record)
    print(f'generated {i + 1} sequencedsample records in total')
    return SequencedSample_data

if __name__ == "__main__":
    start_time = time.time()
    # Use the global record_amount variable
    record_amount = 10000

    SequencedSample_headers = ["SequencedSampleID", "SequencingType", "DateSequencing", "SampleContent", "BatchID", 
                           "CurrentConsensusID", "SampleID", "TimestampCreated", "TimestampUpdated"]
    
    existing_sequenced_ids = set()
    existing_batch_ids = set()
    existing_consensus_ids = set()
    existing_sample_ids = set()

    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    batch_ids = [GenerateUniqueBatchID(existing_batch_ids) for i in range(record_amount // 100 + 1)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    sequenced_sample_ids = [GenerateUniqueSequencedSampleID(existing_sequenced_ids) for i in range(record_amount)]

    SequencedSample_data = SequencedSampleData(record_amount, sequenced_sample_ids, batch_ids, consensus_ids, sample_ids)
    write_to_csv('SequencedSample_data.csv', SequencedSample_data, SequencedSample_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")