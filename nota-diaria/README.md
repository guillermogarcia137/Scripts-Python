# Crea una nota Markdown del día sin sobrescribir notas previas.

Categoría: Productividad. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py nota-diaria ejemplos/datos
py nota-diaria/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
La fecha usa la zona horaria local del equipo. Una nota existente se conserva.
