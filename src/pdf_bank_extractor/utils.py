"""
Utility functions for PDF Bank Extractor
"""

import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def setup_environment():
    """Configura el entorno de ejecución"""
    try:
        output_dir = Path.home() / "PDF_Bank_Extractor"
        output_dir.mkdir(exist_ok=True)
        return output_dir
    except Exception as e:
        logger.error(f"Error configurando el entorno: {e}")
        return None

def validate_pdf(file_path):
    """Valida que el archivo PDF existe y es accesible"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        if not file_path.lower().endswith('.pdf'):
            raise ValueError("El archivo debe ser un PDF")
        return True
    except Exception as e:
        logger.error(f"Error validando PDF: {e}")
        return False