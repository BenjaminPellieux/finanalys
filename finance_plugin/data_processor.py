"""
Module de traitement des données financières.

Ce module calcule des indicateurs techniques standardisés utilisés en analyse boursière,
y compris les moyennes mobiles, le RSI et le MACD.

Classes:
    DataProcessor: Classe principale pour le calcul des indicateurs techniques
"""

import pandas as pd
import talib

class DataProcessor:
    """
    Calcule des indicateurs techniques sur des données financières.

    Cette classe applique des calculs techniques standardisés sur des séries de prix
    pour aider à l'analyse des tendances et à la prise de décision.

    Attributes:
        data (pd.DataFrame): DataFrame contenant les données financières brutes
        processed_data (pd.DataFrame): DataFrame contenant les données avec indicateurs calculés
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialise le DataProcessor avec les données financières.

        Args:
            data: DataFrame contenant les données financières (doit inclure une colonne 'Close')
        """
        self.data = data
        self.processed_data = None

    def calculate_indicators(self) -> pd.DataFrame:
        """
        Calcule les indicateurs techniques standard sur les données financières.

        Les indicateurs calculés sont:
        - SMA 20: Moyenne mobile simple sur 20 périodes
        - RSI 14: Relative Strength Index sur 14 périodes
        - MACD: Moving Average Convergence Divergence

        Returns:
            pd.DataFrame: DataFrame avec les indicateurs techniques ajoutés

        Raises:
            ValueError: Si les données ne sont pas valides ou insuffisantes
        """
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")

        if 'Close' not in self.data.columns:
            raise ValueError("DataFrame must contain a 'Close' column")

        self.data = self.data.copy()

        self.data['Close'] = pd.to_numeric(self.data['Close'], errors='coerce')

        self.data = self.data.dropna(subset=['Close'])

        if len(self.data) < 20:
            raise ValueError("Not enough data points to calculate indicators")

        close_prices = self.data['Close'].values.astype('float64')

        self.data['SMA_20'] = talib.SMA(close_prices, timeperiod=20)

        self.data['RSI_14'] = talib.RSI(close_prices, timeperiod=14)

        macd, macd_signal, macd_hist = talib.MACD(close_prices)

        self.data['MACD'] = macd
        self.data['MACD_Signal'] = macd_signal
        self.data['MACD_Hist'] = macd_hist

        self.processed_data = self.data

        return self.processed_data
