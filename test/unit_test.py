import unittest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from finance_plugin import DataFetcher, DataProcessor, Visualizer, Exporter
import os
import tempfile

class TestDataFetcher(unittest.TestCase):
    """Tests unitaires pour la classe DataFetcher"""

    @patch('yfinance.download')
    def test_fetch_data_success(self, mock_download):
        """Test le téléchargement réussi des données"""
        # Configuration du mock
        mock_data = pd.DataFrame({
            'Date': [datetime(2025, 9, 1), datetime(2025, 9, 2)],
            'Close': [100, 101],
            'High': [101, 102],
            'Low': [99, 100],
            'Open': [99, 100],
            'Volume': [1000, 1500]
        })
        mock_download.return_value = mock_data

        # Test
        fetcher = DataFetcher('ETL.PA', '2025-09-01', '2025-09-02')
        result = fetcher.fetch_data()

        # Vérifications
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn('Close', result.columns)
        mock_download.assert_called_once()

    @patch('yfinance.download')
    def test_fetch_data_failure(self, mock_download):
        """Test l'échec du téléchargement des données"""
        mock_download.side_effect = Exception("API Error")

        with self.assertRaises(Exception) as context:
            fetcher = DataFetcher('ETL.PA', '2025-09-01', '2025-09-02')
            fetcher.fetch_data()

        self.assertIn("Failed to fetch data", str(context.exception))

    def test_clean_dataframe(self):
        """Test le nettoyage du DataFrame"""
        fetcher = DataFetcher('ETL.PA', '2025-09-01', '2025-09-02')
        
        # Test avec différentes structures de colonnes
        test_cases = [
            # Cas 1: Structure standard
            pd.DataFrame({
                'Date': ['2025-09-01', '2025-09-02'],
                'Close': [100, 101]
            }),
            # Cas 2: Avec colonne Datetime
            pd.DataFrame({
                'Datetime': ['2025-09-01', '2025-09-02'],
                'Close': [100, 101]
            }),
            # Cas 3: Avec valeurs manquantes
            pd.DataFrame({
                'Date': ['2025-09-01', '2025-09-02'],
                'Close': [100, None]
            })
        ]

        for test_data in test_cases:
            cleaned = fetcher.clean_dataframe(test_data.copy())
            self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned['Date']))

    def test_get_data_before_fetch(self):
        """Test l'accès aux données avant le téléchargement"""
        fetcher = DataFetcher('ETL.PA', '2025-09-01', '2025-09-02')
        with self.assertRaises(ValueError):
            fetcher.get_data()

class TestDataProcessor(unittest.TestCase):
    """Tests unitaires pour la classe DataProcessor"""

    def setUp(self):
        """Préparation des données de test"""
        self.valid_data = pd.DataFrame({
            'Date': pd.date_range('2025-09-01', periods=30),
            'Close': list(range(30, 60))
        })

    def test_calculate_indicators_success(self):
        """Test le calcul réussi des indicateurs"""
        processor = DataProcessor(self.valid_data)
        result = processor.calculate_indicators()

        self.assertIn('SMA_20', result.columns)
        self.assertIn('RSI_14', result.columns)
        self.assertIn('MACD', result.columns)
        self.assertIn('MACD_Signal', result.columns)
        self.assertIn('MACD_Hist', result.columns)

    def test_calculate_indicators_insufficient_data(self):
        """Test avec données insuffisantes"""
        short_data = pd.DataFrame({
            'Date': pd.date_range('2025-09-01', periods=10),
            'Close': list(range(10))
        })

        with self.assertRaises(ValueError) as context:
            processor = DataProcessor(short_data)
            processor.calculate_indicators()

        self.assertIn("Not enough data points", str(context.exception))

    def test_calculate_indicators_missing_close(self):
        """Test avec colonne Close manquante"""
        invalid_data = pd.DataFrame({
            'Date': pd.date_range('2025-09-01', periods=30),
            'Open': list(range(30))
        })

        with self.assertRaises(ValueError) as context:
            processor = DataProcessor(invalid_data)
            processor.calculate_indicators()

        self.assertIn("must contain a 'Close' column", str(context.exception))

    def test_calculate_indicators_invalid_input(self):
        """Test avec entrée invalide"""
        with self.assertRaises(ValueError):
            processor = DataProcessor("not a dataframe")
            processor.calculate_indicators()

class TestVisualizer(unittest.TestCase):
    """Tests unitaires pour la classe Visualizer"""

    def setUp(self):
        """Préparation des données de test"""
        self.test_data = pd.DataFrame({
            'Date': pd.date_range('2025-09-01', periods=30),
            'Close': list(range(30, 60)),
            'SMA_20': [None]*19 + list(range(49, 60)),
            'RSI_14': [None]*13 + [50]*17,
            'MACD': [0]*30
        })

    @patch('matplotlib.pyplot.show')
    def test_plot_data_success(self, mock_show):
        """Test la visualisation réussie"""
        Visualizer.plot_data('ETL.PA', self.test_data)
        mock_show.assert_called_once()

    def test_plot_data_missing_columns(self):
        """Test avec colonnes manquantes"""
        incomplete_data = pd.DataFrame({
            'Date': pd.date_range('2025-09-01', periods=30),
            'Close': list(range(30, 60))
        })

        with self.assertRaises(ValueError):
            Visualizer.plot_data('ETL.PA', incomplete_data)

    def test_plot_data_invalid_input(self):
        """Test avec entrée invalide"""
        with self.assertRaises(ValueError):
            Visualizer.plot_data('ETL.PA', "not a dataframe")

class TestExporter(unittest.TestCase):
    """Tests unitaires pour la classe Exporter"""

    def setUp(self):
        """Préparation des données de test"""
        self.test_data = pd.DataFrame({
            'Date': pd.date_range('2025-09-01', periods=5),
            'Close': list(range(5))
        })

    def test_to_csv_success(self):
        """Test l'export réussi vers CSV"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            try:
                Exporter.to_csv(self.test_data, tmp.name)
                self.assertTrue(os.path.exists(tmp.name))
                # Vérifier que le fichier n'est pas vide
                self.assertGreater(os.path.getsize(tmp.name), 0)
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

    def test_to_csv_failure(self):
        """Test l'échec de l'export CSV"""
        with self.assertRaises(Exception):
            Exporter.to_csv(self.test_data, '/invalid/path/file.csv')

    def test_to_excel_success(self):
        """Test l'export réussi vers Excel"""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            try:
                Exporter.to_excel(self.test_data, tmp.name)
                self.assertTrue(os.path.exists(tmp.name))
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

    def test_to_excel_invalid_extension(self):
        """Test avec extension de fichier invalide"""
        with self.assertRaises(ValueError):
            Exporter.to_excel(self.test_data, 'file.csv')

if __name__ == '__main__':
    unittest.main()
