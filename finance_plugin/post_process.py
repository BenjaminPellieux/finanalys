"""
Module de post-traitement des données financières.

Ce module contient des classes pour la visualisation graphique et l'export des données
financières analysées. Il permet de générer des graphiques techniques professionnels
et d'exporter les résultats vers différents formats.

Classes:
    Visualizer: Classe pour la visualisation graphique des indicateurs techniques
    Exporter: Classe pour l'export des données vers différents formats
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from typing import Optional

class Visualizer:
    """
    Classe de visualisation des données financières et des indicateurs techniques.

    Cette classe fournit des méthodes pour générer des graphiques professionnels
    des principaux indicateurs techniques (SMA, RSI, MACD) avec une mise en forme
    adaptée à l'analyse financière.

    Methods:
        plot_data: Génère une visualisation complète des indicateurs techniques
    """

    @staticmethod
    def plot_data(name: str, data: pd.DataFrame, title: Optional[str] = None) -> None:
        """
        Génère une visualisation complète des indicateurs techniques.

        Cette méthode crée un graphique à trois niveaux montrant:
        1. Les cours de clôture avec la moyenne mobile simple (SMA)
        2. Le Relative Strength Index (RSI)
        3. Le Moving Average Convergence Divergence (MACD)

        Args:
            name: Nom de l'actif financier (ex: 'ETL.PA')
            data: DataFrame contenant les données financières et les indicateurs calculés
            title: Titre personnalisé pour le graphique (optionnel)

        Raises:
            ValueError: Si les données nécessaires sont manquantes
            Exception: En cas d'erreur de traçage

        Example:
            >>> Visualizer.plot_data('ETL.PA', processed_data)
        """
        # Validation des données d'entrée
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame")

        required_columns = ['Date', 'Close', 'SMA_20', 'RSI_14', 'MACD']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"DataFrame must contain '{col}' column")

        try:
            # Convertir la colonne Date en datetime si nécessaire
            if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                data['Date'] = pd.to_datetime(data['Date'])

            # Créer la figure et les sous-graphiques
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

            # Configuration commune aux trois graphiques
            date_formatter = DateFormatter('%Y-%m-%d')
            for ax in [ax1, ax2, ax3]:
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.xaxis.set_major_formatter(date_formatter)

            # Graphique 1: Cours de clôture et SMA
            ax1.plot(data['Date'], data['Close'], label='Close', color='#1f77b4', alpha=0.7)
            ax1.plot(data['Date'], data['SMA_20'], label='SMA 20', color='#ff7f0e', linewidth=1.5)
            ax1.set_title('Cours et Moyenne Mobile Simple (SMA 20)')
            ax1.set_ylabel('Prix')
            ax1.legend(loc='upper left')

            # Graphique 2: RSI
            ax2.plot(data['Date'], data['RSI_14'], label='RSI 14', color='#9467bd')
            ax2.axhline(70, linestyle='--', color='red', alpha=0.5, label='Surachat')
            ax2.axhline(30, linestyle='--', color='green', alpha=0.5, label='Survente')
            ax2.set_title('Relative Strength Index (RSI 14)')
            ax2.set_ylabel('RSI')
            ax2.legend(loc='upper left')

            # Graphique 3: MACD
            ax3.plot(data['Date'], data['MACD'], label='MACD', color='#2ca02c')
            ax3.set_title('Moving Average Convergence Divergence (MACD)')
            ax3.set_ylabel('MACD')
            ax3.legend(loc='upper left')

            # Titre principal
            if title:
                fig.suptitle(title, fontsize=16, y=1.02)
            else:
                fig.suptitle(f'Analyse technique - {name}', fontsize=16, y=1.02)

            # Ajuster la disposition et afficher
            plt.tight_layout()
            plt.show()

        except Exception as e:
            raise Exception(f"Error plotting data: {str(e)}")

class Exporter:
    """
    Classe pour l'export des données financières vers différents formats.

    Cette classe fournit des méthodes pour exporter les données traitées vers
    des fichiers dans différents formats (CSV, Excel, etc.) avec des options
    de configuration.

    Methods:
        to_csv: Exporte les données vers un fichier CSV
    """

    @staticmethod
    def to_csv(data: pd.DataFrame, filename: str, **kwargs) -> None:
        """
        Exporte les données vers un fichier CSV.

        Args:
            data: DataFrame contenant les données à exporter
            filename: Chemin du fichier de destination
            kwargs: Arguments supplémentaires pour pandas.to_csv()

        Raises:
            ValueError: Si les données ou le nom de fichier sont invalides
            Exception: En cas d'erreur d'export

        Example:
            >>> Exporter.to_csv(processed_data, 'financial_analysis.csv')
        """
        # Validation des entrées
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame")

        if not filename or not isinstance(filename, str):
            raise ValueError("Filename must be a non-empty string")

        # Options par défaut pour l'export
        default_kwargs = {
            'index': False,
            'encoding': 'utf-8',
            'date_format': '%Y-%m-%d'
        }

        # Fusionner avec les options personnalisées
        export_kwargs = {**default_kwargs, **kwargs}

        try:
            data.to_csv(filename, **export_kwargs)
        except Exception as e:
            raise Exception(f"Error exporting to CSV: {str(e)}")

    @staticmethod
    def to_excel(data: pd.DataFrame, filename: str, **kwargs) -> None:
        """
        Exporte les données vers un fichier Excel.

        Args:
            data: DataFrame contenant les données à exporter
            filename: Chemin du fichier de destination (doit se terminer par .xlsx)
            kwargs: Arguments supplémentaires pour pandas.to_excel()

        Raises:
            ValueError: Si le nom de fichier n'est pas valide
            Exception: En cas d'erreur d'export

        Example:
            >>> Exporter.to_excel(processed_data, 'financial_analysis.xlsx')
        """
        if not filename.endswith('.xlsx'):
            raise ValueError("Filename must end with .xlsx for Excel export")

        try:
            data.to_excel(filename, index=False, **kwargs)
        except Exception as e:
            raise Exception(f"Error exporting to Excel: {str(e)}")
