from faker import Faker
import datetime

fake = Faker()

print(fake.date_between(datetime.date(2020, 10, 1), datetime.date(2022, 9, 1)))