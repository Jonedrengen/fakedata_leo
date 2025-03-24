from Complete_dataset import Generate_complete_data
from datetime import datetime as datetime, timedelta
import time
from utility import write_to_csv


"""
This is the main use file, containing basics to generate datasets based on SSI covid data.

batch_amount and batch_size are the only variables you need to modify.
    #batch_amount: max size recommended 8500
    #batch_size: max size recommended 96
    NOTE: the max possible datapoints that can be created one million, due to unique id limitations. So be carefull when choosing batch_size and amount

"""


if __name__ == "__main__":
    start_time = time.time()

    #can be modified
    batch_amount = 8500
    batch_size = 96
    #can be modified

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
    (Consensus_data, NextcladeResult_data, Sample_data, Batch_data, PangolinResult_data, SequencedSample_data) = Generate_complete_data(Batch_amount=batch_amount, Batch_size=batch_size)

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