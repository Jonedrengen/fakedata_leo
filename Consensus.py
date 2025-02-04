from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
import pandas as pd
from id_generators import GenerateUniquePangolinResultID, GenerateUniqueConsensusID, GenerateUniqueSequencedSampleID, GenerateUniqueNextcladeResultID
from utility import write_to_csv, generate_ncount_value, generate_ambiguoussites, generate_NumbAlignedReads, generate_qc_values

fake = Faker()

def ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextclade_ids, pangolin_ids):
    Consensus_data = []
    starting_time = time.time()
    update_time = 0.15

    # map of different variants and their connections
    variant_mapping = {
        'Alpha': {'alpha': 1, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 0, 'ba_1': 0, 'ba_2': 0},
        'Beta': {'alpha': 0, 'beta': 1, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 0, 'ba_1': 0, 'ba_2': 0},
        'Gamma': {'alpha': 0, 'beta': 0, 'gamma': 1, 'delta': 0, 'eta': 0, 'omicron': 0, 'ba_1': 0, 'ba_2': 0},
        'Delta': {'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 1, 'eta': 0, 'omicron': 0, 'ba_1': 0, 'ba_2': 0},
        'Eta': {'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 1, 'omicron': 0, 'ba_1': 0, 'ba_2': 0},
        'Omicron': {'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 1, 'ba_1': 0, 'ba_2': 0},
        'BA.1': {'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 1, 'ba_1': 1, 'ba_2': 0},
        'BA.2': {'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 1, 'ba_1': 0, 'ba_2': 1},
        None: {'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 0, 'ba_1': 0, 'ba_2': 0}
    }

    # map of exclusion
    manualExclusion_mapping = {
        None: {'sequenceexclude': None, 'qcscore': None},
        'Manually_Excluded_Run': {'sequenceexclude': None, 'qcscore': None},
        'Manually_Excluded_Plate': {'sequenceexclude': None, 'qcscore': None},
        'Manually_Excluded_Sample': {'sequenceexclude': None, 'qcscore': None}
    }

    version_possibilities = pd.read_csv('important_files/versions.csv').dropna()

    #read the CSV file
    Nextclade_pango_essentials = pd.read_csv('important_files/Nextclade_pango_essentials.csv')
    weights_essentials = Nextclade_pango_essentials.iloc[:, -1].tolist()

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} consensus records')
        consensus_id = consensus_ids[i]
        sequencedsample_id = sequencedsample_ids[i]
        nextclade_id = nextclade_ids[i]
        pango_id = pangolin_ids[i]

        #exclusions (manualexclusion)
        manualExclusion = fake.random_element(elements=(None, "Manually_Excluded_Run", "Manually_Excluded_Plate", "Manually_Excluded_Sample"))
        manualExclusion_values = manualExclusion_mapping.get(manualExclusion, manualExclusion_mapping[None])

        #defining ncount, ambiguous and nwamb
        ncount = generate_ncount_value()
        if ncount is None:
            nwamb = None
            ambiguoussites = None
        else:
            ambiguoussites = generate_ambiguoussites()
            nwamb = ncount + ambiguoussites

        if manualExclusion is None and random.randint(0, 71) == 1:
            manualExclusion_values['ncount'] = None
            manualExclusion_values['ambiguoussites'] = None
            manualExclusion_values['NwAmb'] = None
        else:
            manualExclusion_values['ncount'] = ncount
            manualExclusion_values['ambiguoussites'] = ambiguoussites
            manualExclusion_values['NwAmb'] = nwamb

        # NCountQC: Depends on the value of NwAmb
        if manualExclusion_values['NwAmb'] is not None:
            if manualExclusion_values['NwAmb'] <= 130:
                ncountqc = 'HQ'
            elif manualExclusion_values["NwAmb"] > 130 and manualExclusion_values["NwAmb"] <= 3000:
                ncountqc = 'MQ'
            else:
                ncountqc = 'Fail'
        else:
            ncountqc = 'Fail'

        # pctCoveredBases based on NCountQC
        if ncount is None:
            pctcoveredbases = None
        elif ncountqc == 'HQ':
            pctcoveredbases = round(random.uniform(99.56, 100.00), 2)
        elif ncountqc == 'MQ':
            pctcoveredbases = round(random.uniform(89.83, 99.57), 2)
        else:
            pctcoveredbases = round(random.uniform(0.00, 90.12), 2)

        # exclusion specifics (sequenceexlude and qcscore)
        if manualExclusion is None:
            manualExclusion_values['sequenceexclude'] = random.choices(population=[None, "MixedStrain"],
                                                                       weights=[0.95, 0.05],
                                                                       k=1)[0]
            manualExclusion_values['qcscore'] = random.choices(population=[None, "Fail: Mixed strain"],
                                                                weights=[0.95, 0.05],
                                                                k=1)[0]
        elif manualExclusion == 'Manually_Excluded_Run':
            manualExclusion_values['sequenceexclude'] = random.choices(population=[None, "MixedStrain;ManuallyExcluded"],
                                                            weights=[0.95, 0.05],
                                                            k=1)[0]
            manualExclusion_values['qcscore'] = random.choices(population=[None, "Fail: Mixed strain"],
                                                    weights=[0.95, 0.05],
                                                    k=1)[0]
        elif manualExclusion == 'Manually_Excluded_Plate':
            manualExclusion_values['sequenceexclude'] = random.choices(population=[None, "NegContamination;ManuallyExcluded"],
                                                            weights=[0.95, 0.05],
                                                            k=1)[0]
            manualExclusion_values['qcscore'] = random.choices(population=[None, "Fail: Neg. Contamination"],
                                        weights=[0.95, 0.05],
                                        k=1)[0]
        elif manualExclusion == 'Manually_Excluded_Sample':
            manualExclusion_values['sequenceexclude'] = random.choices(population=[None, "TooManyNs;ManuallyExcluded"],
                                                weights=[0.95, 0.05],
                                                k=1)[0]
            manualExclusion_values['qcscore'] = random.choices(population=[None, "Fail: Too many Ns"],
                            weights=[0.95, 0.05],
                            k=1)[0]
            
        # if sequenceexclude is NULL, some qc_scores will be pass
        

        #exclusion specifics numalignedreads
        if manualExclusion_values['qcscore'] is None:
            manualExclusion_values['numalignedreads'] = None
        else:
            manualExclusion_values['numalignedreads'] = generate_NumbAlignedReads()

        # get essentials data
        essentials = Nextclade_pango_essentials.sample(n=1, weights=weights_essentials).iloc[0]
        
        whovariant = essentials["WhoVariant"]
        if pd.isna(whovariant):
            whovariant = None
        lineageofinterest = essentials["LineagesOfInterest"]
        if pd.isna(lineageofinterest):
            lineageofinterest = None
        unaliasedpango = essentials["UnaliasedPango"]
        if pd.isna(unaliasedpango):
            unaliasedpango = None

        #apply variant mapping
        variant_values = variant_mapping.get(whovariant, variant_mapping[None])

                # adjust for Omicron and its sublineages
        if whovariant == 'Omicron':
            if lineageofinterest == 'BA.1':
                variant_values['ba_1'] = 1
                variant_values['ba_2'] = 0
            elif lineageofinterest == 'BA.2':
                variant_values['ba_1'] = 0
                variant_values['ba_2'] = 1

        record = {
            "ConsensusID": consensus_id,
            "NCount": manualExclusion_values['ncount'], #above 3k = not passed (not implemented)
            "AmbiguousSites": manualExclusion_values['ambiguoussites'], # over 5, then NcountQC = fail (not implemented)
            "NwAmb": manualExclusion_values['NwAmb'],
            "NCountQC": ncountqc,
            "NumAlignedReads": manualExclusion_values['numalignedreads'],
            "PctCoveredBases": pctcoveredbases,
            "SeqLength": random.randint(29300, 30402),
            "QcScore": manualExclusion_values['qcscore'], 
            "SequenceExclude": manualExclusion_values['sequenceexclude'],
            "ManualExclude": manualExclusion,
            "Alpha": variant_values['alpha'],
            "Beta": variant_values['beta'],
            "Gamma": variant_values['gamma'],
            "Delta": variant_values['delta'],
            "Eta": variant_values['eta'],
            "Omicron": variant_values['omicron'],
            "BA.1": variant_values['ba_1'],
            "BA.2": variant_values['ba_2'],
            "BG": 0,
            "BA.4": 0,
            "BA.5": 0,
            "BA.2.75": 0,
            "BF.7": 0,
            "WhoVariant": whovariant,
            "LineagesOfInterest": lineageofinterest,
            "UnaliasedPango": unaliasedpango,
            "SequencedSampleID": sequencedsample_id,
            "CurrentNextcladeID": nextclade_id,
            "CurrentPangolinID": pango_id,
            "IsCurrent": '1',  # always current in test data
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
                         "Omicron", "BA.1", "BA.2", "BG", "BA.4", "BA.5", "BA.2.75", "BF.7", "WhoVariant", "LineagesOfInterest",
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