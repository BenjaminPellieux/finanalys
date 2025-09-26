#exporter
import pandas as pd

class Exporter:
    @staticmethod
    def to_csv(data: pd.DataFrame, filename: str):
        """Exporte les données vers un fichier CSV"""
        try:
            data.to_csv(filename, index=False)
        except Exception as e:
            raise Exception(f"Error exporting to CSV: {str(e)}")
