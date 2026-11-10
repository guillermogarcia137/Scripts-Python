# Alinear la barra de tareas de Windows 11

Python 3.9+ sin dependencias externas.

Estado por defecto. Modifica solo TaskbarAl del usuario. Anota el valor anterior y usa centro/izquierda para volver. Para un valor originalmente ausente, restablece la preferencia desde Configuración → Personalización → Barra de tareas. Esta clave puede cambiar o ser ignorada en futuras versiones de Windows. No afecta políticas de empresa.

```powershell
.\ejecutar.cmd estado
.\ejecutar.cmd izquierda
```

`py script.py --help` muestra todas las opciones. `ejecutar.cmd` inicia Python
y transmite argumentos. Los archivos de salida deben ser nuevos; sus carpetas
padre deben existir.
