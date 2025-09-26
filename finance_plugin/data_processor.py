import pandas as pd
import talib  # Bibliothèque pour indicateurs techniques

class DataProcessor:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def calculate_indicators(self) -> pd.DataFrame:
        """Calcule les indicateurs techniques"""
        self.data['SMA_20'] = talib.SMA(self.data['Close'], timeperiod=20)
        self.data['RSI_14'] = talib.RSI(self.data['Close'], timeperiod=14)
        self.data['MACD'], _, _ = talib.MACD(self.data['Close'])
        return self.data

    def get_processed_data(self) -> pd.DataFrame:
        """Retourne les données traitées"""
        return self.data

