# Consultar o ajustar animaciones del área cliente

Python 3.9+ sin dependencias externas.

Usa la API de Windows SPI_GET/SETCLIENTAREAANIMATION. Afecta animaciones del área cliente en aplicaciones que respeten esta preferencia; no controla todas las animaciones del sistema. Guarda el estado mostrado y aplica activar/desactivar para revertir.

```powershell
.\ejecutar.cmd estado
.\ejecutar.cmd desactivar
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
