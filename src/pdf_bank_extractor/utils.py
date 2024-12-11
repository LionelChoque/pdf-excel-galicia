"""
Utility functions for PDF Bank Extractor
"""

import os
from pathlib import Path
import logging
import shutil
from typing import Union, Optional

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment() -> Optional[Path]:
    """
    Configura el entorno de ejecución creando los directorios necesarios.
    
    Returns:
        Path: Directorio de salida si se creó correctamente
        None: Si hubo un error en la creación
    """
    try:
        output_dir = Path.home() / "PDF_Bank_Extractor"
        output_dir.mkdir(exist_ok=True)
        
        # Crear subdirectorios para mejor organización
        (output_dir / "processed").mkdir(exist_ok=True)
        (output_dir / "output").mkdir(exist_ok=True)
        (output_dir / "logs").mkdir(exist_ok=True)
        
        logger.info(f"Ambiente configurado exitosamente en: {output_dir}")
        return output_dir
    except Exception as e:
        logger.error(f"Error configurando el entorno: {str(e)}")
        return None

def validate_pdf(file_path: Union[str, Path]) -> bool:
    """
    Valida que el archivo PDF existe, es accesible y tiene un tamaño válido.
    
    Args:
        file_path: Ruta al archivo PDF
        
    Returns:
        bool: True si el archivo es válido, False en caso contrario
    """
    try:
        # Convertir a Path si es string
        file_path = Path(file_path)
        
        # Validaciones básicas
        if not file_path.exists():
            raise FileNotFoundError(f"El archivo {file_path} no existe")
        
        if not file_path.suffix.lower() == '.pdf':
            raise ValueError("El archivo debe ser un PDF")
        
        # Validar permisos de lectura
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"No hay permisos de lectura para {file_path}")
        
        # Validar tamaño del archivo (ejemplo: máximo 100MB)
        max_size = 100 * 1024 * 1024  # 100MB en bytes
        if file_path.stat().st_size > max_size:
            raise ValueError(f"El archivo excede el tamaño máximo permitido de 100MB")
        
        logger.info(f"Archivo PDF validado correctamente: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error validando PDF: {str(e)}")
        return False

def clean_environment(output_dir: Path) -> bool:
    """
    Limpia los archivos temporales y directorios de trabajo.
    
    Args:
        output_dir: Directorio de salida a limpiar
        
    Returns:
        bool: True si la limpieza fue exitosa, False en caso contrario
    """
    try:
        if output_dir.exists():
            shutil.rmtree(output_dir)
            logger.info(f"Directorio {output_dir} eliminado correctamente")
        return True
    except Exception as e:
        logger.error(f"Error limpiando el ambiente: {str(e)}")
        return False