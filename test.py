from utility import generate_exclusion_values, gen_whovariant_datesampling, generate_BatchSource
import pandas as pd
from datetime import datetime as datetime, timedelta
from faker import Faker

fake = Faker()

start_date = '2021-05-05'

#convert strings to dates
start_date = datetime.strptime(start_date, "%Y-%m-%d")
#end_date = datetime.strptime(end_date, "%Y-%m-%d")

days_between = start_date + timedelta(days=2)
print(days_between)

random_date = fake.date_between(start_date, end_date=days_between)
print(random_date)
