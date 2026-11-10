# Panel visual con tipografía y colores

Python 3.9+ sin dependencias externas.

Exporta SVG editable, sin modificar el escritorio. Windows necesita un PNG/JPEG para usarlo como fondo: exporta el SVG desde un editor vectorial. Las fuentes dependen de las instaladas en el equipo. `--semilla` controla el mosaico; `--texto` se usa en monograma y panel.

```powershell
.\ejecutar.cmd ejemplo.svg --primario "#0B1026" --secundario "#56DCC6"
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
