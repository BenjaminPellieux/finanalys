import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter

class Visualizer:
    @staticmethod
    def plot_data(data: pd.DataFrame):
        """Affiche les graphiques des données financières"""
    
        # fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Convertir la colonne Date en datetime
        data['Date'] = pd.to_datetime(data['Date'])

        # Cours de clôture et SMA
        ax1.plot(data['Date'], data['Close'], label='Close')
        ax1.plot(data['Date'], data['SMA_20'], label='SMA 20')
        ax1.set_title('Cours et Moyenne Mobile')
        ax1.legend()
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        # RSI
        ax2.plot(data['Date'], data['RSI_14'], label='RSI 14')
        ax2.axhline(70, linestyle='--', color='red')
        ax2.axhline(30, linestyle='--', color='green')
        ax2.set_title('RSI 14')
        ax2.legend()
        ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        # MACD
        # ax3.plot(data['Date'], data['MACD'], label='MACD')
        # ax3.set_title('MACD')
        # ax3.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        plt.tight_layout()
        plt.show()
        