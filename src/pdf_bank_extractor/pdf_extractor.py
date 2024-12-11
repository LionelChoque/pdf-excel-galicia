import sys
import logging
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os
import pdfplumber
import pandas as pd
import re
from .utils import setup_environment


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_pdf_path_gui():
    
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de tkinter
    while True:
        file_path = filedialog.askopenfilename(
            title="Seleccione el archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if file_path:  # Si se seleccionó un archivo
            if os.path.exists(file_path):
                return file_path
        else:  # Si el usuario canceló la selección
            if tk.messagebox.askokcancel("Cancelar", "¿Desea salir del programa?"):
                sys.exit()
            continue
        

def extract_text_from_pdf(pdf_path):
    """Extrae el texto del PDF y lo muestra para debugging"""
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            print(f"\n--- Página {i+1} ---")
            print(text)
            all_text.append(text)
    return all_text

def process_line(text):
    transactions = []
    # Dividimos el texto en líneas
    lines = text.split('\n')
    
    # Patrón para fecha
    date_pattern = r'\d{2}/\d{2}/\d{2}'
    
    for line in lines:
        # Si la línea contiene una fecha
        if re.search(date_pattern, line):
            try:
                # Separamos los componentes
                parts = line.split()
                date = parts[0]  # Primera parte es la fecha
                
                # Buscamos los valores numéricos al final de la línea
                numbers = re.findall(r'-?[\d.]+\,\d{2}', line)
                
                # La descripción es todo lo que está entre la fecha y los números
                description = ' '.join(parts[1:len(parts)-len(numbers)])
                
                transaction = {
                    'Fecha': date,
                    'Descripción': description,
                    'Crédito': '',
                    'Débito': '',
                    'Saldo': numbers[-1] if numbers else ''
                }
                
                # Si hay más números, asignamos débito o crédito
                if len(numbers) > 1:
                    #if 'ACREDITAMIENTO' in description or 'DEPOSITO' in description:
                    if  '-' in (numbers[0]) :
                        transaction['Débito'] = numbers[0]
                        print(numbers[0], 'DEBITO +++++++++')
                    else:
                        transaction['Crédito'] = numbers[0]
                        print(numbers[0], 'CREDITO ----------')
                transactions.append(transaction)
                print(f"Transacción procesada: {transaction}")  # Para debugging
                
            except Exception as e:
                print(f"Error procesando línea: {line}")
                print(f"Error: {str(e)}")
                continue
                
    return transactions

def format_output(df):
    try:
        # Convertir fecha
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%y')
        
        # Limpiar y convertir valores numéricos
        for col in ['Crédito', 'Débito', 'Saldo']:
            df[col] = df[col].str.replace(',', '').astype(float)
        
        return df
    except Exception as e:
        print(f"Error en format_output: {str(e)}")
        return df

def main():
    try:
        # Obtener la ruta del archivo mediante interfaz gráfica
        pdf_path = get_pdf_path_gui()
        # Obtener el nombre base del archivo PDF sin la extensión
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        # Primero extraemos y mostramos el texto para debugging
        print("Extrayendo texto del PDF...")
        all_text = extract_text_from_pdf(pdf_path)
        
        # Procesamos las transacciones
        all_transactions = []
        for page_text in all_text:
            transactions = process_line(page_text)
            all_transactions.extend(transactions)
        
        # Creamos el DataFrame
        if all_transactions:
            df = pd.DataFrame(all_transactions)
            df = format_output(df)
            
            print("\nTransacciones extraídas:")
            print(df)
            
            # Guardar a CSV con el mismo nombre que el PDF
            csv_filename = f'{pdf_name}.csv'
            df.to_csv(csv_filename, index=False, sep=';', encoding='utf-8-sig', decimal=',')
            print(f"\nArchivo CSV generado exitosamente como: {csv_filename}")
            
            return df, pdf_name  # Retornamos también el nombre del archivo
        else:
            print("No se encontraron transacciones en el PDF.")
            return None, None
            
    except Exception as e:
        print(f"Error durante el proceso: {str(e)}")
        return None, None
    
    
'''
# Ejecutar el código
if __name__ == "__main__":
    df = main()
'''
    
def run():
    """Función principal de ejecución"""
    try:
        output_dir = setup_environment()
        if not output_dir:
            sys.exit(1)

        df, pdf_name = main()  # Recibimos también el nombre del archivo
        
        if df is not None and pdf_name is not None:
            output_file = output_dir / f"{pdf_name}.csv"
            df.to_csv(output_file, index=False, sep=';', encoding='utf-8-sig', decimal=',')
            logger.info(f"Archivo guardado en: {output_file}")
            
            if sys.platform == 'win32':
                os.startfile(output_dir)
    
    except Exception as e:
        logger.error(f"Error en la ejecución: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    run()