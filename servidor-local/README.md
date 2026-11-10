# Sirve una carpeta por HTTP solo en 127.0.0.1; Ctrl+C detiene.

Categoría: Desarrollo. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py servidor-local ejemplos --puerto 8000
py servidor-local/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
Sirve archivos e índices de carpetas en primer plano solo en loopback. Elige una carpeta sin secretos; otros procesos de tu equipo pueden leerla. No es un servidor de producción. Ctrl+C detiene.
