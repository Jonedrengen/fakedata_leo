from utility import generate_exclusion_values, gen_whovariant_datesampling, generate_BatchSource
import pandas as pd
from datetime import datetime as datetime, timedelta
from faker import Faker

fake = Faker()




IsCurrent_test = pd.read_csv('output/PangolinResult_data.csv')
IsCurrent_test2 = pd.read_csv('output/Consensus_data.csv')
IsCurrent_test3 = pd.read_csv('PangolinResult_data.csv')
print(type(IsCurrent_test['IsCurrent'][0]))
print(type(IsCurrent_test2['IsCurrent'][0]))
print(type(IsCurrent_test3['IsCurrent'][0]))
