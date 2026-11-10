# Crear un fondo desenfocado desde una foto

Python 3.9+ y Pillow (`py -m pip install -r requirements.txt`).

Recorta al centro para llenar el fondo, corrige orientación EXIF y elimina metadatos. Procesa el primer fotograma; conserva el original.

```powershell
.\ejecutar.cmd foto.jpg fondo.png --radio 45
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
