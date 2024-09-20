from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime as datetime2
import datetime as datetime1
import time
from Consensus import ConsensusData

fake = Faker()

# Global Variables #
record_amount = 10000 ## Change for desired record amount
# Global Variables #

NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                           "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                           "pcrPrimerChanges", "qc_mixedSites_totalMixedSited", "qc_overallScore", "qc_overallStatus", "qc_frameShifts_status", 
                           "qc_frameShifts_frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]

def extract_column(data, column_header):
    column = [record[column_header] for record in data]
    return column


def GenerateUniqueNextcladeResultID(existing_ids):
    while True:
        NextcladeResult_id = "Nextclade-" + str(random.randint(0, 999999)).zfill(6)
        if NextcladeResult_id not in existing_ids:
            return NextcladeResult_id

def NextcladeResult(record_amount):
    NextcladeResult_data = []
    Consensus_data = ConsensusData(record_amount)
    extracted_consensus_ids = extract_column(Consensus_data, "ConsensusID")
    existing_Nextclade_ids = set()
    for i in range(record_amount):
        nextcladeresult_id = GenerateUniqueNextcladeResultID(existing_Nextclade_ids)
        existing_Nextclade_ids.add(nextcladeresult_id)
        consensus_id = extracted_consensus_ids.pop(0)
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
            "clade": fake.random_element(elements=(None, "20A", "20E (EU1)", "20D", "21F (Iota)", "21H (Mu)", "21G (Lambda)", "20B", "20G", "recombinant", 
                                                   "21D (Eta)", "20I (Alpha; V1)", "21J (Delta)", "21C (Epsilon)", "21L (Omicron)", "20H (Beta; V2)",
                                                   "21M (Omicron)", "21B (Kappa)", "21K (Omicron)", "19B", "21I (Delta)", "20C", "19A", "21A (Delta)",
                                                   "20J (Gamma; V3)")), #contains all possible clades as per dataset from Leo
            "Nextclade_pango": fake.random_element(elements=("AY.4.6", "B.1.177.12", "AY.4.2.3", "AY.60", "BA.1.1.13", "BC.2", "XV")),
            "substitutions": fake.random_element(elements=("C241T;C3037T;T7767C;C8047T;G12988T;C14408T;G15598A;C17104T;G18028T;A18030G;C18681T;A20268G;C20451T;C22879A;A23403G;T24910C;C25919T;T26972C;C27800A;G29734C", 
                                                           "T670G;C2790T;C3037T;G4184A;C4321T;C9344T;A9424G;C9534T;C9866T;C10029T;C10198T;G10447A;C10449A;C12880T;C14408T;C15714T;T17112C;C17410T;A18163G;C19955T;A20055G;G21987A;T22200G;G22578A;C22674T;T22679C;C22686T;A22688G;G22775A;A22786C;C22792T;G22813T;A23403G;C23525T;T23599G;C23604A;C23854A;G23948T;A24424T;T24469A;C25000T;C25584T;C25624T;C26060T;C26270T;C26577G;G26709A;C26858T;A27259C;G27382C;A27383T;T27384C;C27807T;A28271T;C28311T;G28881A;G28882A;G28883C;A29510C", 
                                                           "G210T;C241T;C3037T;G4181T;C6402T;C7124T;C7851T;C8986T;G9053T;C10029T;A11201G;A11332G;C14408T;G14829T;G15451A;C16466T;G17193T;C19220T;C21618G;C21846T;T22917G;C22995A;A23403G;C23604G;G24410A;C25469T;G26416T;T26767C;T27638C;C27752T;C27874T;C28291T;A28461G;G28881T;G28916T;G29402T;G29742T", 
                                                           "G61T;C140T;T209C;G210T;C241T;A2276G;T2308C;C3037T;G4181T;C6402T;C7124T;C7851T;C8964T;C8986T;G9053T;A9685G;C10029T;T10084A;A10323G;G10688T;A11201G;A11332G;C14408T;G15451A;C16293T;C16466T;T17040C;C19220T;C19524T;C20404T;C21618G;C21846T;G21987A;T22917G;C22995A;G23012C;A23403G;C23604G;G24410A;C25469T;T26767C;T27638C;C27752T;C27874T;A28461G;G28881T;G28916T;A28967G;G28979T;G28980T;G29402T;G29742T", 
                                                           )),
            "deletions": fake.random_element(elements=("22029-22034;28248-28253;28271", 
                                                       "11288-11296;21765-21770;21992-21994;28271", 
                                                       "21765-21770", 
                                                       "686-694;11288-11296;21633-21641;28362-28370")),
            "insertions": fake.random_element(elements=(None, "29747:TATT", "22204:GAGCCAGAA", "28332:G")),
            "missing": fake.random_element(elements=(None, "1-54;29837-29903", "1-54;27512-27520;27530-27537;27553-27556;27571-27650;27725-27726;29837-29903", "1-17;29837-29870;29900-29903")),
            "nonACGTNs": fake.random_element(elements=(None, "R:21987;R:24410;Y:27527", "R:21987", "M:22564;K:23401")),
            "pcrPrimerChanges": fake.random_element(elements=(None, 
                                                              "Charit├⌐_RdRp_F:G15451A;ChinaCDC_N_F:G28881T;ChinaCDC_N_R:A28967G", 
                                                              "ChinaCDC_N_F:G28881A;G28882A;G28883C;ChinaCDC_N_R:C28977T", 
                                                              "Charit├⌐_E_F:C26270T;ChinaCDC_N_F:G28881A;G28882A;G28883C;USCDC_N1_P:C28311T")),
            "qc_mixedSites_totalMixedSited": fake.random_element(elements=(None, "0", "1", "2", "3", "7", "11")),
            "qc_overallScore": fake.random_element(elements=(None, "0", "20", "8", "6", "157", "121")),
            "qc_overallStatus": fake.random_element(elements=(None, "good", "mediocre", "bad")),
            "qc_frameShifts_status": None,
            "qc_frameShifts_frameShiftsIgnored": None,
            "NextcladeVersion": fake.random_element(elements=("nextclade 2.5.0", "nextclade 2.6.0", "nextclade 2.4.0")),
            "ConsensusID": consensus_id,
            "IsCurrent": '1',
            "TimestampCreated": str(datetime2.now()),
            "TimestampUpdated": str(datetime2.now())
        }
        NextcladeResult_data.append(record)
    print(f"NextcladeResult data generated {record_amount} times")
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