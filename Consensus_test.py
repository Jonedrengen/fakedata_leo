from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
from id_generators import GenerateUniquePangolinResultID, GenerateUniqueConsensusID, GenerateUniqueSequencedSampleID, GenerateUniqueNextcladeResultID
from utility import write_to_csv

fake = Faker()


def ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextclade_ids ,pangolin_ids):
    Consensus_data = []
    starting_time = time.time()
    update_time = 0.15

    #map of different vatiants and their connections
    variant_mapping = {
        None: {'lineageofinterest': None, 'alpha': '0', 'beta': '0', 'gamma': '0', 'delta': '0', 'eta': '0', 'omicron': '0', 'ba_1': '0', 'ba_2': '0', 'bg': '0', 'ba_4': '0', 'ba_5': '0', 'ba_2_75': '0', 'bf_7': '0', 'unaliasedpango': None},
        'Alpha': {'lineageofinterest': 'Alpha', 'alpha': '1', 'beta': '0', 'gamma': '0', 'delta': '0', 'eta': '0', 'omicron': '0', 'ba_1': '0', 'ba_2': '0', 'bg': '0', 'ba_4': '0', 'ba_5': '0', 'ba_2_75': '0', 'bf_7': '0', 'unaliasedpango': 'B.1.1.7'},
        'Beta': {'lineageofinterest': 'Beta', 'alpha': '0', 'beta': '1', 'gamma': '0', 'delta': '0', 'eta': '0', 'omicron': '0', 'ba_1': '0', 'ba_2': '0', 'bg': '0', 'ba_4': '0', 'ba_5': '0', 'ba_2_75': '0', 'bf_7': '0', 'unaliasedpango': 'B.1.351'},
        'Gamma': {'lineageofinterest': 'Gamma', 'alpha': '0', 'beta': '0', 'gamma': '1', 'delta': '0', 'eta': '0', 'omicron': '0', 'ba_1': '0', 'ba_2': '0', 'bg': '0', 'ba_4': '0', 'ba_5': '0', 'ba_2_75': '0', 'bf_7': '0', 'unaliasedpango': 'B.1.1.28'},
        'Delta': {'lineageofinterest': 'Delta', 'alpha': '0', 'beta': '0', 'gamma': '0', 'delta': '1', 'eta': '0', 'omicron': '0', 'ba_1': '0', 'ba_2': '0', 'bg': '0', 'ba_4': '0', 'ba_5': '0', 'ba_2_75': '0', 'bf_7': '0', 'unaliasedpango': 'B.1.617.2'},
        'Eta': {'lineageofinterest': 'Eta', 'alpha': '0', 'beta': '0', 'gamma': '0', 'delta': '0', 'eta': '1', 'omicron': '0', 'ba_1': '0', 'ba_2': '0', 'bg': '0', 'ba_4': '0', 'ba_5': '0', 'ba_2_75': '0', 'bf_7': '0', 'unaliasedpango': 'B.1.525'},
        'Omicron': {'lineageofinterest': 'Omicron', 'alpha': '0', 'beta': '0', 'gamma': '0', 'delta': '0', 'eta': '0', 'omicron': '1', 'ba_1': '0', 'ba_2': '0', 'bg': '0', 'ba_4': '0', 'ba_5': '0', 'ba_2_75': '0', 'bf_7': '0', 'unaliasedpango': 'B.1.1.529.2'}

    } 
    #map og exclusion
    manualExclusion_mapping = {
        None: {'sequenceexclude': fake.random_element(elements=(None, "MixedStrain")), 
               'qcscore': fake.random_element(elements=(None, "Fail: Mixed strain"))},

        'Manually_Excluded_Run': {'sequenceexclude': fake.random_element(elements=(None, "MixedStrain;ManuallyExcluded")), 
                                  'qcscore': fake.random_element(elements=(None, "Fail: Mixed strain"))},

        'Manually_Excluded_Plate': {'sequenceexclude': fake.random_element(elements=(None, "NegContamination;ManuallyExcluded")), 
                                    'qcscore': fake.random_element(elements=(None, "Fail: Neg. Contamination"))},

        'Manually_Excluded_Sample': {'sequenceexclude': fake.random_element(elements=(None, "TooManyNs;ManuallyExcluded")), 
                                     'qcscore': fake.random_element(elements=(None, "Fail: Too many Ns"))}
    }

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} consensus records')
        consensus_id = consensus_ids[i]
        sequencedsample_id = sequencedsample_ids[i]
        nextclade_id = nextclade_ids[i]
        pango_id = pangolin_ids[i]

        #exclusions
        manualExclusion = fake.random_element(elements=(None, "Manually_Excluded_Run", "Manually_Excluded_Plate",
                                                        "Manually_Excluded_Sample",))
        manualExclusion_values = manualExclusion_mapping.get(manualExclusion, manualExclusion_mapping[None])

        #exclusion specifics

        #WhoVariants interconnections
        whovariant = fake.random_element(elements=(None, "Alpha", "Beta", "Delta", "Eta", "Gamma", "Omicron"))
        variant_values = variant_mapping.get(whovariant, variant_mapping[None])

        #handling omicron 
        if whovariant == 'Omicron':
            variant_values['omicron'] = '1'
            if random.choice([True, False]):
                variant_values['ba_1'] = '1'
                variant_values['ba_2'] = '0'
                variant_values['lineageofinterest'] = 'BA.1'
            else:
                variant_values['ba_1'] = '0'
                variant_values['ba_2'] = '1'
                variant_values['lineageofinterest'] = 'BA.2'
        if whovariant == None:
            variant_values['unaliasedpango'] = random.choice([None, 'XN', 'B.1.111', 'B.1.619', 'A.21', 'B.1.36'])

        record = { #TODO expand on consensus data, especially different variant and how they are connected
            "ConsensusID": consensus_id,
            "NCount": random.randint(0, 30000),
            "AmbiguousSites": random.randint(0, 157),
            "NwAmb": random.randint(0, 29903),
            "NCountQC": fake.random_element(elements=("HQ", "MQ", "Fail")),
            "NumAlignedReads": random.randint(0, 1000000),
            "PctCoveredBases": round(random.uniform(0, 100), 2),
            "SeqLength": random.randint(0, 30000),
            "QcScore": manualExclusion_values['qcscore'],
            "SequenceExclude": manualExclusion_values['sequenceexclude'],
            "ManualExclude": manualExclusion,
            "Alpha": variant_values['alpha'],
            "Beta": variant_values['beta'],
            "Gamma": variant_values['gamma'],
            "Delta": variant_values['delta'],
            "Eta": variant_values['eta'],
            "Omicron": variant_values['omicron'],
            "BA_1": variant_values['ba_1'],
            "BA_2": variant_values['ba_2'],
            "BG": '0',
            "BA_4": '0',
            "BA_5": '0',
            "BA_2_75": '0',
            "BF_7": '0',
            "WhoVariant": whovariant,
            "LineagesOfInterest": variant_values['lineageofinterest'],
            "UnaliasedPango": variant_values['unaliasedpango'],
            "SequencedSampleID": sequencedsample_id,
            "CurrentNextcladeID": nextclade_id,
            "CurrentPangolinID": pango_id,
            "IsCurrent": fake.random_element(elements=('0', '1')),
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Consensus_data.append(record)
    print(f'generated {i + 1} consensus records in total')
    return Consensus_data



if __name__ == "__main__":
    start_time = time.time()

    record_amount = 10000  # Example record amount

    Consensus_headers = ["ConsensusID", "NCount", "AmbiguousSites", "NwAmb", "NCountQC", "NumAlignedReads", "PctCoveredBases",
                     "SeqLength", "QcScore", "SequenceExclude", "ManualExclude", "Alpha", "Beta", "Gamma", "Delta", "Eta",
                     "Omicron", "BA_1", "BA_2", "BG", "BA_4", "BA_5", "BA_2_75", "BF_7", "WhoVariant", "LineagesOfInterest",
                     "UnaliasedPango", "SequencedSampleID", "CurrentNextcladeID", "CurrentPangolinID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    
    existing_consensus_ids = set()
    existing_pango_ids = set()
    existing_sequencedsample_ids = set()
    existing_nextclade_ids = set()

    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pangolin_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]
    sequencedsample_ids = [GenerateUniqueSequencedSampleID(existing_sequencedsample_ids) for i in range(record_amount)]
    nextclade_ids = [GenerateUniqueNextcladeResultID(existing_nextclade_ids) for i in range(record_amount)]

    Consensus_data = ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextclade_ids, pangolin_ids)
    write_to_csv('Consensus_data.csv', Consensus_data, Consensus_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")