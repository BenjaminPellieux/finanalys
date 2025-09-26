# Finance Analysis Toolkit

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

Un outil complet pour l'analyse technique des marchés financiers utilisant les indicateurs SMA, RSI et MACD.


# AI USAGE

Pour ce projet, le LLM de MistralAI "le chat" a été utilisé pour la génération des tests unitaires & de la documentation.
[Le-chat](https://mistral.ai/fr/products/le-chat)
**MistralAI >>>>> OpenAI**

## Description

Ce projet fournit une solution complète pour :
- Récupérer des données financières via l'API Yahoo Finance
- Calculer des indicateurs techniques standardisés (SMA, RSI, MACD)
- Visualiser les données avec des graphiques professionnels
- Exporter les résultats vers différents formats

## Fonctionnalités

### 1. Récupération des données
- Téléchargement des données financières via Yahoo Finance
- Support des différents intervalles (minute, horaire, quotidien)
- Nettoyage et formatage automatique des données

### 2. Analyse technique
- Calcul de la Moyenne Mobile Simple (SMA 20)
- Calcul du Relative Strength Index (RSI 14)
- Calcul du Moving Average Convergence Divergence (MACD)

### 3. Visualisation
- Graphiques interactifs des indicateurs techniques
- Mise en forme professionnelle des graphiques
- Affichage des zones de surachat/survente

### 4. Export des données
- Export vers CSV
- Export vers Excel
- Options de configuration avancées

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Dépendances
```bash
pip install pandas yfinance matplotlib TA-Lib
```

### Installation du package
```bash
git clone https://github.com/votre-utilisateur/finance-analysis-toolkit.git
cd finance-analysis-toolkit
pip install -e .
```

## Utilisation

### Exemple de base
```python
from finance_plugin import DataFetcher, DataProcessor, Visualizer, Exporter

# 1. Récupération des données
fetcher = DataFetcher('ETL.PA', '2025-09-01', '2025-09-26', interval='60m')
data = fetcher.fetch_data()

# 2. Calcul des indicateurs
processor = DataProcessor(data)
processed_data = processor.calculate_indicators()

# 3. Visualisation
Visualizer.plot_data('Eurotunnel', processed_data)

# 4. Export
Exporter.to_csv(processed_data, 'analysis_results.csv')
```

### Interface en ligne de commande
```bash
python -m finance_analysis --ticker ETL.PA --start 2025-09-01 --end 2025-09-26 --output results.csv
```

## Documentation

### Classes principales

1. **DataFetcher** : Récupération et nettoyage des données financières
   - `fetch_data()` : Télécharge les données depuis Yahoo Finance
   - `clean_dataframe()` : Nettoie et formate les données

2. **DataProcessor** : Calcul des indicateurs techniques
   - `calculate_indicators()` : Calcule SMA, RSI et MACD

3. **Visualizer** : Visualisation des données
   - `plot_data()` : Génère des graphiques professionnels

4. **Exporter** : Export des données
   - `to_csv()` : Export vers fichier CSV
   - `to_excel()` : Export vers fichier Excel

## Indicateurs techniques

### SMA (Simple Moving Average)
- Moyenne des prix sur 20 périodes
- Indique la tendance générale du marché
- Utilisé comme support/résistance dynamique

### RSI (Relative Strength Index)
- Oscillateur entre 0 et 100
- >70 : Zone de surachat
- <30 : Zone de survente
- Mesure la vitesse des mouvements de prix

### MACD (Moving Average Convergence Divergence)
- Combinaison de moyennes mobiles
- Signals de croisement pour les points d'entrée/sortie
- Histogramme pour visualiser la force de la tendance

## Exemples

### Analyse d'une action
```python
# Analyse complète d'une action
fetcher = DataFetcher('AAPL', '2025-01-01', '2025-12-31')
data = fetcher.fetch_data()

processor = DataProcessor(data)
results = processor.calculate_indicators()

Visualizer.plot_data('Apple Inc.', results)
Exporter.to_excel(results, 'apple_analysis.xlsx')
```

### Analyse comparative
```python
# Comparaison de plusieurs actions
tickers = ['ETL.PA', 'AIR.PA', 'BNP.PA']
for ticker in tickers:
    fetcher = DataFetcher(ticker, '2025-01-01', '2025-09-26')
    data = fetcher.fetch_data()
    processor = DataProcessor(data)
    results = processor.calculate_indicators()
    Visualizer.plot_data(ticker, results)
```

## Configuration

Le projet peut être configuré via :
1. Fichier `config.ini` (pour les paramètres persistants) [TODO]
2. Variables d'environnement
3. Arguments de ligne de commande

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :
1. Forker le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committer vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. Pousser vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteurs

- [Benjamin PELLIEUX](https://github.com/benjaminpellieux)

## Remerciements

- Yahoo Finance pour l'API de données financières
- TA-Lib pour les calculs d'indicateurs techniques
- La communauté open source pour les bibliothèques Python

## Structure du projet

```
finance-analysis-toolkit/
├── data_fetcher.py        # Récupération des données
├── data_processor.py      # Calcul des indicateurs
├── post_process/          # Post-traitement
│   ├── __init__.py
│   ├── data_fetcher.py
│   ├── data_processor.py
│   └── post_process.py    # Visualisation & Export des données 
├── examples/              # Exemples d'utilisation
├── tests/                 # Tests unitaires
├── setup.py
├── README.md              # Documentation principale
└── LICENSE                # Licence du projet
```

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.
