import pandas as pd

class Exporter:
    @staticmethod
    def to_csv(data: pd.DataFrame, filename: str):
        """Exporte les données vers un fichier CSV"""
        data.to_csv(filename, index=False)

