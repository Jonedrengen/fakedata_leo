import matplotlib.pyplot as plt
from utility import gen_whovariant_samplingdate
# Generate a large number of dates
dates = [gen_whovariant_samplingdate() for _ in range(10000)]

# Plot the distribution
plt.hist([date.strftime("%Y-%m-%d") for date in dates], bins=100, alpha=0.75)
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.title('Distribution of Generated Dates')
plt.xticks(rotation=45)
plt.show()