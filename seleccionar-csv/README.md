# Selecciona columnas de un CSV en el orden pedido.

Categoría: Datos. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py seleccionar-csv ejemplos/datos/personas.csv nombres.csv nombre
py seleccionar-csv/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
 Los CSV se procesan en memoria. Usa punto decimal. Los valores exportados se conservan literalmente: al abrirlos en Excel, importa las celdas como texto si los datos no son confiables.
