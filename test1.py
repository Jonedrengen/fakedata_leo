from faker import Faker
from faker.providers import BaseProvider #custom providers
import random
import csv

fake = Faker()

#desired file headers using *args
def DesiredHeaders(*headers):
    return list(headers)

def RandomName(amount):
    list = []
    for i in range(amount):
        print(fake.name())
        list.append(fake.name())
    return list

data = RandomName(25)
print(type(data))
