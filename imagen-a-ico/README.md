# Crear iconos ICO multirresolución

Python 3.9+ y Pillow (`py -m pip install -r requirements.txt`).

Mantiene transparencia y proporción con margen transparente. Para usarlo: Propiedades de un acceso directo → Cambiar icono. No cambia asociaciones del sistema.

```powershell
.\ejecutar.cmd logo.png mi-icono.ico
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
