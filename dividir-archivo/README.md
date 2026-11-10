# Divide en partes y genera manifiesto SHA-256 en carpeta nueva.

Categoría: Archivos. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py dividir-archivo ejemplos/datos/notas.txt partes --mb 1
py dividir-archivo/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
Si falla a mitad, conserva la carpeta parcial para revisión; usa otro destino al reintentar.
