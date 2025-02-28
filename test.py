from utility import generate_exclusion_values, gen_whovariant_datesampling, generate_BatchSource, generate_ambiguoussites, generate_ncount_value
import pandas as pd
from datetime import datetime as datetime, timedelta
from faker import Faker

somevalue = generate_ncount_value()
print(somevalue)
print(type(somevalue))

for i in range(10000):
    ncount = generate_ncount_value()
    amb = generate_ambiguoussites()
    print(ncount + amb)
        