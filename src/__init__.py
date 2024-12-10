"""
PDF Bank Extractor
-----------------
Package for extracting bank data from PDF files
"""

__version__ = "1.0.0"
__author__ = "Lionel Alan Choque"
__email__ = "lionelchoque@gmail.com"

from .pdf_plumber_pandas import main, run

# Exponer las funciones principales a nivel de paquete
__all__ = ['main', 'run']