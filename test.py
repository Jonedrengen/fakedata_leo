import pandas as pd
import matplotlib.pyplot as plt

def plot_date_sampling_distribution(csv_file, essentials_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    essentials = pd.read_csv(essentials_file)

    # Ensure DateSampling is in datetime format
    df['DateSampling'] = pd.to_datetime(df['DateSampling'])

    # Merge with essentials to get LineagesOfInterest
    df = df.merge(essentials[['DateSampling', 'LineagesOfInterest']], on='DateSampling', how='left')

    # Plot the distribution
    plt.figure(figsize=(12, 6))
    for lineage in df['LineagesOfInterest'].unique():
        subset = df[df['LineagesOfInterest'] == lineage]
        plt.hist(subset['DateSampling'], bins=30, alpha=0.5, label=lineage)

    plt.xlabel('DateSampling')
    plt.ylabel('Frequency')
    plt.title('Distribution of DateSampling by LineagesOfInterest')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    csv_file = 'Sample_data.csv'
    essentials_file = 'important_files/Nextclade_pango_essentials.csv'
    plot_date_sampling_distribution(csv_file, essentials_file)