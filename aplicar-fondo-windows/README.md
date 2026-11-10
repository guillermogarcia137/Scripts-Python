# Aplicar y restaurar un fondo de escritorio

Python 3.9+ sin dependencias externas.

Crea la copia de la ruta anterior antes de aplicar. No copia la imagen ni cambia su estilo de ajuste. Mantén la imagen anterior para restaurar. Pensado para un fondo estático; no preserva presentaciones, Spotlight ni configuraciones por monitor. No modifica pantalla de bloqueo.

```powershell
.\ejecutar.cmd estado
.\ejecutar.cmd aplicar --imagen C:\Fondos\fondo.png --copia anterior.json
.\ejecutar.cmd restaurar --copia anterior.json
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
