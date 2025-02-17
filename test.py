from utility_V2 import generate_exclusion_values, gen_whovariant_datesampling, generate_BatchSource
import pandas as pd
from datetime import datetime as datetime, timedelta
from faker import Faker

reference_data = pd.read_csv('important_files/Complete_reference_data.csv', na_values=["NULL"])
initial_row = reference_data.sample(n=1, weights=reference_data['weight']).iloc[0]
BatchDate_unfixed = gen_whovariant_datesampling(initial_row['LineagesOfInterest'], reference_data)
batch = generate_BatchSource('Alpha', datetime(2021, 2, 15), reference_data)
print(batch)