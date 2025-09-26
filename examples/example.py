from finance_plugin import DataFetcher, DataProcessor, Visualizer, Exporter

# 1. Récupération des données
fetcher = DataFetcher('AAPL', '2023-01-01', '2023-12-31')
data = fetcher.fetch_data()

# 2. Traitement des données
processor = DataProcessor(data)
processed_data = processor.calculate_indicators()

# 3. Visualisation
Visualizer.plot_data(processed_data)

# 4. Export CSV
Exporter.to_csv(processed_data, 'apple_stock_data.csv')

