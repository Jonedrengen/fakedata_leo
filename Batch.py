from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv

fake = Faker()

#BatchID is primary key
Batch_headers = ["BatchID", "BatchDate", "Platform", "BatchSource", "TimestampCreated", "TimestampUpdated"]



def BatchData(record_amount):
    Batch_data = []
    for i in range(record_amount):
        record = {
            "BatchID": fake.uuid4(),
            "BatchDate": fake.date(),
            "Platform": fake.random_element(elements=('labA','labB','labC')),
            "BatchSource": fake.company(),
            "TimestampCreated": fake.date_time_this_year(),
            "TimestampCreated": fake.date_time_this_year(),
            
        }

    