# Consulta certificado TLS validando cadena y nombre de servidor.

Categoría: Red. Python 3.9+; solo biblioteca estándar.

Desde la raíz del repositorio:

```powershell
py cli.py certificado-tls github.com
py certificado-tls/script.py --help
```

También puedes entrar en esta carpeta y usar `py script.py` o `ejecutar.cmd`.
Conserva la carpeta `nucleo` junto a las herramientas: no copies un lanzador solo.
Las rutas relativas se resuelven desde tu carpeta de trabajo.
Los ejemplos que generan archivos requieren destinos nuevos y carpetas padre existentes.
Necesita acceso directo al servidor; una red que exija proxy puede impedir la conexión. Valida certificados; no desactiva TLS.
