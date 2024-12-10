import pdfplumber
import pandas as pd
import re

# Ruta del archivo
pdf_path = r"C:\Users\alan_\OneDrive\Escritorio\BAIRES - Resumen Galicia 31-10-2023.pdf"
#pdf_path = "/content/drive/MyDrive/Temporal/BAIRES - Resumen Galicia 31-10-2023.pdf"

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
            
            # Guardar a CSV
            df.to_csv('transacciones_bancarias.csv', index=False, sep=';',encoding='utf-8-sig', decimal=',')
            print("\nArchivo CSV generado exitosamente.")
            
            return df
        else:
            print("No se encontraron transacciones en el PDF.")
            return None
            
    except Exception as e:
        print(f"Error durante el proceso: {str(e)}")
        return None

# Ejecutar el código
if __name__ == "__main__":
    df = main()