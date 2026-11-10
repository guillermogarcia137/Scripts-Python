# Extraer colores de una imagen

Python 3.9+ y Pillow (`py -m pip install -r requirements.txt`).

Devuelve JSON de colores representativos aproximados, calculados sobre una miniatura. No representa frecuencias exactas del original. Elimina transparencia al convertir a RGB.

```powershell
.\ejecutar.cmd foto.jpg --colores 6
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
