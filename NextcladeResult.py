from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2
import datetime as datetime1
import time

fake = Faker()

# Global Variables #
record_amount = 10000 ## Change for desired record amount
# Global Variables #

NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                           "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                           "pcrPrimerChanges", "qc_mixedSites_totalMixedSited", "qc_overallScore", "qc_overallStatus", "qc_frameShifts_status", 
                           "qc_frameShifts_frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]

def GenerateUniqueNextcladeResultID(existing_ids):
    while True:
        NextcladeResult_id = "Nextclade-" + str(random.randint(0, 999999)).zfill(6)
        if NextcladeResult_id not in existing_ids:
            return NextcladeResult_id

def NextcladeResult(record_amount):
    NextcladeResult_data = []
    existing_Nextclade_ids = set()
    for i in range(record_amount):
        nextcladeresult_id = GenerateUniqueNextcladeResultID(existing_Nextclade_ids)
        existing_Nextclade_ids.add(nextcladeresult_id)
        record = {
            "NextcladeResultID": nextcladeresult_id,
            "frameShifts": fake.random_element(elements=("S:159-1274", "ORF1a:3607-4401", "N:21-420;ORF9b:18-98", 
                                                         "S:70-1274", "S:6-1274", "ORF8:122", None)), #TODO figure out wtf frameShifts are 
            "aaSubstitutions": fake.random_element(elements=("M:I82T;N:D63G;N:R203M;N:G215C;N:D377Y;ORF1a:A1306S;ORF1a:P2046L;ORF1a:L2146F;ORF1a:P2287S;ORF1a:A2529V;ORF1a:V2930L;ORF1a:T3255I;ORF1a:T3646A;ORF1b:P314L;ORF1b:G662S;ORF1b:P1000L;ORF1b:A1918V;ORF3a:S26L;ORF7a:V82A;ORF7a:T120I;ORF7b:T40I;ORF9b:T60A;S:T19R;S:T95I;S:G142D;S:Y145H",
                                                             "N:A220V;ORF1a:T614I;ORF1b:P314L;ORF1b:Q813H;ORF3a:L111S;ORF9b:P39L;S:A222V;S:D614G",
                                                             "N:D3L;N:R203K;N:G204R;N:S235F;ORF1a:T1001I;ORF1a:T1241I;ORF1a:A1708D;ORF1a:I2230T;ORF1b:P314L;ORF3a:L85F;ORF3a:W131C;ORF7a:Q94L;ORF8:Q27*;ORF8:R52I;ORF8:K68*;ORF8:Y73C",
                                                             "N:T265I;ORF1a:G379E;ORF1a:K1895N;ORF1a:I2501T;ORF1a:M4241I;ORF3a:T32I;ORF3a:P240S;S:N439K;S:D614G;S:S1252F")), #TODO also figure out tf this is
            "aaDeletions": fake.random_element(elements=("ORF8:D119-;ORF8:F120-;S:E156-;S:F157-;S:R158-",
                                                         "ORF1a:L3606-",
                                                         "ORF1a:S3675-;ORF1a:G3676-;ORF1a:F3677-;S:I68-;S:H69-",
                                                         "S:H69-;S:V70-")), #TODO also figure out this
            "aaInsertions": fake.random_element(elements=(None,
                                                          "S:214:EPE",
                                                          "S:210:IV",
                                                          "ORF7a:69:NN*;ORF7a:79:T")), #TODO also figure this out
            "alignmentScore": random.randint(89000, 89700),
            "clade": 
        }
        NextcladeResult_data.append(record)
    print(f"Sample data generated {record_amount} times")
    return NextcladeResult_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")

if __name__ == '__main__':
    start_time = time.time()
    
    NextcladeResult_data = NextcladeResult(record_amount) #warning: do not make more that 1000000 records (not enough unique IDs)
    write_to_csv('NextcladeResult_data.csv', NextcladeResult_data, NextcladeResult_headers)

    end_time = time.time()
    time_passed = end_time - start_time
    print(f"Execution time: {time_passed:.5} seconds")