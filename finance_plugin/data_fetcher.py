"""
Module de récupération de données financières utilisant l'API Yahoo Finance.

Ce module permet de télécharger des données boursières historiques et en temps réel
pour un actif financier donné, avec des fonctionnalités de nettoyage et de préparation
des données pour l'analyse technique.

Classes:
    DataFetcher: Classe principale pour la récupération et le nettoyage des données financières
"""

import pandas as pd
import yfinance as yf

class DataFetcher:
    """
    Récupère et nettoie les données financières depuis Yahoo Finance.

    Cette classe permet de télécharger des données boursières (cours, volumes, etc.)
    pour un actif financier donné, sur une période et un intervalle de temps spécifiés.

    Attributes:
        ticker (str): Symbole de l'actif financier (ex: 'AAPL' pour Apple)
        start_date (str): Date de début au format 'YYYY-MM-DD'
        end_date (str): Date de fin au format 'YYYY-MM-DD'
        interval (str): Intervalle de temps entre les points de données ('1m', '2m', '5m', '15m',
                       '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        period (str): Période de temps ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        data (pd.DataFrame): DataFrame contenant les données financières nettoyées
    """

    def __init__(self, ticker: str, start_date: str, end_date: str, period: str = '5d', interval: str = '2m'):
        """
        Initialise le DataFetcher avec les paramètres de récupération.

        Args:
            ticker: Symbole de l'actif financier
            start_date: Date de début au format 'YYYY-MM-DD'
            end_date: Date de fin au format 'YYYY-MM-DD'
            period: Période de temps (par défaut '5d')
            interval: Intervalle de temps entre les points de données (par défaut '2m')
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.period = period
        self.data = None

    def fetch_data(self) -> pd.DataFrame:
        """
        Récupère les données financières via l'API Yahoo Finance.

        Returns:
            pd.DataFrame: DataFrame contenant les données financières nettoyées

        Raises:
            Exception: En cas d'échec de la récupération des données
        """
        try:
            # Télécharger les données via l'API yfinance
            self.data = yf.download(
                tickers=self.ticker,
                start=self.start_date,
                end=self.end_date,
                interval=self.interval,
                progress=False
            )

            # Réinitialiser l'index pour avoir une colonne 'Date' classique
            self.data.reset_index(inplace=True)

            # Nettoyer et formater les données
            self.data = self.clean_dataframe(self.data)

            return self.data
        except Exception as e:
            raise Exception(f"Failed to fetch data: {str(e)}")

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoie et formate le DataFrame pour une utilisation optimale.

        Cette méthode:
        1. Convertit la colonne de date en datetime
        2. Convertit les colonnes numériques au bon format
        3. Supprime les lignes avec des valeurs manquantes

        Args:
            df: DataFrame brut à nettoyer

        Returns:
            pd.DataFrame: DataFrame nettoyé et formaté

        Note:
            Gère automatiquement les différentes structures de colonnes possibles
            retournées par l'API Yahoo Finance.
        """
        # Essayer différentes colonnes de date possibles
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except KeyError:
            try:
                df['Date'] = pd.to_datetime(df['Datetime'])
            except KeyError:
                raise ValueError("DataFrame doesn't contain valid date column")

        numeric_cols = ['Close', 'High', 'Low', 'Open', 'Volume']

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.dropna(subset=numeric_cols)

        return df

    def get_data(self) -> pd.DataFrame:
        """
        Retourne les données financières récupérées et nettoyées.

        Returns:
            pd.DataFrame: DataFrame contenant les données financières

        Raises:
            ValueError: Si aucune donnée n'a été récupérée
        """
        if self.data is None:
            raise ValueError("No data has been fetched. Call fetch_data() first.")
        return self.data
