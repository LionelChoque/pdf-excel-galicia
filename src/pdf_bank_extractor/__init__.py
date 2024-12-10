"""
PDF Bank Extractor
-----------------
Package for extracting bank data from PDF files
"""

__version__ = "1.0.0"
__author__ = "Lionel Alan Choque"
__email__ = "lionelchoque@gmail.com"

from .pdf_extractor import main, run
from .utils import setup_environment

__all__ = ['main', 'run', 'setup_environment']