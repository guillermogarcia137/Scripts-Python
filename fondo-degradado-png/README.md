# Crear fondo PNG para Windows

Python 3.9+ y Pillow (`py -m pip install -r requirements.txt`).

Genera un PNG opaco listo para seleccionar como fondo. No cambia Windows. Máximo 40 megapíxeles.

```powershell
.\ejecutar.cmd fondo.png --ancho 2560 --alto 1440 --inicio "#10152E" --fin "#46C9B5"
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
