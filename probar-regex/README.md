# Prueba una expresión regular sobre una cadena local.

Categoría: Desarrollo. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py probar-regex "[0-9]+" "Proyecto 123"
py probar-regex/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
Python re no limita el tiempo de evaluación. Usa patrones propios sobre texto de tamaño controlado.
