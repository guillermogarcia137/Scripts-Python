# Convierte un subconjunto de Markdown a HTML estático escapado.

Categoría: Documentos. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py markdown-a-html README.md documento.html
py markdown-a-html/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
Subconjunto: encabezados ATX, párrafos y bloques con triple acento grave. No implementa tablas, enlaces, énfasis ni Markdown completo.
