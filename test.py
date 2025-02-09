from utility import generate_exclusion_values, gen_whovariant_datesampling, generate_BatchSource
import pandas as pd
from datetime import datetime as datetime, timedelta
from faker import Faker

fake = Faker()

Variant_connections = pd.read_csv('important_files/Nextclade_pango_essentials.csv', na_values=["NULL"])
Variant_connections_weights = Variant_connections.iloc[:, -1].tolist()

#Batchsource
BatchSource = generate_BatchSource("Alpha", "2021-04-26")
print(BatchSource)