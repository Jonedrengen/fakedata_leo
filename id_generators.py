from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time


def GenerateUniqueSampleID(existing_sample_ids):
    while True:
        sample_id = "Sample-" + str(random.randint(0, 999999)).zfill(6)
        if sample_id not in existing_sample_ids:
            existing_sample_ids.add(sample_id)
            return sample_id

def GenerateUniqueConsensusID(existing_consensus_ids):
    while True:
        consensus_id = "Consensus-" + str(random.randint(0, 999999)).zfill(6)
        if consensus_id not in existing_consensus_ids:
            existing_consensus_ids.add(consensus_id)
            return consensus_id
        
def GenerateUniquePangolinResultID(existing_pango_ids):
    while True:
        pango_id = "Pangolin-" + str(random.randint(0, 999999)).zfill(6)
        if pango_id not in existing_pango_ids:
            existing_pango_ids.add(pango_id)
            return pango_id