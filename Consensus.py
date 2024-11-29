from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
from id_generators import GenerateUniquePangolinResultID, GenerateUniqueConsensusID, GenerateUniqueSequencedSampleID, GenerateUniqueNextcladeResultID
from utility import write_to_csv, generate_ncount_value, generate_ambiguoussites, generate_NumbAlignedReads, generate_pctcoveredbases

fake = Faker()


def ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextclade_ids ,pangolin_ids):
    Consensus_data = []
    starting_time = time.time()
    update_time = 0.15

    #map of different vatiants and their connections
    variant_mapping = {
        None: {'lineageofinterest': None, 'alpha': False, 'beta': False, 'gamma': False, 'delta': False, 'eta': False, 'omicron': False, 'ba_1': False, 'ba_2': False, 'bg': False, 'ba_4': False, 'ba_5': False, 'ba_2_75': False, 'bf_7': False, 'unaliasedpango': None},
        'Alpha': {'lineageofinterest': 'Alpha', 'alpha': True, 'beta': False, 'gamma': False, 'delta': False, 'eta': False, 'omicron': False, 'ba_1': False, 'ba_2': False, 'bg': False, 'ba_4': False, 'ba_5': False, 'ba_2_75': False, 'bf_7': False, 'unaliasedpango': 'B.1.1.7'},
        'Beta': {'lineageofinterest': 'Beta', 'alpha': False, 'beta': True, 'gamma': False, 'delta': False, 'eta': False, 'omicron': False, 'ba_1': False, 'ba_2': False, 'bg': False, 'ba_4': False, 'ba_5': False, 'ba_2_75': False, 'bf_7': False, 'unaliasedpango': 'B.1.351'},
        'Gamma': {'lineageofinterest': 'Gamma', 'alpha': False, 'beta': False, 'gamma': True, 'delta': False, 'eta': False, 'omicron': False, 'ba_1': False, 'ba_2': False, 'bg': False, 'ba_4': False, 'ba_5': False, 'ba_2_75': False, 'bf_7': False, 'unaliasedpango': 'B.1.1.28'},
        'Delta': {'lineageofinterest': 'Delta', 'alpha': False, 'beta': False, 'gamma': False, 'delta': True, 'eta': False, 'omicron': False, 'ba_1': False, 'ba_2': False, 'bg': False, 'ba_4': False, 'ba_5': False, 'ba_2_75': False, 'bf_7': False, 'unaliasedpango': 'B.1.617.2'},
        'Eta': {'lineageofinterest': 'Eta', 'alpha': False, 'beta': False, 'gamma': False, 'delta': False, 'eta': True, 'omicron': False, 'ba_1': False, 'ba_2': False, 'bg': False, 'ba_4': False, 'ba_5': False, 'ba_2_75': False, 'bf_7': False, 'unaliasedpango': 'B.1.525'},
        'Omicron': {'lineageofinterest': 'Omicron', 'alpha': False, 'beta': False, 'gamma': False, 'delta': False, 'eta': False, 'omicron': True, 'ba_1': False, 'ba_2': False, 'bg': False, 'ba_4': False, 'ba_5': False, 'ba_2_75': False, 'bf_7': False, 'unaliasedpango': 'B.1.1.529.2'}
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


        #exclusion specifics (NumAlignedReads)
        if manualExclusion_values['qcscore'] == None:
            manualExclusion_values['numalignedreads'] = None
        else:
            manualExclusion_values['numalignedreads'] = generate_NumbAlignedReads()

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

        #WhoVariants interconnections
        whovariant = fake.random_element(elements=(None, "Alpha", "Beta", "Delta", "Eta", "Gamma", "Omicron"))
        variant_values = variant_mapping.get(whovariant, variant_mapping[None])

        #handling omicron 
        if whovariant == 'Omicron':
            variant_values['omicron'] = True
            if random.choice([True, False]):
                variant_values['ba_1'] = True
                variant_values['ba_2'] = False
                variant_values['lineageofinterest'] = 'BA.1'
            else:
                variant_values['ba_1'] = False
                variant_values['ba_2'] = True
                variant_values['lineageofinterest'] = 'BA.2'
        if whovariant == None:
            variant_values['unaliasedpango'] = random.choice([None, 'XN', 'B.1.111', 'B.1.619', 'A.21', 'B.1.36'])

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
            "BG": False,
            "BA.4": False,
            "BA.5": False,
            "BA.2.75": False,
            "BF.7": False,
            "WhoVariant": whovariant,
            "LineagesOfInterest": variant_values['lineageofinterest'],
            "UnaliasedPango": variant_values['unaliasedpango'],
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

    record_amount = 100000  # Example record amount

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