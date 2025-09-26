from finance_plugin import DataFetcher, DataProcessor, Visualizer, Exporter

# Configuration
TICKER = 'ETL.PA'
START_DATE = '2025-09-01'
END_DATE = '2025-09-26'
OUTPUT_CSV = 'processed_data.csv'

# try:
# 1. Récupération des données
print("Fetching data...")
fetcher = DataFetcher(TICKER, START_DATE, END_DATE)
data = fetcher.fetch_data()
print(f"\nData fetched successfully. {len(data)} records found.")
print("Data sample:")
print(data.head())

# 2. Traitement des données
print("\nProcessing data...")
processor = DataProcessor(data)
processed_data = processor.calculate_indicators()

# 3. Visualisation
print("\nGenerating plots...")
Visualizer.plot_data(processed_data)

# 4. Export CSV
print(f"\nExporting data to {OUTPUT_CSV}...")
Exporter.to_csv(processed_data, OUTPUT_CSV)
print("Data exported successfully!")

# except Exception as e:
#     print(f"\nAn error occurred: {str(e)}")
