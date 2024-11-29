from faker import Faker
import random
import csv
import datetime as datetime1
from datetime import datetime as datetime2, timedelta
import time

from id_generators import (GenerateUniquePangolinResultID, GenerateUniqueConsensusID, GenerateUniqueSequencedSampleID, 
                           GenerateUniqueNextcladeResultID, GenerateUniqueBatchID, GenerateUniqueSampleID)
from utility import write_to_csv, generate_ct_value, generate_ncount_value, generate_ambiguoussites, generate_NumbAlignedReads


fake = Faker

if __name__ == '__main__':
    start_time = time.time()
    
    #record amount (max is 999999.00)
    record_amount = 50000

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
    batch_ids = [GenerateUniqueBatchID(existing_batch_ids) for i in range(record_amount // 100 + 1)] #change for batch size
    consensus_ids = [GenerateUniqueConsensusID(existing_consensus_ids) for i in range(record_amount)]
    pangolin_ids = [GenerateUniquePangolinResultID(existing_pango_ids) for i in range(record_amount)]
    sequencedsample_ids = [GenerateUniqueSequencedSampleID(existing_sequencedsample_ids) for i in range(record_amount)]
    nextclade_ids = [GenerateUniqueNextcladeResultID(existing_nextcladeresult_ids) for i in range(record_amount)]

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


            #random date for DateSequencing and SampleDateTime
            random_date_SampleDateSequencing = fake.date_between(start_date=two_years_SampleDateSequencing, end_date='today')
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

            if manualExclusion_values['qcscore'] == None:
                manualExclusion_values['numalignedreads'] = None
            else:
                manualExclusion_values['numalignedreads'] = generate_NumbAlignedReads()



            record = {
                "SequencedSampleID": sequencedsample_id,
                "SequencingType": fake.random_element(elements=("hospital_sequencing", "test", "Hogwarts_sequencing_sent_to_Panem", "historic",
                                                            "Panem_sequencing", "live", "project", "hostital")),
                "DateSequencing": fake.date_between(datetime1.date(2020, 9, 17), datetime1.date(2022, 10, 3)), #TODO should match the batch date?
                "SampleContent": "RNA",
                "SampleID": sample_id,
                "SampleDateTime": sample_SampleDateSequencing,
                "Host": 'human',
                "Ct": generate_ct_value(), #TODO this should follow the real data
                "DateSampling": formatted_date_SampleDateSequencing,
                "BatchID": batch_id,
                "BatchDate": formatted_date_BateDate,
                "Platform": Batch_platform,
                "BatchSource": Batch_source, 
                "ConsensusID": consensus_id,
                "NCount": manualExclusion_values['ncount'], #TODO this should match real data
                "AmbiguousSites": manualExclusion_values["ambiguoussites"], #TODO this should match real data
                "NwAmb": manualExclusion_values['nwamb'], #TODO this should match real data
                "NCountQC": ncountqc,
                "NumAlignedReads": manualExclusion_values['numalignedreads'],
                "PctCoveredBases": 

            }
