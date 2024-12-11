import pandas as pd
import random

# Read the CSV file
dataframe = pd.read_csv('important_files/qc_mixedsites_possibilities.csv').dropna()



#print(qc_mixedsites_totalmixedsites['qc.mixedSites.totalMixedSites'].tolist())

qc_sites_weights = dataframe['counted']

sample = dataframe.sample(n=1, weights=qc_sites_weights).iloc[0]
print(sample)

qc_mixedsites_totalmixedsites = sample['qc.mixedSites.totalMixedSites']
print(qc_mixedsites_totalmixedsites)
qc_overallscore = random.randint(int(sample['Min_score']),int(sample['Max_score']))
print(qc_overallscore)