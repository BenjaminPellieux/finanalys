import matplotlib.pyplot as plt
import pandas as pd

class Visualizer:
    @staticmethod
    def plot_data(data: pd.DataFrame):
        """Affiche les graphiques des données financières"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

        # Cours de clôture et SMA
        ax1.plot(data['Date'], data['Close'], label='Close')
        ax1.plot(data['Date'], data['SMA_20'], label='SMA 20')
        ax1.set_title('Cours et Moyenne Mobile')
        ax1.legend()

        # RSI
        ax2.plot(data['Date'], data['RSI_14'], label='RSI 14')
        ax2.axhline(70, linestyle='--', color='red')
        ax2.axhline(30, linestyle='--', color='green')
        ax2.set_title('RSI 14')

        # MACD
        ax3.plot(data['Date'], data['MACD'], label='MACD')
        ax3.set_title('MACD')

        plt.tight_layout()
        plt.show()

