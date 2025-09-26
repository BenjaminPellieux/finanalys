import pandas as pd
import talib
import numpy as np

class DataProcessor:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.processed_data = None

    def calculate_indicators(self) -> pd.DataFrame:
        """Calcule les indicateurs techniques"""
        try:
            # Vérification et préparation des données
            if not isinstance(self.data, pd.DataFrame):
                raise ValueError("Input data must be a pandas DataFrame")

            # Vérifier que la colonne 'Close' existe
            if 'Close' not in self.data.columns:
                raise ValueError("DataFrame must contain a 'Close' column")

            # Créer une copie pour éviter les avertissements
            self.data = self.data.copy()

            # Convertir les valeurs en numérique
            self.data['Close'] = pd.to_numeric(self.data['Close'], errors='coerce')

            # Supprimer les lignes avec des valeurs manquantes
            self.data = self.data.dropna(subset=['Close'])

            # Vérifier qu'il y a assez de données
            if len(self.data) < 20:
                raise ValueError("Not enough data points to calculate indicators")

            # Calcul des indicateurs
            close_prices = self.data['Close'].values.astype('float64')

            # SMA 20
            self.data['SMA_20'] = talib.SMA(close_prices, timeperiod=20)

            # RSI 14
            self.data['RSI_14'] = talib.RSI(close_prices, timeperiod=14)

            # MACD
            macd, macd_signal, macd_hist = talib.MACD(close_prices)
            self.data['MACD'] = macd
            self.data['MACD_Signal'] = macd_signal
            self.data['MACD_Hist'] = macd_hist

            self.processed_data = self.data
            return self.processed_data
        except Exception as e:
            raise Exception(f"Error processing data: {str(e)}")
