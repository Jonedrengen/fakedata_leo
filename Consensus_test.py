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


def ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextclade_ids ,pangolin_ids):
    Consensus_data = []
    starting_time = time.time()
    update_time = 0.15

    #map of different vatiants and their connections
    variant_mapping = {
    'Alpha': {
        'alpha': 1, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 0,
        'ba_1': 0, 'ba_2': 0, 'lineageofinterest': 'Alpha',
        'unaliasedpango': 'B.1.1.7'
    },
    'Beta': {
        'alpha': 0, 'beta': 1, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 0,
        'ba_1': 0, 'ba_2': 0, 'lineageofinterest': 'Beta',
        'unaliasedpango': 'B.1.351'
    },
    'Gamma': {
        'alpha': 0, 'beta': 0, 'gamma': 1, 'delta': 0, 'eta': 0, 'omicron': 0,
        'ba_1': 0, 'ba_2': 0, 'lineageofinterest': 'Gamma',
        'unaliasedpango': 'P.1'
    },
    'Delta': {
        'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 1, 'eta': 0, 'omicron': 0,
        'ba_1': 0, 'ba_2': 0, 'lineageofinterest': 'Delta',
        'unaliasedpango': 'B.1.617.2'
    },
    'Eta': {
        'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 1, 'omicron': 0,
        'ba_1': 0, 'ba_2': 0, 'lineageofinterest': 'Eta',
        'unaliasedpango': 'B.1.525'
    },
    'Omicron': {
        'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 1,
        'ba_1': 0, 'ba_2': 0, 'lineageofinterest': 'Omicron',
        'unaliasedpango': 'B.1.1.529'
    },
    None: {
        'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'eta': 0, 'omicron': 0,
        'ba_1': 0, 'ba_2': 0, 'lineageofinterest': None,
        'unaliasedpango': None
    }
}
    #map og exclusion #TODO make sure there is an evenly distributed amount across Mixed strain, neg contam, etc. Make sure it happens in the loop
    manualExclusion_mapping = {
        None: {'sequenceexclude': None, 
               'qcscore': None},

        'Manually_Excluded_Run': {'sequenceexclude': None,
                                  'qcscore': None
                                  },

        'Manually_Excluded_Plate': {'sequenceexclude': None, 
                                    'qcscore': None
                                    
                                    },

        'Manually_Excluded_Sample': {'sequenceexclude': None, 
                                     'qcscore': None
                                     }
    }

    version_possibilities = pd.read_csv('important_files/versions.csv').dropna()

    # Read the CSV file
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
        manualExclusion = fake.random_element(elements=(None, None, None, "Manually_Excluded_Run", "Manually_Excluded_Plate",
                                                    "Manually_Excluded_Sample",))
        manualExclusion_values = manualExclusion_mapping.get(manualExclusion, manualExclusion_mapping[None])
        #exclusion specifics (NCount, AmbiguousSites, NwAmb, PctCoveredBases, SeqLength)
    

        # defining ncount, ambiguous and nwamb
        ncount = generate_ncount_value()
        if ncount == None:
            nwamb = None
            ambiguoussites = None
        else:
            ambiguoussites = generate_ambiguoussites()
            nwamb = ncount + ambiguoussites

        if manualExclusion == None and random.randint(0, 71) == 1: # for every "NULL" ncount, there was 71 "NULL" manualexclusions in the test data set
            manualExclusion_values['ncount'] = None
            manualExclusion_values['ambiguoussites'] = None
            manualExclusion_values['NwAmb'] = None
        else:
            manualExclusion_values['ncount'] = ncount
            manualExclusion_values['ambiguoussites'] = ambiguoussites
            manualExclusion_values['NwAmb'] = nwamb

        #NCountQC: Depends on the value of NwAmb
        if manualExclusion_values['NwAmb'] is not None:
            if manualExclusion_values['NwAmb'] <= 130:
                ncountqc = 'HQ'
            elif manualExclusion_values["NwAmb"] > 130 and manualExclusion_values["NwAmb"] <= 3000:
                ncountqc = 'MQ'
            else:
                ncountqc = 'Fail'
        else:
            ncountqc = 'Fail'

        #PctCoveredBases based on NCountQC (based on the real data)
        #HQ = 99.56-100.00
        #MQ = 89.83-99.57
        #Fail = 0.00-90.12
        if ncount == None:
            pctcoveredbases = None
        elif ncountqc == 'HQ':
            pctcoveredbases = round(random.uniform(99.56, 100.00), 2)
        elif ncountqc == 'MQ':
            pctcoveredbases = round(random.uniform(89.83, 99.57), 2)
        else:
            pctcoveredbases = round(random.uniform(0.00, 90.12), 2)


        #exclusion specifics (sequenceexlude and qcscore)
        if manualExclusion == None:
            manualExclusion_values['sequenceexclude'] = fake.random_element(elements=(None, "MixedStrain"))
            manualExclusion_values['qcscore'] = fake.random_element(elements=(None, "Fail: Mixed strain"))
        elif manualExclusion == 'Manually_Excluded_Run':
            manualExclusion_values['sequenceexclude'] = fake.random_element(elements=(None, "MixedStrain;ManuallyExcluded"))
            manualExclusion_values['qcscore'] = fake.random_element(elements=(None, "Fail: Mixed strain"))
        elif manualExclusion == 'Manually_Excluded_Plate':
            manualExclusion_values['sequenceexclude'] = fake.random_element(elements=(None, "NegContamination;ManuallyExcluded"))
            manualExclusion_values['qcscore'] = fake.random_element(elements=(None, "Fail: Neg. Contamination"))
        elif manualExclusion == 'Manually_Excluded_Sample':
            manualExclusion_values['sequenceexclude'] = fake.random_element(elements=(None, "TooManyNs;ManuallyExcluded"))
            manualExclusion_values['qcscore'] = fake.random_element(elements=(None, "Fail: Too many Ns"))

        #exclusionspecifics numalignedreads
        if manualExclusion_values['qcscore'] == None:
            manualExclusion_values['numalignedreads'] = None
        else:
            manualExclusion_values['numalignedreads'] = generate_NumbAlignedReads()

        #WhoVariants interconnections
        whovariant = fake.random_element(elements=(None, "Alpha", "Beta", "Delta", "Eta", "Gamma", "Omicron"))
        variant_values = variant_mapping.get(whovariant, variant_mapping[None])

        # 2. Update omicron handling
        if whovariant == 'Omicron':
            variant_values['omicron'] = 1
            if random.choice([1, 0]):  # Change to 1/0
                variant_values['ba_1'] = 1
                variant_values['ba_2'] = 0
                variant_values['lineageofinterest'] = 'BA.1'
            else:
                variant_values['ba_1'] = 0
                variant_values['ba_2'] = 1
                variant_values['lineageofinterest'] = 'BA.2'

        version = str(version_possibilities['version'].sample(n=1, weights=version_possibilities['amount_nextclade_pangos'].tolist()).values[0])

        essentials = Nextclade_pango_essentials.sample(n=1, weights=weights_essentials).iloc[0]
        if pd.isna(essentials["WhoVariant"]):
            essentials['WhoVariant'] = None
        if pd.isna(essentials["LineagesOfInterest"]):
            essentials['LineagesOfInterest'] = None
        if pd.isna(essentials["UnaliasedPango"]):
            essentials['UnaliasedPango'] = None
        



        record = { 
            "ConsensusID": consensus_id,
            "NCount": manualExclusion_values['ncount'],
            "AmbiguousSites": manualExclusion_values['ambiguoussites'],
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
            "WhoVariant": essentials["WhoVariant"], #skal vælges ud fra nextclade_pango
            "LineagesOfInterest": essentials['LineagesOfInterest'], # skal vælges ud fra nextclade_pango
            "UnaliasedPango": essentials['UnaliasedPango'], #skal vælges ud fra Nextclade_Pango
            "SequencedSampleID": sequencedsample_id,
            "CurrentNextcladeID": nextclade_id,
            "CurrentPangolinID": pango_id,
            "IsCurrent": '1', #always current in test data
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