# PDF Bank Extractor

Extractor de datos bancarios desde archivos PDF.

## Entorno virtual

activar entorno virtual

```bash
.venvPDF\Scripts\activate.bat
```
## Instalar empaquetador

```bash
pip install build
```

## Empaquetar

Construir el paquete con:

```bash
python -m build
```

## Instalación

cmd dentro de la carpeta "dist" creada con el build

```bash
pip install pdf_bank_extractor-1.0.0-py3-none-any.whl
```

## Ejecucion

```bash
pdf_extractor
```

## Seleccion de archivo, csv extracción

En ventana, seleccionar archivo ".pdf", los registros quedan en path "C:\Users\tu_usuario\PDF_Bank_Extractor"