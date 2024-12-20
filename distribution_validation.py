import pandas as pd
import random
import datetime as datetime1
from datetime import datetime as datetime2, timedelta
from faker import Faker

fake = Faker()

def generate_qc_values(csv_file):
    # Read the CSV file
    qc_possibilities = pd.read_csv(csv_file).dropna()

    # Extract the weights (last column)
    qc_sites_weights = qc_possibilities['counted']

    # Sample a row from the qc_possibilities based on the weights
    sample = qc_possibilities.sample(n=1, weights=qc_sites_weights).iloc[0]

    # Extract the values from the sampled row
    qc_mixedsites_totalmixedsites = int(sample['qc.mixedSites.totalMixedSites'])
    
    #random overall score based on the distribution from real data
    overallstatus = random.choices(['good', 'mediocre', 'bad'],
                                    weights=[0.806, 0.140, 0.038], #weights
                                    k=1)[0] # k=take only 1
    if overallstatus == 'good':
        qc_overallscore = random.randint(0, 29)
    elif overallstatus == 'mediocre':
        qc_overallscore = random.randint(30, 99)
    else:
        qc_overallscore = random.randint(100, 24702)

    return qc_mixedsites_totalmixedsites, qc_overallscore, overallstatus
    

print(generate_qc_values('important_files/qc_mixedsites_possibilities.csv')[0])
two_years_SampleDateSequencing = datetime2.now() - timedelta(days=2*365)
#random_date_SampleDateSequencing = random_date(two_years_SampleDateSequencing, datetime2.now())

Faker.seed(0)
for _ in range(5):
    print(fake.date_between())

