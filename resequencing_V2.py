import csv
import pandas as pd
import random
from datetime import datetime, timedelta
from id_generators_V2 import GenerateUniqueConsensusID, GenerateUniqueNextcladeResultID, GenerateUniqueSequencedSampleID, GenerateUniquePangolinResultID, GenerateUniqueBatchID
from utility import clean_string_fields, write_to_csv
from faker import Faker

fake = Faker()

def clean_nan_values(record):
    for key, value in record.items():
        if pd.isna(value):
            record[key] = None
    return record

# Read all the necessary data files
Sample_data = pd.read_csv("output/CaseSample_data.csv")
Consensus_data = pd.read_csv("output/QcVariantConsensus_data.csv", dtype={"NCount": "Int64", "AmbiguousSites": "Int64", "NwAmb": "Int64"})
NextcladeResult_data = pd.read_csv("output/ResultsNextclade_data.csv")
PangolinResult_data = pd.read_csv("output/ResultsPangolin_data.csv")
SequencedSample_data = pd.read_csv("output/SampleSequenced_data.csv")
Batch_data = pd.read_csv("output/Run_data.csv")

# Convert dataframes to lists of dictionaries for easier manipulation
sample_records = Sample_data.to_dict('records')
consensus_records = Consensus_data.to_dict('records')
nextclade_records = NextcladeResult_data.to_dict('records')
pangolin_records = PangolinResult_data.to_dict('records')
sequencedsample_records = SequencedSample_data.to_dict('records')
batch_records = Batch_data.to_dict('records')

# Initialize sets for tracking existing IDs
existing_ConsensusIDs = set(Consensus_data["QcVariantConsensusID"])
existing_SequencedSampleIDs = set(SequencedSample_data["SampleSequencedID"])
existing_NextcladeResultIDs = set(NextcladeResult_data["ResultsNextcladeID"])
existing_PangolinResultIDs = set(PangolinResult_data["PangolinID"])
existing_BatchIDs = set(Batch_data["RunID"])
print(len(existing_PangolinResultIDs))
# Get headers from the original files
consensus_headers = list(Consensus_data.columns)
nextclade_headers = list(NextcladeResult_data.columns)
pangolin_headers = list(PangolinResult_data.columns)
sequencedsample_headers = list(SequencedSample_data.columns)
batch_headers = list(Batch_data.columns)

# Select random batches to resequence instead of individual samples
num_batches_to_reuse = int(len(Batch_data) * 0.0845)  # 8,45% of batches
batches_to_reuse = Batch_data.sample(n=num_batches_to_reuse)
batch_ids_to_reuse = set(batches_to_reuse["RunID"])

print(f"Selected {len(batch_ids_to_reuse)} batches for resequencing")

#for perfromance
consensus_dict = {record["QcVariantConsensusID"]: record for record in consensus_records}
nextclade_dict = {record["ResultsNextcladeID"]: record for record in nextclade_records}
pangolin_dict = {record["PangolinID"]: record for record in pangolin_records}

# New collections for resequenced data
new_consensus_records = []
new_nextclade_records = []
new_pangolin_records = []
new_sequencedsample_records = []
new_batch_records = []


# To properly compare against the original data (not the modified set):
pangolin_ids_original = set(PangolinResult_data["PangolinID"])
additional_pangolin_ids = []

batch_counter = 0
total_batches = len(batches_to_reuse)

# looper gennem batches xxx
for i, batch in batches_to_reuse.iterrows():
    batch_counter += 1
    original_batch_id = batch["RunID"]
    #print(original_batch_id)

    #new id
    new_batch_id = GenerateUniqueBatchID(existing_BatchIDs)
    #print(new_batch_id)
    existing_BatchIDs.add(new_batch_id)

    #new resequencing date (remember data must match from original, otherwise the plots will be wrong)
    original_batch_date = pd.to_datetime(batch["RunDate"]).date()
    #print(original_batch_date)
    first_batch_date = original_batch_date - timedelta(days=random.randint(10, 40))
    #print(reseq_batch_date)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # create a new batch record (should i make NCount higher? or ambiguoussites?)
    new_batch = { 
        "RunID": new_batch_id,
        "RunDate": first_batch_date,
        "Platform": batch["Platform"],  # same platform
        "RunSource": batch["RunSource"],  # Usually same source
        "TimestampCreated": timestamp,
        "TimestampUpdated": timestamp
    }
    #print(new_batch)

    samples_in_batch = SequencedSample_data[SequencedSample_data["RunID"] == original_batch_id]
    #print(samples_in_batch)
    #print(f"Found {len(samples_in_batch)} samples in batch {original_batch_id}")

    #for each sample in the batch
    for i, sequenced_sample in samples_in_batch.iterrows():
        original_sequenced_id = sequenced_sample["SampleSequencedID"]
        original_sample_id = sequenced_sample["CaseSampleID"]
        original_consensus_id = sequenced_sample["CurrentQcVariantConsensusID"]
        #nextcladeID er først taget senere, da den ikke er i sequenced sample datasettet, men først i consensus datasettet
        #samme med pangolinID

        # generate new IDs, but not SampleID, since the same will be used
        new_sequenced_id = GenerateUniqueSequencedSampleID(existing_SequencedSampleIDs)
        new_consensus_id = GenerateUniqueConsensusID(existing_ConsensusIDs)
        new_nextclade_id = GenerateUniqueNextcladeResultID(existing_NextcladeResultIDs)
        new_pangolin_id = GenerateUniquePangolinResultID(existing_PangolinResultIDs)
        
        if new_pangolin_id in additional_pangolin_ids:
            print(f"{new_pangolin_id} found in new data!")
        additional_pangolin_ids.append(new_pangolin_id)

        if new_pangolin_id in pangolin_ids_original:
            print(f"{new_pangolin_id} found in original data!")

        # Create new sequenced sample record fake.date_between(start_date=BatchDate, end_date=BatchDate + timedelta(days=4))
        new_sequencedsample = {
            "SampleSequencedID": new_sequenced_id,
            "SequencingType": sequenced_sample["SequencingType"],
            "DateSequencing": fake.date_between(start_date=first_batch_date, end_date=first_batch_date + timedelta(days=4)),
            "SampleContent": sequenced_sample["SampleContent"],
            "RunID": new_batch_id,  # Link to new batch
            "CurrentQcVariantConsensusID": new_consensus_id,
            "CaseSampleID": original_sample_id,  #same sample
            "TimestampCreated": timestamp,
            "TimestampUpdated": timestamp
        }
        new_sequencedsample_records.append(new_sequencedsample)

        orig_consensus = consensus_dict[original_consensus_id]
        #print(orig_consensus)

        orig_nextclade_id = orig_consensus["CurrentResultsNextcladeID"]
        #print(orig_nextclade_id)
        orig_nextclade = nextclade_dict[orig_nextclade_id]

        orig_pangolin_id = orig_consensus["CurrentPangolinID"]
        orig_pangolin = pangolin_dict[orig_pangolin_id]
        
        new_consensus_record = orig_consensus.copy()
        new_consensus_record = clean_nan_values(new_consensus_record)  # Convert "nan" to None
        # opdater hvad der skal opdateres nedfor!
        new_consensus_record.update({
            "QcVariantConsensusID": new_consensus_id,
            "NCount": int(orig_consensus["NCount"]) if not pd.isna(orig_consensus["NCount"]) else None,
            "AmbiguousSites": int(orig_consensus["AmbiguousSites"]) if not pd.isna(orig_consensus["AmbiguousSites"]) else None,
            "NwAmb": int(orig_consensus["NwAmb"]) if not pd.isna(orig_consensus["NwAmb"]) else None,
            "QcScore": "Fail",
            "SequenceExclude": "ManuallyExcluded",
            "ManualExclude": "ManuallyExcluded: Sequencing_Fail",
            "SampleSequencedID": new_sequenced_id,
            "CurrentResultsNextcladeID": new_nextclade_id,
            "CurrentPangolinID": new_pangolin_id,
            "IsCurrent": 1,
            "TimestampCreated": timestamp,
            "TimestampUpdated": timestamp
        })
        new_consensus_records.append(new_consensus_record)

        # opdater nextclade med hvad der skal opdateres!
        new_nextclade = orig_nextclade.copy()
        new_nextclade = clean_nan_values(new_nextclade)  # Convert "nan" to None
        new_nextclade.update({
            "ResultsNextcladeID": new_nextclade_id,
            "QcVariantConsensusID": new_consensus_id,
            "IsCurrent": 1,
            "TimestampCreated": timestamp,
            "TimestampUpdated": timestamp
        })
        new_nextclade_records.append(new_nextclade)

        # opdater pangolin med hvad der skal opdateres
        new_pangolin = orig_pangolin.copy()
        new_pangolin = clean_nan_values(new_pangolin)
        new_pangolin.update({
            "PangolinID": new_pangolin_id,
            "QcVariantConsensusID": new_consensus_id,
            "IsCurrent": 1,
            "TimestampCreated": timestamp,
            "TimestampUpdated": timestamp
        })
        new_pangolin_records.append(new_pangolin)

    print(f"Created {len(samples_in_batch)} new records for resequenced batch {original_batch_id} num {batch_counter} of {len(batch_ids_to_reuse)}")
    new_batch_records.append(new_batch)
#append til eksisterende csv fil
def append_to_csv(filename, records, headers):
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        for record in records:
            writer.writerow(record)

# Append new records to their respective files
append_to_csv('output/QcVariantConsensus_data.csv', new_consensus_records, consensus_headers)
append_to_csv('output/ResultsNextclade_data.csv', new_nextclade_records, nextclade_headers)
append_to_csv('output/ResultsPangolin_data.csv', new_pangolin_records, pangolin_headers)
append_to_csv('output/SampleSequenced_data.csv', new_sequencedsample_records, sequencedsample_headers)
append_to_csv('output/Run_data.csv', new_batch_records, batch_headers)

print(f"Added {len(new_batch_records)} new batches with {len(new_sequencedsample_records)} resequenced samples")