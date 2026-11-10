# Comprobar contraste de texto

Python 3.9+ sin dependencias externas.

Calcula contraste sRGB WCAG para colores opacos. No evalúa una interfaz completa. Texto grande: al menos 18 pt normal o 14 pt en negrita. Las decisiones usan la ratio sin redondear.

```powershell
.\ejecutar.cmd "#FFFFFF" "#0B1026"
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
