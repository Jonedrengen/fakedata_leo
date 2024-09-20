from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
from id_generators import GenerateUniquePangolinResultID, GenerateUniqueConsensusID

fake = Faker()


def ConsensusData(record_amount, consensus_ids, pangolin_ids):
    Consensus_data = []
    for i in range(record_amount):
        print(f'generating Consensus record nr. {i}')
        consensus_id = consensus_ids[i]
        pango_id = pangolin_ids[i]
        record = {
            "ConsensusID": consensus_id,
            "NCount": random.randint(0, 1000),
            "AmbiguousSites": random.randint(0, 100),
            "NwAmb": random.randint(0, 100),
            "NCountQC": random.randint(0, 1000),
            "NumAlignedReads": random.randint(0, 1000000),
            "PctCoveredBases": random.uniform(0, 100),
            "SeqLength": random.randint(0, 30000),
            "QcScore": random.uniform(0, 100),
            "SequenceExclude": fake.boolean(),
            "ManualExclude": fake.boolean(),
            "Alpha": fake.boolean(),
            "Beta": fake.boolean(),
            "Gamma": fake.boolean(),
            "Delta": fake.boolean(),
            "Eta": fake.boolean(),
            "Omicron": fake.boolean(),
            "BA_1": fake.boolean(),
            "BA_2": fake.boolean(),
            "BG": fake.boolean(),
            "BA_4": fake.boolean(),
            "BA_5": fake.boolean(),
            "BA_2_75": fake.boolean(),
            "BF_7": fake.boolean(),
            "WhoVariant": fake.random_element(elements=("Variant1", "Variant2", "Variant3")),
            "LineagesOfInterest": fake.random_element(elements=("Lineage1", "Lineage2", "Lineage3")),
            "UnaliasedPango": fake.random_element(elements=("Pango1", "Pango2", "Pango3")),
            "SequencedSampleID": fake.random_element(elements=("SequencedID", "SequencedSampleID")) + str(random.randint(0, 999999999)).zfill(9),
            "CurrentNextcladeID": fake.random_element(elements=("NextcladeID1", "NextcladeID2")),
            "CurrentPangolinID": pango_id,
            "IsCurrent": fake.boolean(),
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Consensus_data.append(record)
    print(f"Consensus data generated {record_amount} times")
    return Consensus_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")

if __name__ == "__main__":
    start_time = time.time()

    record_amount = 10000  # Example record amount

    Consensus_headers = ["ConsensusID", "NCount", "AmbiguousSites", "NwAmb", "NCountQC", "NumAlignedReads", "PctCoveredBases",
                     "SeqLength", "QcScore", "SequenceExclude", "ManualExclude", "Alpha", "Beta", "Gamma", "Delta", "Eta",
                     "Omicron", "BA_1", "BA_2", "BG", "BA_4", "BA_5", "BA_2_75", "BF_7", "WhoVariant", "LineagesOfInterest",
                     "UnaliasedPango", "SequencedSampleID", "CurrentNextcladeID", "CurrentPangolinID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    
    existing_consensus_ids = set()
    existing_pango_ids = set()
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pangolin_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]

    Consensus_data = ConsensusData(record_amount, consensus_ids, pangolin_ids)
    write_to_csv('Consensus_data.csv', Consensus_data, Consensus_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")