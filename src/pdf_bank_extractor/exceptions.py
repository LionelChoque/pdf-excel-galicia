"""
Custom exceptions for PDF Bank Extractor
"""

class PDFExtractionError(Exception):
    """Raised when there's an error extracting data from PDF"""
    pass

class PDFValidationError(Exception):
    """Raised when the PDF file is invalid"""
    pass

class DataProcessingError(Exception):
    """Raised when there's an error processing the extracted data"""
    pass