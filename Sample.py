from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv
from datetime import datetime

fake = Faker()


Sample_headers = ["SampleID", "SampleDateTime", "Host", "Ct", "DateSampling", "CurrentConsensusID", "TimestampCreated", "TimestampUpdated"]


def SampleData(record_amount):
    Sample_data = []
    for i in range(record_amount):
        record = {
            "SampleID": fake.random_element(elements=("someID","someotherID")) + str(random.randint(0, 999999999)).zfill(9),
            "SampleDateTime": fake.date(),
            "Host": fake.random_element(elements=("HostA", "HostB", "HostC")),
            "Ct": fake.random_element(elements=("CtA", "CtB", "CtC")),
            "DateSampling": fake.random_element(elements=("DateSamplingX", "DateSamplingY", "DateSamplingZ")),
            "CurrentConsensusID": fake.random_element(elements=("anID", "anotherID", "thirdID")),
            "TimestampCreated": str(datetime.now()),
            "TimestampUpdated": str(datetime.now())
        }
        Sample_data.append(record)
    print(f"Sample data generated {record_amount} times")
    return Sample_data

def write_to_csv(file_name, data, headers):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"written to {file_name}")

if __name__ == "__main__":

    sample_data = SampleData(1000)

    write_to_csv('Sample_data.csv', sample_data, Sample_headers)