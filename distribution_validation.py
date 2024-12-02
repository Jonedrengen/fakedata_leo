# import pandas lib as pd
import pandas as pd

# read by default 1st sheet of an excel file
dataframe1 = pd.read_excel('version.xlsx').dropna()

#print(dataframe1)

sample = str(dataframe1['version'].sample().values[0])

print(type(sample))

print(str(sample))
