from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
import numpy as np
from datetime import datetime as datetime, timedelta
import datetime as datetime1
import time
from id_generators import GenerateUniqueSampleID, GenerateUniqueConsensusID, GenerateUniqueNextcladeResultID, GenerateUniqueSequencedSampleID, GenerateUniquePangolinResultID
from utility import write_to_csv, generate_ct_value, gen_whovariant_samplingdate, generate_qc_values, generate_NumbAlignedReads, generate_ncount_value, generate_ambiguoussites, gen_whovariant_datesampling
import pandas as pd


fake = Faker()

def ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextclade_ids, pangolin_ids):
    consensus_essentials = []
    
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
        manualExclusion = fake.random_element(elements=(None, None, None, "Manually_Excluded_Run", "Manually_Excluded_Plate", "Manually_Excluded_Sample"))
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
            else:
                variant_values['ba_1'] = 0
                variant_values['ba_2'] = 0
        
        consensus_essentials.append(dict(essentials))
        
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
    return Consensus_data, consensus_essentials

def NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids):
    nextclade_essentials = []
    
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
        nextclade_essentials.append(dict(essentials))
        

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
    return NextcladeResult_data, nextclade_essentials


def SampleData(record_amount, sample_ids, consensus_ids, consensus_essentials):
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
        essentials = consensus_essentials[i]
        lineage_of_interest = essentials['LineagesOfInterest']

        if lineage_of_interest == "Alpha":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        elif lineage_of_interest == "Beta":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        elif lineage_of_interest == "Gamma":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        elif lineage_of_interest == "Delta":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        elif lineage_of_interest == "Eta":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        elif lineage_of_interest == "Omicron":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        elif lineage_of_interest == "BA.2":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        elif lineage_of_interest == "BA.1":
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        else:
            random_date = gen_whovariant_datesampling(lineage_of_interest)

        record = {
            "SampleID": sample_id,
            "Host": 'Human',
            "Ct": generate_ct_value(), #check korreletion med ncount eller ncountQC eller SeqLength
            "DateSampling": random_date.strftime('%Y-%m-%d') if random_date else None,
            "CurrentConsensusID": consensus_id,
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now()),
            "SampleDateTime": datetime.combine(random_date, fake.time_object()) if random_date else None
        }
        Sample_data.append(record)
    print(f'generated {i + 1} sample records in total')
    return Sample_data


if __name__ == "__main__":
    start_time = time.time()
    
    record_amount = 1000

    Consensus_headers = ["ConsensusID", "NCount", "AmbiguousSites", "NwAmb", "NCountQC", "NumAlignedReads", "PctCoveredBases",
                         "SeqLength", "QcScore", "SequenceExclude", "ManualExclude", "Alpha", "Beta", "Gamma", "Delta", "Eta",
                         "Omicron", "BA.1", "BA.2", "BG", "BA.4", "BA.5", "BA.2.75", "BF.7", "WhoVariant", "LineagesOfInterest",
                         "UnaliasedPango", "SequencedSampleID", "CurrentNextcladeID", "CurrentPangolinID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                               "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                               "pcrPrimerChanges", "qc.mixedSites.totalMixedSites", "qc.overallScore", "qc.overallStatus", "qc.frameShifts.status", 
                               "qc.frameShifts.frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    Sample_headers = ["SampleID", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated", "SampleDateTime"]
    

    existing_sample_ids = set()
    existing_consensus_ids = set()
    existing_pango_ids = set()
    existing_sequencedsample_ids = set()
    existing_nextclade_ids = set()

    nextcladeresult_ids = [GenerateUniqueNextcladeResultID(existing_nextclade_ids) for i in range(record_amount)]
    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pangolin_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]
    sequencedsample_ids = [GenerateUniqueSequencedSampleID(existing_sequencedsample_ids) for i in range(record_amount)]

    Consensus_data, consensus_essentials = ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextcladeresult_ids, pangolin_ids)
    NextcladeResult_data, nextclade_essentials = NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids)
    sample_data = SampleData(record_amount, sample_ids, consensus_ids, consensus_essentials)
    
    write_to_csv('Consensus_data.csv', Consensus_data, Consensus_headers)
    write_to_csv('Sample_data.csv', sample_data, Sample_headers)
    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")