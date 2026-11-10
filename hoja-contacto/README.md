# Crear una hoja de contacto de imágenes

Python 3.9+ y Pillow (`py -m pip install -r requirements.txt`).

Miniaturas ordenadas por nombre con etiquetas ASCII. Primer nivel; excluye el destino. Si una imagen está dañada, aborta. No modifica originales.

```powershell
.\ejecutar.cmd C:\Fotos contacto.png --columnas 4 --limite 24
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
