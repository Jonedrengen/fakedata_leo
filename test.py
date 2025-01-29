from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime
import time
import pandas as pd
from id_generators import GenerateUniquePangolinResultID, GenerateUniqueConsensusID, GenerateUniqueSequencedSampleID, GenerateUniqueNextcladeResultID
from utility import write_to_csv, generate_ncount_value, generate_ambiguoussites, generate_NumbAlignedReads, generate_qc_values, gen_whovariant_datesampling


some_date = gen_whovariant_datesampling(None)
print(some_date)