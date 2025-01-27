import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_date_sampling_distribution(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    df_clean = df[df['DateSampling'].notna()]

    # Extract LineagesOfInterest and DateSampling
    df_clean['LineagesOfInterest'] = df_clean['DateSampling'].apply(lambda x: x.split(':')[0])
    df_clean['DateSampling'] = pd.to_datetime(df_clean['DateSampling'].apply(lambda x: x.split(': ')[1]))
    
        

    # Plot the distribution
    plt.figure(figsize=(12, 6))
    for lineage in df_clean['LineagesOfInterest'].unique():
        subset = df_clean[df_clean['LineagesOfInterest'] == lineage]
        plt.hist(subset['DateSampling'], bins=30, alpha=0.5, label=lineage)

    plt.xlabel('DateSampling')
    plt.ylabel('Frequency')
    plt.title('Distribution of DateSampling by LineagesOfInterest')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    csv_file = 'Sample_data.csv'
    plot_date_sampling_distribution(csv_file) 