import pandas as pd
import yfinance as yf

class DataFetcher:
    def __init__(self, ticker: str, start_date: str, end_date: str, frequency: str = '1d'):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.data = None

    def fetch_data(self) -> pd.DataFrame:
        """Récupère les données financières via yfinance"""
        try:
            # Télécharger les données
            self.data = yf.download(
                tickers=self.ticker,
                start=self.start_date,
                end=self.end_date,
                interval=self.frequency,
                auto_adjust=True,
                progress=False
            )

            # Réinitialiser l'index
            self.data.reset_index(inplace=True)

            # Debug: Afficher les premières lignes
            print("\nDEBUG - First rows:")
            print(self.data.head())

            # Nettoyer le DataFrame
            self.data = self.clean_dataframe(self.data)

            return self.data
        except Exception as e:
            raise Exception(f"Failed to fetch data: {str(e)}")

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie le DataFrame pour avoir une structure correcte"""
        # Supprimer les lignes inutiles
        df = df.dropna(how='all')

        # Vérifier si le DataFrame a une structure multi-index
        if isinstance(df.columns, pd.MultiIndex):
            # Aplatir les colonnes
            df.columns = df.columns.droplevel(0)

        # Convertir les types de données
        df['Datetime'] = pd.to_datetime(df['Datetime'])
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
