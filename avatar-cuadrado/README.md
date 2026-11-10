# Preparar un avatar cuadrado

Python 3.9+ y Pillow (`py -m pip install -r requirements.txt`).

Recorta al centro, sin detección facial. Corrige orientación EXIF. Exporta PNG RGB sin metadatos ni animación.

```powershell
.\ejecutar.cmd retrato.jpg avatar.png --lado 512
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
