import csv
import pandas
from test1 import RandomName

data = RandomName(25)
print(type(data))

def nameCSV(data_list, file_path):
    with open(file_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["random names", "not so random here"])
        for name in data_list:
            writer.writerow([name])

nameCSV(data, "random_names.csv")
