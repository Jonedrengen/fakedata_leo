from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime

fake = Faker()


NextcladeResult_headers = ["NextcladeResultID", "frameShifts", "aaSubstitutions", "aaDeletions", "aaInsertions", "alignmentScore", 
                           "clade", "Nextclade_pango", "substitutions", "deletions", "insertions", "missing", "nonACGTNs", 
                           "pcrPrimerChanges", "qc_mixedSites_totalMixedSited", "qc_overallScore", "qc_overallStatus", "qc_frameShifts_status", 
                           "qc_frameShifts_frameShiftsIgnored", "NextcladeVersion", "ConsensusID", "IsCurrent", "TimestampCreated", "TimestampUpdated"]

def NextcladeResult(record_amount):
    NextcladeResult_data = []
    for i in range(record_amount):
        record = {
            
        }
