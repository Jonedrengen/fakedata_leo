from faker import Faker
import random
import csv
import datetime as datetime1
from datetime import datetime as datetime2, timedelta
import time
import pandas as pd
from id_generators import (GenerateUniquePangolinResultID, GenerateUniqueConsensusID, GenerateUniqueSequencedSampleID, 
                           GenerateUniqueNextcladeResultID, GenerateUniqueBatchID, GenerateUniqueSampleID)
from utility import write_to_csv, generate_ct_value, generate_ncount_value, generate_ambiguoussites, generate_NumbAlignedReads, generate_qc_values, gen_whovariant_samplingdate


fake = Faker()


def Covidplots_view(record_amount, sequencedsample_ids, sample_ids, batch_ids, consensus_ids, pangolin_ids, nextclade_ids):
    Covidplots_view_data = []
    starting_time = time.time()
    update_time = 0.15

    #random date 2 years back for DateSequencing and SampleDateTime
    two_years_SampleDateSequencing = datetime2.now() - timedelta(days=2*365)
    #random date 2 years back for Batchdate
    two_years_BatchDate = datetime2.now() - timedelta(days=2*365)


    #variables and their weights for batch_data
    platforms = [None, 'illumina qiaseq', 'nanopore', 'Illumina']
    platform_weights = [17, 20, 879, 1044]
    Batch_sources = ['Neverland', 'Gilead', 'Asgard', 'Agrabah', 'Panem', 'Narnia', 'Hogwarts', 'Middle-Earth', 'Wakanda', 'Pandora', 'Westeros']
    Batch_sources_weights = [41, 286, 100, 106, 16, 271, 865, 66, 127, 98, 2]


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

    version_possibilities = pd.read_csv('important_files/versions.csv').dropna()

    # Read the CSV file
    Nextclade_pango_essentials = pd.read_csv('important_files/Nextclade_pango_essentials.csv')
    weights_essentials = Nextclade_pango_essentials.iloc[:, -1].tolist()
    
    

    for i in range(record_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} Covidplots_view records')
        sequencedsample_id = sequencedsample_ids[i]
        sample_id = sample_ids[i]
        batch_id = batch_ids[i]
        consensus_id = consensus_ids[i]
        pangolin_id = pangolin_ids[i]
        nextclade_id = nextclade_ids[i]

        essentials = Nextclade_pango_essentials.sample(n=1, weights=weights_essentials).iloc[0]

        if essentials['LineagesOfInterest'] == "Alpha":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2020-09-18", "2022-02-01", "2021-04-22", 501) #501 = standard deviation / days between min and max
        elif essentials['LineagesOfInterest'] == "Beta":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2021-01-10", "2021-07-19", "2021-04-03", 190)
        elif essentials['LineagesOfInterest'] == "Gamma":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2020-10-12", "2021-07-30", "2021-04-22", 291)
        elif essentials['LineagesOfInterest'] == "Delta":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2021-03-30", "2022-02-27", "2021-10-12", 334)
        elif essentials['LineagesOfInterest'] == "Eta":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2021-01-14", "2021-07-21", "2021-03-12", 188)
        elif essentials['LineagesOfInterest'] == "Omicron":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2021-02-20", "2022-03-01", "2022-01-26", 374)
        elif essentials['LineagesOfInterest'] == "BA.2":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2021-02-20", "2022-03-01", "2022-02-03", 374)
        elif essentials['LineagesOfInterest'] == "BA.1":
            random_date_SampleDateSequencing = gen_whovariant_samplingdate("2021-11-22", "2022-03-01", "2022-01-17", 99)

        #random date for DateSequencing and SampleDateTime
        formatted_date_SampleDateSequencing = random_date_SampleDateSequencing.strftime("%Y-%m-%d")
        
        
        # Generate a random time of day
        random_time = fake.time_object()
        # Combine date and time to create a datetime object (TODO maybe change so that only first 2 pairs of numbers show)
        sample_SampleDateSequencing = datetime2.combine(random_date_SampleDateSequencing, random_time)
        #Random date for BatchDate
        random_date_BatchDate = fake.date_between(start_date=two_years_BatchDate, end_date='today')
        formatted_date_BateDate = random_date_BatchDate.strftime("%Y-%m-%d")


        #selecting platform based on weight
        Batch_platform = random.choices(platforms, platform_weights)[0]
        Batch_source = random.choices(Batch_sources, Batch_sources_weights)[0]


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

        version = str(version_possibilities['version'].sample(n=1, weights=version_possibilities['amount_nextclade_pangos'].tolist()).values[0])

        
        qc_data = generate_qc_values('important_files/qc_mixedsites_possibilities.csv')
        qc_mixedsites_totalmixedsites = qc_data[0]
        qc_overallscore = qc_data[1]
        qc_ocerallstatus = qc_data[2]

        record = {
            "SequencedSampleID": sequencedsample_id,
            "SequencingType": fake.random_element(elements=("hospital_sequencing", "test", "Hogwarts_sequencing_sent_to_Panem", "historic",
                                                        "Panem_sequencing", "live", "project", "hostital")), # er nogle variabler påvirket af SequencingType?
            "DateSequencing": fake.date_between(datetime1.date(2020, 9, 17), datetime1.date(2022, 10, 3)),
            "SampleContent": "RNA",
            "SampleID": sample_id,
            "SampleDateTime": sample_SampleDateSequencing,
            "Host": 'human',
            "Ct": generate_ct_value(),
            "DateSampling": formatted_date_SampleDateSequencing, #based on lineageofinterest
            "BatchID": batch_id,
            "BatchDate": formatted_date_BateDate,
            "Platform": Batch_platform,
            "BatchSource": Batch_source, 
            "ConsensusID": consensus_id,
            "NCount": manualExclusion_values['ncount'],
            "AmbiguousSites": manualExclusion_values["ambiguoussites"],
            "NwAmb": manualExclusion_values['NwAmb'], 
            "NCountQC": ncountqc,
            "NumAlignedReads": manualExclusion_values['numalignedreads'], #hvilke variabler påvirker denne?
            "PctCoveredBases": pctcoveredbases, 
            "SeqLength": random.randint(29300, 30402), #er det fint alle sequencelængder bare er mellem dette? eller er det vigtigt med specifikke værdier
            "QcScore": manualExclusion_values["qcscore"],
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
            "WhoVariant": essentials["WhoVariant"], #skal vælges ud fra nextclade_pango
            "LineagesOfInterest": essentials['LineagesOfInterest'], # skal vælges ud fra nextclade_pango
            "UnaliasedPango": essentials['UnaliasedPango'], #skal vælges ud fra Nextclade_Pango
            "PangolinResultID": pangolin_id,
            "lineage": essentials["lineage"], #skal vælges ud fra Nextclade_Pango
            "version": version,
            "pangolin_version": random.choice(['4.2', '4.1.2']), #real data: 4.2 = 26, 4.1.2 = 525417, NULL = 85643
            "scorpio_version": "0.3.17", #real data: 0.3.17 = 525443, NULL = 85643
            "constellation_version": "v0.1.10", #real data: v0.1.10 = 525443, NULL = 85643
            "qc_status": "pass", #real data: pass = 525443, NULL = 85643
            "qc_notes": "some_qc_note", #TODO if needed
            "note": "some_note", #TODO if needed
            "NextcladeResultID": nextclade_id,
            "frameShifts": None, #excluded
            "aaSubstitutions": None, #excluded
            "aaDeletions": None, #excluded
            "aaInsertions": None, #excluded
            "alignmentScore": random.randint(87816,89709), #min and max values from real data TODO what is alignmentScore?
            "clade": essentials["clade"], #TODO should match Nextclade_Pango
            "Nextclade_pango": essentials['Nextclade_pango'], #TODO This is the main generated item, where clade, lineage, UnaliasedPango, LineageOfInterest and WhoVariant are generated
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
            "NextcladeVersion": random.choice(["nextclade 2.6.0","nextclade 2.4.0","nextclade 2.9.1","nextclade 2.5.0"])
        }
        Covidplots_view_data.append(record)
    print(f'generated {i + 1} pangolin records in total')
    return Covidplots_view_data

if __name__ == '__main__':
    start_time = time.time()
    
    #record amount (max is 999999.00)
    record_amount = 1000

    Covidplots_view_headers = [
        "SequencedSampleID", "SequencingType", "DateSequencing", "SampleContent", "SampleID", "SampleDateTime", "Host", "Ct", "DateSampling",
        "BatchID", "BatchDate", "Platform", "BatchSource", "ConsensusID", "NCount", "AmbiguousSites", "NwAmb", "NCountQC",
        "NumAlignedReads", "PctCoveredBases", "SeqLength", "QcScore", "SequenceExclude", "ManualExclude", "Alpha", "Beta",
        "Gamma", "Delta", "Eta", "Omicron", "BA.1", "BA.2", "BG", "BA.4", "BA.5", "BA.2.75", "BF.7", "WhoVariant",
        "LineagesOfInterest", "UnaliasedPango", "PangolinResultID", "lineage", "version", "pangolin_version", "scorpio_version",
        "constellation_version", "qc_status", "qc_notes", "note", "NextcladeResultID", "frameShifts", "aaSubstitutions",
        "aaDeletions", "aaInsertions", "alignmentScore", "clade", "Nextclade_pango", "substitutions", "deletions", "insertions",
        "missing", "nonACGTNs", "pcrPrimerChanges", "qc.mixedSites.totalMixedSites", "qc.overallScore", "qc.overallStatus",
        "qc.frameShifts.status", "qc.frameShifts.frameShiftsIgnored", "NextcladeVersion"
    ]

    #generating unique ids
    existing_sample_ids = set()
    existing_batch_ids = set()
    existing_consensus_ids = set()
    existing_pango_ids = set()
    existing_sequencedsample_ids = set()
    existing_nextcladeresult_ids = set()

    sample_ids = [GenerateUniqueSampleID(existing_sample_ids) for i in range(record_amount)]
    batch_ids = [GenerateUniqueBatchID(existing_batch_ids) for i in range((record_amount))]  #generate enough batch IDs
    batch_ids = [batch_id for batch_id in batch_ids for i in range(100)]  # repeat each batch ID 100 times
    batch_ids = batch_ids[:record_amount]
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pangolin_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]
    sequencedsample_ids = [GenerateUniqueSequencedSampleID(existing_sequencedsample_ids) for i in range(record_amount)]
    nextclade_ids = [GenerateUniqueNextcladeResultID(existing_nextcladeresult_ids) for i in range(record_amount)]

    Covidplots_view_data = Covidplots_view(record_amount, sequencedsample_ids, sample_ids, batch_ids, consensus_ids, pangolin_ids, nextclade_ids)

    write_to_csv('Covid_plots_data.csv', Covidplots_view_data, Covidplots_view_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")