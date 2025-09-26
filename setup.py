from setuptools import setup, find_packages

setup(
    name="finance_plugin",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'yfinance',
        'pandas',
        'matplotlib',
        'TA-Lib'
    ],
    python_requires='>=3.8',
)
