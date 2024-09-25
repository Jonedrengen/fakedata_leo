from PangolinResult import PangolinResult
from Consensus import ConsensusData, write_to_csv
from Sample import SampleData
from Batch import BatchData
from NextcladeResult import NextcladeResultData
from SequencedSample import SequencedSampleData
from id_generators import (GenerateUniquePangolinResultID, GenerateUniqueConsensusID, GenerateUniqueSampleID,
                           GenerateUniqueBatchID, GenerateUniqueSequencedSampleID, GenerateUniqueNextcladeResultID)

import time
import csv

if __name__ == '__main__':
    start_time = time.time()
    
    #record amount (max is 999999.00)
    record_amount = 500


    #headers
    Sample_headers = ["SampleID", "SampleDateTime", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated"]
    Batch_headers = ["BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"]
    Consensus_headers = ["ConsensusID", "NCount", "AmbiguousSites", "NwAmb", "NCountQC", "NumAlignedReads", "PctCoveredBases",
                     "SeqLength", "QcScore", "SequenceExclude", "ManualExclude", "Alpha", "Beta", "Gamma", "Delta", "Eta",
                     "Omicron", "BA_1", "BA_2", "BG", "BA_4", "BA_5", "BA_2_75", "BF_7", "WhoVariant", "LineagesOfInterest",
                     "UnaliasedPango", "SequencedSampleID", "CurrentNextcladeID", "CurrentPangolinID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    PangolinResult_headers = ["PangolinResultID", "lineage", "version", "pangolin_version", "scorpio_version", "constellation_version", 
                           "qc_status", "qc_notes", "note", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    SequencedSample_headers = ["SequencedSampleID", "SequencingType", "DateSequencing", "SampleContent", "BatchID", 
                           "CurrentConsensusID", "SampleID", "TimestampCreated", "TimestampUpdated"]
    NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                            "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                            "pcrPrimerChanges", "qc_mixedSites_totalMixedSited", "qc_overallScore", "qc_overallStatus", "qc_frameShifts_status", 
                            "qc_frameShifts_frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]
    
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
    nextcladeresult_ids = [GenerateUniqueNextcladeResultID(existing_nextcladeresult_ids) for i in range(record_amount)]

    #generating data
    Sample_data = SampleData(record_amount, sample_ids, consensus_ids)
    Batch_data = BatchData(record_amount // 100 + 1, batch_ids)
    Consensus_data = ConsensusData(record_amount, consensus_ids, pangolin_ids)
    PangolinResult_data = PangolinResult(record_amount, pangolin_ids, consensus_ids)
    SequencedSample_data = SequencedSampleData(record_amount, sequencedsample_ids, batch_ids, consensus_ids, sample_ids)
    NextcladeResult_data = NextcladeResultData(record_amount, nextcladeresult_ids, consensus_ids)

    #creating csv
    write_to_csv('Sample_data.csv', Sample_data, Sample_headers)
    write_to_csv('Batch_data.csv', Batch_data, Batch_headers)
    write_to_csv('Consensus_data.csv', Consensus_data, Consensus_headers)
    write_to_csv('PangolinResult_data.csv', PangolinResult_data, PangolinResult_headers)
    write_to_csv('SequencedSample_data.csv', SequencedSample_data, SequencedSample_headers)
    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)

    end_time = time.time()

    time_passed = end_time - start_time
    print(f'time passed {time_passed:.5}')