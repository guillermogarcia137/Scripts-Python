# ZIP nuevo fuera del origen; omite enlaces.

Categoría: Archivos. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py copia-zip ejemplos/datos copia.zip
py copia-zip/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
No conserva carpetas vacías, ACL ni enlaces. No garantiza consistencia de archivos que cambian mientras se copian.
