import requests
import pandas as pd
from datetime import datetime

class DataFetcher:
    def __init__(self, ticker: str, start_date: str, end_date: str):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def fetch_data(self) -> pd.DataFrame:
        """Récupère les données financières via l'API Yahoo Finance"""
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{self.ticker}?period1={int(datetime.strptime(self.start_date, '%Y-%m-%d').timestamp())}&period2={int(datetime.strptime(self.end_date, '%Y-%m-%d').timestamp())}&interval=1d&events=history&includeAdjustedClose=true"
        response = requests.get(url)
        if response.status_code == 200:
            self.data = pd.read_csv(io.StringIO(response.text))
            return self.data
        raise Exception(f"Failed to fetch data: {response.status_code}")

    def get_data(self) -> pd.DataFrame:
        """Retourne les données récupérées"""
        return self.data

