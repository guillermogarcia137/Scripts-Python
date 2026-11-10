# Detecta nombres repetidos y referencias locales en requirements; no busca vulnerabilidades.

Categoría: Desarrollo. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py revisar-requirements requirements.txt
py revisar-requirements/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
