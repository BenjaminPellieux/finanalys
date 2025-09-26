import pandas as pd
import yfinance as yf

class DataFetcher:
    def __init__(self, ticker: str, start_date: str, end_date: str, period: str = '5d', interval: str = '2m'):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.period = period
        self.data = None

    def fetch_data(self) -> pd.DataFrame:
        """Récupère les données financières via yfinance"""
        try:
            
            self.data = yf.download(
                tickers=self.ticker,
                period=self.period,
                interval=self.interval,
                multi_level_index=False
            )

            self.data.reset_index(inplace=True)

            self.data = self.clean_dataframe(self.data)

            return self.data
        except Exception as e:
            raise Exception(f"Failed to fetch data: {str(e)}")

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie le DataFrame pour avoir une structure correcte"""
        #print(f"DEBUG {df.head()=}")
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except:
            try:
                df['Date'] = pd.to_datetime(df['Datetime'])
            except:
                print("ERROR")

        numeric_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Supprimer les lignes avec des valeurs manquantes
        df = df.dropna(subset=numeric_cols)

        return df

    def get_data(self) -> pd.DataFrame:
        """Retourne les données récupérées"""
        return self.data
