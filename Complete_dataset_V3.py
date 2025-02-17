from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
import numpy as np
from datetime import datetime as datetime, timedelta
import datetime as datetime1
import time
from id_generators import GenerateUniqueSampleID, GenerateUniqueConsensusID, GenerateUniqueNextcladeResultID, GenerateUniqueSequencedSampleID, GenerateUniquePangolinResultID, GenerateUniqueBatchID
from utility_V2 import write_to_csv, generate_ct_value, generate_qc_values, generate_NumbAlignedReads, generate_ncount_value, generate_ambiguoussites, gen_whovariant_datesampling, generate_exclusion_values, generate_BatchSource, clean_string_fields
import pandas as pd
from collections import Counter

fake = Faker()

def Generate_complete_data(Batch_amount: int):


    starting_time = time.time()
    update_time = 0.15

    #Existing IDs (ID cannot be reused)
    existing_ConsensusIDs = set()
    existing_SequencedSampleIDs = set()
    existing_NextcladeResultIDs = set()
    existing_SampleIDs = set()
    existing_BatchIDs = set()
    existing_PangolinResultIDs = set()

    #Datasets
    Consensus_data = []
    NextcladeResult_data = []
    Sample_data = []
    Batch_data = []
    PangolinResult_data = []
    SequencedSample_data = []

    #Complete reference data:
    #1 row is 1 possible combination in a record
    #BatchSource,DateSampling,WhoVariant,LineagesOfInterest,lineage,UnaliasedPango,Nextclade_pango,clade,weight
    reference_data = pd.read_csv('important_files/Complete_reference_data.csv', na_values=["NULL"])

    #Version reference data
    #version,weight
    version_df = pd.read_csv('important_files/versions.csv')
    version_possibilities = version_df['version'].tolist()
    version_possibilities_weights = version_df['weight'].tolist()

    
    #starting record creation (1 at a time)
    for i in range(Batch_amount):
        elapsed_time = time.time() - starting_time
        if elapsed_time >= update_time:
            update_time += 0.15
            print(f'generated {i} Batches of {Batch_amount}')

        # Generate batch-level constants first
        BatchID = GenerateUniqueBatchID(existing_BatchIDs)
        
        # Get initial row to determine batch date and source
        initial_row = reference_data.sample(n=1, weights=reference_data['weight']).iloc[0]
        BatchDate_unfixed = gen_whovariant_datesampling(initial_row['LineagesOfInterest'], reference_data)
        BatchDate = BatchDate_unfixed + timedelta(days=2)
        BatchSource = generate_BatchSource(initial_row['LineagesOfInterest'], BatchDate_unfixed, reference_data)
        Platform = random.choices([None, 'illumina qiaseq', 'nanopore', 'Illumina'], 
                                weights=[17, 20, 879, 1044])[0]

        # Create batch record
        batch_record = {
            "BatchID": BatchID,
            "BatchDate": BatchDate,
            "Platform": Platform,
            "BatchSource": BatchSource,
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Batch_data.append(clean_string_fields(batch_record))

        # Filter reference data for valid combinations matching batch date and source
        valid_combinations = reference_data[
            (reference_data['BatchSource'] == BatchSource) & 
            (reference_data['DateSampling'] == BatchDate_unfixed.strftime('%Y-%m-%d'))
        ]

        # Add these checks
        if valid_combinations.empty:
            continue  # Skip this batch if no valid combinations exist

        #making valid samples for the batch
        valid_samples = 0
        max_attempts = 1000  # Safety limit to prevent infinite loops
        attempts = 0
        while valid_samples < random.randint(36, 164) and attempts < max_attempts:
            attempts += 1
            ConsensusID = GenerateUniqueConsensusID(existing_ConsensusIDs)
            SequencedSampleID= GenerateUniqueSequencedSampleID(existing_SequencedSampleIDs)
            NextcladeResultID = GenerateUniqueNextcladeResultID(existing_NextcladeResultIDs)
            SampleID = GenerateUniqueSampleID(existing_SampleIDs)
            PangolinResultID = GenerateUniquePangolinResultID(existing_PangolinResultIDs)

            # Sample from valid combinations for this sample
            sample_row = valid_combinations.sample(n=1, weights=valid_combinations['weight']).iloc[0]

            ######################## Consensus_data ########################
            #NCount
            #above 3k = not passed (see constraints)
            #below 3k = Lineage TODO: not implemented
            NCount = generate_ncount_value()

            #AmbiguousSites
            # If AmbiguousSites over 5, then NcountQC = fail (see constraints)
            AmbiguousSites = generate_ambiguoussites()

            #NwAmb
            NwAmb = NCount + AmbiguousSites
            
            #NCountQC
            NCountQC = None
            if NwAmb <= 130:
                NCountQC = "HQ"
            elif NwAmb > 130 and NwAmb <= 3000:
                NCountQC = "MQ"
            else:
                NCountQC = "fail"
            if AmbiguousSites > 5:
                NCountQC = "fail"

            #NumAlignedReads 
            NumAlignedReads = generate_NumbAlignedReads()

            #PctCoveredBases
            PctCoveredBases = None
            if NCountQC == "HQ":
                PctCoveredBases = round(random.uniform(99.56, 100.00), 2)
            elif NCountQC == "MQ":
                PctCoveredBases = round(random.uniform(89.83, 99.57), 2)
            else:
                PctCoveredBases = round(random.uniform(0.00, 90.12), 2)

            #SeqLength
            SeqLength = random.randint(29300, 30402)

            #ManualExclude, SequenceExclude, QcScore
            QcScore = None
            SequenceExclude = None
            ManualExclude = None
            Exclusion_values = generate_exclusion_values()
            QcScore = Exclusion_values['qc_score']
            SequenceExclude = Exclusion_values['sequence_exclude']
            ManualExclude = Exclusion_values['manual_exclude']

            #WhoVariant, LineagesOfInterest, UnaliasedPango
            WhoVariant = sample_row['WhoVariant']
            LineageOfInterest = sample_row['LineagesOfInterest']
            UnaliasedPango = sample_row['UnaliasedPango']
            if pd.isna(WhoVariant):
                WhoVariant = None
            if pd.isna(LineageOfInterest):
                LineageOfInterest = None
            if pd.isna(UnaliasedPango):
                UnaliasedPango = None

            #Alpha, Beta, Gamma, Delta, Eta, Omicron, BA.1, BA.2, BG, BA.4, BA.5, BA.2.75, BF.7
            Alpha = 0
            Beta = 0
            Gamma = 0
            Delta = 0
            Eta = 0 
            Omicron = 0
            BA_1 = 0
            BA_2 = 0
            BG = 0
            BA_4 = 0
            BA_5 = 0
            BA_2_75 = 0
            BF_7 = 0
            if LineageOfInterest == "Alpha":
                Alpha = 1
            elif LineageOfInterest == "Beta":
                Beta = 1
            elif LineageOfInterest == "Gamma":
                Gamma = 1
            elif LineageOfInterest == "Delta":
                Delta = 1
            elif LineageOfInterest == 'Eta':
                Eta = 1
            elif LineageOfInterest == "Omicron":
                Omicron = 1
            elif LineageOfInterest == "BA.1":
                Omicron = 1
                BA_1 = 1
            elif LineageOfInterest == "BA.2":
                Omicron = 1
                BA_2 = 1
            
            #IsCurrent 
            # always current in test data
            IsCurrent = 1

            #TimestampCreated
            TimestampCreated = str(datetime.now())

            #TimestampUpdated
            TimestampUpdated = str(datetime.now())

            ######################## NextcladeResult_data ########################
            
            #frameShifts, aaSubstitutions, aaDeletions, aaInsertions
            frameShifts = None #excluded
            aaSubstitutions = None #excluded
            aaDeletions = None #excluded
            aaInsertions = None #excluded

            #alignmentScore
            alignmentScore = random.randint(87816, 89709)

            #clade, Nextclade_pango
            clade = sample_row['clade']
            Nextclade_pango = sample_row['Nextclade_pango']
            if pd.isna(clade):
                clade = None
            if pd.isna(Nextclade_pango):
                Nextclade_pango = None
            
            #substitutions, deletions, insertions, missing, nonACGTNs, pcrPrimerChanges
            substitutions = None #excluded
            deletions = None #excluded
            insertions = None #excluded
            missing = None #excluded
            nonACGTNs = None #excluded
            pcrPrimerChanges = None #excluded

            #qc.mixedSites.totalMixedSites, qc.overallScore, qc.overallStatus
            qc_data = generate_qc_values('important_files/qc_mixedsites_possibilities.csv')
            qc_mixedSites_totalMixedSites = qc_data[0]
            qc_overallScore = qc_data[1]
            qc_ocerallStatus = qc_data[2]

            #qc.frameShifts.status, qc.frameShifts.frameShiftsIgnored
            qc_frameShifts_status = None #excluded
            qc_frameShifts_frameShiftsIgnored = None #excluded

            #NextcladeVersion
            NextcladeVersion = fake.random_element(elements=("nextclade 2.5.0", "nextclade 2.6.0", "nextclade 2.4.0"))

            ######################## Sample_data ########################

            #Host
            Host = 'Human'

            #Ct
            #check korreletion med ncount eller ncountQC eller SeqLength
            Ct = generate_ct_value()

            #DateSampling
            DateSampling = BatchDate_unfixed

            #SampleDateTime 
            SampleDateTime = datetime.combine(DateSampling, fake.time_object()) if DateSampling else None

            ######################## PangolinResult_data ########################

            #lineage
            lineage = sample_row['lineage']
            if pd.isna(lineage):
                lineage = None

            #version
            if pd.isna(lineage):
                version = None
            else:
                version = random.choices(version_possibilities, weights=version_possibilities_weights)[0]
            
            if pd.isna(version):
                version = None

            #pangolin_version
            pangolin_version_variants = ("4.2", "4.1.2")
            if pd.isna(lineage):
                pangolin_version = None
            else:
                pangolin_version = random.choices(pangolin_version_variants)[0]

            #scopio_version
            if pd.isna(lineage):
                scopio_version = None
            else:
                scopio_version = "0.3.17"

            #constellation_version
            if pd.isna(lineage):
                constellation_version = None
            else: 
                constellation_version = 'v0.1.10'

            #qc_status
            if pd.isna(lineage):
                qc_status = None
            elif NCount > 3000 or NCountQC == "fail":
                qc_status = "fail"
            else:
                qc_status = "pass"

            #qc_notes
            if pd.isna(lineage):
                qc_notes = None
            else:
                qc_notes = "nothing of note"

            #note
            if pd.isna(lineage):
                note = None
            else:
                note = "again nothing"

            ######################## SequencedSample_data ########################
            
            #SequencingType
            SequencingType_elements=("hospital_sequencing", "test", "Hogwarts_sequencing_sent_to_Panem", "historic",
                                                                "Panem_sequencing", "live", "project", "hospital")
            SequencingType = random.choices(SequencingType_elements)[0]

            #DateSequencing
            #TODO should match the batch date?
            DateSequencing = fake.date_between(start_date=BatchDate, end_date=BatchDate + timedelta(days=4))

            #SampleContent
            SampleContent = "RNA"

            ######################## Constraints ########################

            #Check all constraints
            if (NCountQC == "fail" or 
                qc_status == "fail" or 
                AmbiguousSites > 5 or
                (NCount < 3000 and DateSampling.date() > datetime.strptime('2021-05-15', '%Y-%m-%d').date() and pd.isna(LineageOfInterest)) or
                (DateSampling.date() > datetime.strptime('2021-03-1', '%Y-%m-%d').date() and random.randint(1,3) in [1, 2] and pd.isna(LineageOfInterest)) or
                (pd.isna(LineageOfInterest) and random.randint(1,5) in [1,2])):
                continue
            # If we get here, the sample passed all constraints
            valid_samples += 1

            ######################## RECORDS ########################

            Consensus_record = {
                # Consensus_data record
                "ConsensusID": ConsensusID,
                "NCount": NCount, #above 3k = not passed 
                "AmbiguousSites": AmbiguousSites, # over 5, then NcountQC = fail 
                "NwAmb": NwAmb,
                "NCountQC": NCountQC,
                "NumAlignedReads": NumAlignedReads,
                "PctCoveredBases": PctCoveredBases,
                "SeqLength": SeqLength,
                "QcScore": QcScore,
                "SequenceExclude": SequenceExclude,
                "ManualExclude": ManualExclude,
                "Alpha": Alpha,
                "Beta": Beta,
                "Gamma": Gamma,
                "Delta": Delta,
                "Eta": Eta,
                "Omicron": Omicron,
                "BA.1": BA_1,
                "BA.2": BA_2,
                "BG": BG,
                "BA.4": BA_4,
                "BA.5": BA_5,
                "BA.2.75": BA_2_75,
                "BF.7": BF_7,
                "WhoVariant": WhoVariant,
                "LineagesOfInterest": LineageOfInterest,
                "UnaliasedPango": UnaliasedPango,
                "SequencedSampleID": SequencedSampleID,
                "CurrentNextcladeID": NextcladeResultID,
                "CurrentPangolinID": PangolinResultID,
                "IsCurrent": IsCurrent,  # always current in test data
                "TimestampCreated": TimestampCreated,
                "TimestampUpdated": TimestampUpdated
            }
            NextcladeResult_record = {
                "NextcladeResultID": NextcladeResultID,
                "frameShifts": frameShifts, #excluded
                "aaSubstitutions": aaSubstitutions, #excluded
                "aaDeletions": aaDeletions, #excluded
                "aaInsertions": aaInsertions, #excluded
                "alignmentScore": alignmentScore, #min and max values from real data
                "clade": clade,
                "Nextclade_pango": Nextclade_pango,
                "substitutions": substitutions, #excluded
                "deletions": deletions, #excluded
                "insertions": insertions, #excluded
                "missing": missing, #excluded
                "nonACGTNs": nonACGTNs, #excluded
                "pcrPrimerChanges": pcrPrimerChanges, #excluded
                "qc.mixedSites.totalMixedSites": qc_mixedSites_totalMixedSites,
                "qc.overallScore": qc_overallScore,
                "qc.overallStatus": qc_ocerallStatus,
                "qc.frameShifts.status": qc_frameShifts_status, #excluded
                "qc.frameShifts.frameShiftsIgnored": qc_frameShifts_frameShiftsIgnored, #excluded
                "NextcladeVersion": NextcladeVersion,
                "ConsensusID": ConsensusID,
                "IsCurrent": IsCurrent,
                "TimestampCreated": TimestampCreated,
                "TimestampUpdated": TimestampUpdated
            }
            Sample_record = {
                "SampleID": SampleID,
                "Host": Host,
                "Ct": Ct, #check korreletion med ncount eller ncountQC eller SeqLength
                "DateSampling": DateSampling,
                "CurrentConsensusID": ConsensusID,
                "TimestampCreated": TimestampCreated,
                "TimestampUpdated": TimestampUpdated,
                "SampleDateTime": SampleDateTime
            }
            PangolinResult_record = {
                "PangolinResultID": PangolinResultID,
                "lineage": lineage, #skal vælges ud fra Nextclade_Pango
                "version": version,
                "pangolin_version": pangolin_version, #real data: 4.2 = 26, 4.1.2 = 525417, NULL = 85643
                "scorpio_version": scopio_version, #real data: 0.3.17 = 525443, NULL = 85643
                "constellation_version": constellation_version, #real data: v0.1.10 = 525443, NULL = 85643
                "qc_status": qc_status, #real data: pass = 525443, NULL = 85643
                "qc_notes": qc_notes, #TODO if needed
                "note": note, #TODO if needed    
                "ConsensusID": ConsensusID,
                "IsCurrent": IsCurrent,
                "TimestampCreated": TimestampCreated,
                "TimestampUpdated": TimestampUpdated
            }
            SequencedSample_record = {
                "SequencedSampleID": SequencedSampleID,
                "SequencingType": SequencingType,
                "DateSequencing": DateSequencing, #TODO should match the batch date?
                "SampleContent": SampleContent,
                "BatchID": BatchID,  # Assign BatchID from the current batch
                "CurrentConsensusID": ConsensusID,
                "SampleID": SampleID,  # Use extracted SampleID
                "TimestampCreated": TimestampCreated,
                "TimestampUpdated": TimestampUpdated
            }

            # Clean the records before appending
            Consensus_record = clean_string_fields(Consensus_record)
            NextcladeResult_record = clean_string_fields(NextcladeResult_record)
            Sample_record = clean_string_fields(Sample_record)
            PangolinResult_record = clean_string_fields(PangolinResult_record)
            SequencedSample_record = clean_string_fields(SequencedSample_record)

            #appending
            PangolinResult_data.append(PangolinResult_record)
            SequencedSample_data.append(SequencedSample_record)
            Consensus_data.append(Consensus_record)
            NextcladeResult_data.append(NextcladeResult_record)
            Sample_data.append(Sample_record)
    
    return (Consensus_data, NextcladeResult_data, Sample_data, Batch_data, PangolinResult_data, SequencedSample_data)
            
if __name__ == '__main__':
    start_time = time.time()

    Batch_amount = 7500

    #headers "/n" represents a new file (so 6 total files)
    consensus_headers = [
        "ConsensusID", "NCount", "AmbiguousSites", "NwAmb", "NCountQC", "NumAlignedReads", "PctCoveredBases",
        "SeqLength", "QcScore", "SequenceExclude", "ManualExclude", "Alpha", "Beta", "Gamma", "Delta", "Eta",
        "Omicron", "BA.1", "BA.2", "BG", "BA.4", "BA.5", "BA.2.75", "BF.7", "WhoVariant", "LineagesOfInterest",
        "UnaliasedPango", "SequencedSampleID", "CurrentNextcladeID", "CurrentPangolinID", "IsCurrent", 
        "TimestampCreated", "TimestampUpdated"
    ]

    nextclade_headers = [
        "NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore",
        "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs",
        "pcrPrimerChanges", "qc.mixedSites.totalMixedSites", "qc.overallScore", "qc.overallStatus", 
        "qc.frameShifts.status", "qc.frameShifts.frameShiftsIgnored", "NextcladeVersion", "ConsensusID", 
        "IsCurrent", "TimestampCreated", "TimestampUpdated"
    ]

    sample_headers = [
        "SampleID", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", 
        "TimestampUpdated", "SampleDateTime"
    ]

    batch_headers = [
        "BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"
    ]

    sequencedsample_headers = [
        "SequencedSampleID", "SequencingType", "DateSequencing", "SampleContent", "BatchID",
        "CurrentConsensusID", "SampleID", "TimestampCreated", "TimestampUpdated"
    ]

    pangolin_headers = [
        "PangolinResultID", "lineage", "version", "pangolin_version", "scorpio_version", 
        "constellation_version", "qc_status", "qc_notes", "note", "ConsensusID", "IsCurrent",
        "TimestampCreated", "TimestampUpdated"
    ]

    #generating data
    (Consensus_data, NextcladeResult_data, Sample_data, Batch_data, PangolinResult_data, SequencedSample_data) = Generate_complete_data(Batch_amount)

    #make them csv files
    print("Writing data to CSV files...")
    write_to_csv('output/Consensus_data.csv', Consensus_data, consensus_headers)
    write_to_csv('output/NextcladeResult_data.csv', NextcladeResult_data, nextclade_headers)
    write_to_csv('output/Sample_data.csv', Sample_data, sample_headers)
    write_to_csv('output/Batch_data.csv', Batch_data, batch_headers)
    write_to_csv('output/SequencedSample_data.csv', SequencedSample_data, sequencedsample_headers)
    write_to_csv('output/PangolinResult_data.csv', PangolinResult_data, pangolin_headers)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")