# Crea manifiesto JSON de rutas relativas, tamaños y SHA-256.

Categoría: Documentos. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py manifiesto-sha256 ejemplos/datos manifiesto.json
py manifiesto-sha256/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
Guarda el manifiesto fuera del origen para que su propia presencia no altere futuras verificaciones.
