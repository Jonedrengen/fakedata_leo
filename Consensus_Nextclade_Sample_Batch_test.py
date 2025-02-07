from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
import numpy as np
from datetime import datetime as datetime, timedelta
import datetime as datetime1
import time
from id_generators import GenerateUniqueSampleID, GenerateUniqueConsensusID, GenerateUniqueNextcladeResultID, GenerateUniqueSequencedSampleID, GenerateUniquePangolinResultID, GenerateUniqueBatchID
from utility import write_to_csv, generate_ct_value, gen_whovariant_samplingdate, generate_qc_values,generate_NumbAlignedReads, generate_ncount_value, generate_ambiguoussites, gen_whovariant_datesampling, generate_exclusion_values
import pandas as pd
from collections import Counter

fake = Faker()

variant_counter = Counter()

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

    #read pangolin_essentials csv
    Nextclade_pango_essentials = pd.read_csv('important_files/Nextclade_pango_essentials.csv', na_values=["NULL"])
    weights_pango_essentials = Nextclade_pango_essentials.iloc[:, -1].tolist()


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
       # Get exclusion values
        exclusion_values = generate_exclusion_values()
        manualExclusion = exclusion_values['manual_exclude']
        
        # Rest of values now come directly from CSV
        manualExclusion_values = {
            'sequenceexclude': exclusion_values['sequence_exclude'],
            'qcscore': exclusion_values['qc_score']
        }

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

        #exclusion specifics numalignedreads
        if manualExclusion_values['qcscore'] is None:
            manualExclusion_values['numalignedreads'] = None
        else:
            manualExclusion_values['numalignedreads'] = generate_NumbAlignedReads()

        # get essentials data
        essentials = Nextclade_pango_essentials.sample(n=1, weights=weights_pango_essentials).iloc[0]
        
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
    return Consensus_data, consensus_essentials

def NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids, consensus_essentials):
    nextclade_essentials = []
    
    NextcladeResult_data = []
    starting_time = time.time()
    update_time = 0.15

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} nextclade records')
        nextcladeresult_id = nextcladeresult_ids[i]
        consensus_id = consensus_ids[i]
        essentials = consensus_essentials[i]

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
    Sample_essentials = []
    
    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} sample records')
        
        sample_id = sample_ids[i]
        consensus_id = consensus_ids[i]
        essentials = consensus_essentials[i]
        lineage_of_interest = essentials['LineagesOfInterest']

        #print(lineage_of_interest)
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
        elif pd.isna(lineage_of_interest): 
            #print(f"it is a nan: {lineage_of_interest}")
            #lineage_of_interest = random.choices(["Alpha", "Beta", "Gamma", "Delta", "Eta", "Omicron", "BA.2", "BA.1"])
            random_date = gen_whovariant_datesampling(lineage_of_interest)
        else:
            random_date = gen_whovariant_datesampling(lineage_of_interest)

        Sample_essentials.append(dict(essentials))
        

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
    #print(Sample_essentials)
    print(f'generated {i + 1} sample records in total')
    return Sample_data, Sample_essentials

def BatchData(record_amount, batch_ids, Sample_essentials):
    Batch_data = []
    starting_time = time.time()
    update_time = 0.15
    
    # READ the new CSV with time-based weighting
    # Columns expected: [LineagesOfInterest, StartDate, EndDate, BatchSource, weights]
    Batch_sources_df = pd.read_csv('important_files/BatchSources_by_week.csv', na_values=["NULL"])
    
    # If StartDate/EndDate are strings, convert to actual date objects
    Batch_sources_df['StartDate'] = pd.to_datetime(Batch_sources_df['StartDate'].str.split().str[0])
    Batch_sources_df['EndDate'] = pd.to_datetime(Batch_sources_df['EndDate'].str.split().str[0])
     
    # variables and their weights for batch_data platform
    platforms = [None, 'illumina qiaseq', 'nanopore', 'Illumina']
    platform_weights = [17, 20, 879, 1044]

    start_date = datetime(2020, 8, 1)  # Instead of '2020-08-01'
    end_date = datetime(2023, 1, 1) 

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} batch records')
        
        batch_id = batch_ids[i]
        
        # Get the lineage and sampling date from Sample_essentials
        lineage_of_interest = Sample_essentials[i].get('LineagesOfInterest')
        
        # Make sure you stored a valid DateSampling in Sample_essentials
        sample_date_str = Sample_essentials[i].get('DateSampling')  # e.g. '2021-10-05'
        if sample_date_str is not None and pd.notna(sample_date_str):
            # Convert to pandas datetime
            sample_date = pd.to_datetime(sample_date_str)
        else:
            # Generate random date and convert to pandas datetime
            random_date = fake.date_between(start_date=start_date, end_date=end_date)
            sample_date = pd.to_datetime(random_date)
        
        # PLATFORM: pick from your normal weighting
        Batch_platform = random.choices(platforms, platform_weights)[0]
        
        # Now filter the new Batch_sources_df by lineage & time
        if pd.isna(lineage_of_interest):
            # If lineage is NaN, pick rows where LineagesOfInterest is also NaN
            # or handle "NULL" logic
            subset = Batch_sources_df[Batch_sources_df['LineagesOfInterest'].isna()]
        else:
            # Match the lineage
            subset = Batch_sources_df[Batch_sources_df['LineagesOfInterest'] == lineage_of_interest]
        
        # Further filter by date range (StartDate <= sample_date <= EndDate)
        subset = subset[(subset['StartDate'] <= sample_date) & (sample_date <= subset['EndDate'])]
        
        # If subset is empty, fallback to some generic or “NULL” BatchSource
        if subset.empty:
            # Possibly pick from all rows with no lineage or default
            fallback = Batch_sources_df[Batch_sources_df['LineagesOfInterest'].isna()]
            # if that’s also empty, fallback to entire dataset
            if fallback.empty:
                fallback = Batch_sources_df
            subset = fallback
        
        # Sample 1 row from 'subset' with weights
        chosen_row = subset.sample(n=1, weights=subset['weights']).iloc[0]
        
        # Optionally, set the BatchDate to some small offset from sample_date
        # e.g. 0–7 days after the sample
        offset_days = random.randint(0, 7)
        batch_date = sample_date + timedelta(days=offset_days)
        formatted_date_BatchDate = batch_date.strftime('%Y-%m-%d')
        
        record = {
            "BatchID": batch_id,
            "BatchDate": formatted_date_BatchDate,
            "Platform": Batch_platform,
            "BatchSource": chosen_row['BatchSource'],
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        
        Batch_data.append(record)
    
    print(f'generated {i + 1} batch records in total')
    return Batch_data



if __name__ == "__main__":
    start_time = time.time()
    
    record_amount = 10

    Consensus_headers = ["ConsensusID", "NCount", "AmbiguousSites", "NwAmb", "NCountQC", "NumAlignedReads", "PctCoveredBases",
                         "SeqLength", "QcScore", "SequenceExclude", "ManualExclude", "Alpha", "Beta", "Gamma", "Delta", "Eta",
                         "Omicron", "BA.1", "BA.2", "BG", "BA.4", "BA.5", "BA.2.75", "BF.7", "WhoVariant", "LineagesOfInterest",
                         "UnaliasedPango", "SequencedSampleID", "CurrentNextcladeID", "CurrentPangolinID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                               "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                               "pcrPrimerChanges", "qc.mixedSites.totalMixedSites", "qc.overallScore", "qc.overallStatus", "qc.frameShifts.status", 
                               "qc.frameShifts.frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    Sample_headers = ["SampleID", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated", "SampleDateTime"]
    Batch_headers = ["BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"]


    existing_sample_ids = set()
    existing_consensus_ids = set()
    existing_pango_ids = set()
    existing_sequencedsample_ids = set()
    existing_nextclade_ids = set()
    existing_batch_ids = set()

    nextcladeresult_ids = [GenerateUniqueNextcladeResultID(existing_nextclade_ids) for i in range(record_amount)]
    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pangolin_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]
    sequencedsample_ids = [GenerateUniqueSequencedSampleID(existing_sequencedsample_ids) for i in range(record_amount)]
    batch_ids = [GenerateUniqueBatchID(existing_batch_ids) for i in range(record_amount)]

    Consensus_data, consensus_essentials = ConsensusData(record_amount, consensus_ids, sequencedsample_ids, nextcladeresult_ids, pangolin_ids)
    NextcladeResult_data, nextclade_essentials = NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids, consensus_essentials)
    sample_data, Sample_essentials = SampleData(record_amount, sample_ids, consensus_ids, consensus_essentials)
    Batch_data = BatchData(record_amount, batch_ids, Sample_essentials)
    
    write_to_csv('Consensus_data.csv', Consensus_data, Consensus_headers)
    write_to_csv('Sample_data.csv', sample_data, Sample_headers)
    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)
    write_to_csv('Batch_data.csv', Batch_data, Batch_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")