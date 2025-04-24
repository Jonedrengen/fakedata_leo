import random



def GenerateUniqueSampleID(existing_sample_ids):
    while True:
        sample_id = "CaseSample-" + str(random.randint(0, 999999)).zfill(6)
        if sample_id not in existing_sample_ids:
            existing_sample_ids.add(sample_id)
            return sample_id

def GenerateUniqueBatchID(existing_batch_ids):
    while True:
        batch_id = "Run-" + str(random.randint(0, 999999)).zfill(6)
        if batch_id not in existing_batch_ids:
            existing_batch_ids.add(batch_id)
            return batch_id

def GenerateUniqueSequencedSampleID(existing_sequenced_ids):
    while True:
        SequencedSample_id = "SampleSequenced-" + str(random.randint(0, 999999)).zfill(6)
        if SequencedSample_id not in existing_sequenced_ids:
            existing_sequenced_ids.add(SequencedSample_id)
            return SequencedSample_id

def GenerateUniqueConsensusID(existing_consensus_ids):
    while True:
        consensus_id = "QcConsensus-" + str(random.randint(0, 999999)).zfill(6)
        if consensus_id not in existing_consensus_ids:
            existing_consensus_ids.add(consensus_id)
            return consensus_id
        
def GenerateUniquePangolinResultID(existing_pango_ids):
    while True:
        pango_id = "Pangolin-" + str(random.randint(0, 999999)).zfill(6)
        if pango_id not in existing_pango_ids:
            existing_pango_ids.add(pango_id)
            return pango_id
        
def GenerateUniqueNextcladeResultID(existing_NextcladeResult_ids):
    while True:
        NextcladeResult_id = "Nextclade-" + str(random.randint(0, 999999)).zfill(6)
        if NextcladeResult_id not in existing_NextcladeResult_ids:
            existing_NextcladeResult_ids.add(NextcladeResult_id)
            return NextcladeResult_id
