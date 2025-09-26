import pandas as pd
import talib

class DataProcessor:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.processed_data = None

    def calculate_indicators(self) -> pd.DataFrame:
        """Calcule les indicateurs techniques"""
    
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")

        if 'Close' not in self.data.columns:
            raise ValueError("DataFrame must contain a 'Close' column")

        self.data = self.data.copy()
        self.data['Close'] = pd.to_numeric(self.data['Close'], errors='coerce')
        self.data = self.data.dropna(subset=['Close'])

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

