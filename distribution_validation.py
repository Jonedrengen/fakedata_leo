import matplotlib.pyplot as plt
from utility import generate_pctcoveredbases
import numpy as np
import scipy.stats as stats

# Generate synthetic data
generated_data = [generate_pctcoveredbases() for _ in range(100000)]

# Summary statistics
print("Generated Data Summary:")
print(f"Min: {min(generated_data)}")
print(f"1st Quartile: {np.percentile(generated_data, 25)}")
print(f"Median: {np.median(generated_data)}")
print(f"Mean: {np.mean(generated_data)}")
print(f"3rd Quartile: {np.percentile(generated_data, 75)}")
print(f"Max: {max(generated_data)}")

# Plot histogram
plt.hist(generated_data, bins=50, color='gray', alpha=0.7)
plt.title("Histogram of Generated Left-Skewed Data")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# Q-Q plot to check if the data follows the expected distribution
stats.probplot(generated_data, dist="beta", sparams=(alpha, beta), plot=plt)
plt.title("Q-Q Plot of Generated Data")
plt.show()