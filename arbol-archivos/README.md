# Árbol de rutas relativas; omite enlaces y limita la salida.

Categoría: Archivos. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py arbol-archivos ejemplos/datos
py arbol-archivos/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
Emite una lista de rutas relativas, no un dibujo de carpetas. El límite corta la salida.
