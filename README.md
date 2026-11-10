# Scripts-Python

**100 herramientas útiles en Python**, cada una con carpeta, ayuda y ejemplo.
No son 100 variantes del mismo programa: incluyen archivos, datos, texto,
productividad, desarrollo, red, sistema y 18 herramientas de diseño y Windows.

## Empezar

Requiere Python 3.9 o posterior. Windows puede usar `py`; Linux y macOS, `python3`.
Para las seis herramientas de imágenes, instala Pillow en un entorno virtual:

```powershell
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python cli.py --help
```

Sin Pillow puedes utilizar las otras 94 herramientas. Los lanzadores CMD usan
el Python predeterminado (`py -3`, o `python` si no existe py); para usar el entorno
virtual invoca explícitamente su ejecutable como en el ejemplo anterior.

Las 82 herramientas generales se ejecutan con `py cli.py NOMBRE --help` o con
`py NOMBRE/script.py --help`. Comparten `nucleo`: conserva el repositorio completo.
Las 18 de diseño/Windows se ejecutan con `py NOMBRE/script.py --help`.
Los tres ajustes de Windows consultan el estado por defecto; no se aplican al
instalar o al ejecutar pruebas. Las rutas de los ejemplos generales se interpretan
desde la raíz. Los ejemplos visuales en cada README se ejecutan desde su carpeta.

## Catálogo: 100 herramientas

### Archivos (14)

| Herramienta | Uso |
| --- | --- |
| [arbol-archivos](arbol-archivos/README.md) | Árbol de rutas relativas; omite enlaces y limita la salida. |
| [archivos-grandes](archivos-grandes/README.md) | Los archivos de mayor tamaño, sin borrar. |
| [buscar-duplicados](buscar-duplicados/README.md) | Duplicados SHA-256; nunca elimina datos. |
| [buscar-extension](buscar-extension/README.md) | Busca archivos recursivamente por extensión. |
| [carpetas-vacias](carpetas-vacias/README.md) | Informa carpetas vacías, sin eliminarlas. |
| [comparar-carpetas](comparar-carpetas/README.md) | Comparación recursiva por ruta relativa y contenido SHA-256. |
| [comprobar-zip](comprobar-zip/README.md) | Comprueba CRC de un ZIP sin extraer archivos. |
| [copia-zip](copia-zip/README.md) | ZIP nuevo fuera del origen; omite enlaces. |
| [dividir-archivo](dividir-archivo/README.md) | Divide en partes y genera manifiesto SHA-256 en carpeta nueva. |
| [firma-archivo](firma-archivo/README.md) | Identifica firmas comunes sin confiar en la extensión. |
| [hash-archivo](hash-archivo/README.md) | Huella SHA-256 de un archivo. |
| [inventario-archivos](inventario-archivos/README.md) | Inventario recursivo CSV con tamaños y fechas UTC. |
| [listar-zip](listar-zip/README.md) | Lista contenido de un ZIP sin extraerlo. |
| [unir-archivo](unir-archivo/README.md) | Une partes verificadas; elimina salida parcial si falla. |

### Texto (14)

| Herramienta | Uso |
| --- | --- |
| [ajustar-parrafos](ajustar-parrafos/README.md) | Reajusta el ancho de párrafos conservando separaciones vacías. |
| [buscar-regex](buscar-regex/README.md) | Busca un patrón en un archivo local con números de línea. |
| [contar-lineas](contar-lineas/README.md) | Cuenta líneas, líneas vacías y caracteres. |
| [crear-slug](crear-slug/README.md) | Convierte un título en slug ASCII para nombres o URLs. |
| [diferencias-texto](diferencias-texto/README.md) | Diferencias unificadas entre dos archivos UTF-8. |
| [extraer-emails](extraer-emails/README.md) | Extrae candidatos de correo de texto local; no valida buzones. |
| [extraer-enlaces](extraer-enlaces/README.md) | Extrae candidatos HTTP/HTTPS sin abrirlos. |
| [frecuencia-palabras](frecuencia-palabras/README.md) | Frecuencias de palabras Unicode. |
| [normalizar-espacios](normalizar-espacios/README.md) | Quita espacios finales y compacta espacios horizontales. |
| [numerar-lineas](numerar-lineas/README.md) | Crea una copia de texto con números de línea. |
| [ordenar-lineas](ordenar-lineas/README.md) | Ordena líneas alfabéticamente sin distinguir mayúsculas. |
| [quitar-lineas-repetidas](quitar-lineas-repetidas/README.md) | Elimina líneas repetidas conservando su primer orden. |
| [reemplazar-texto](reemplazar-texto/README.md) | Reemplaza texto literal y guarda una copia nueva. |
| [unir-textos](unir-textos/README.md) | Une archivos UTF-8 en el orden indicado. |

### Datos (14)

| Herramienta | Uso |
| --- | --- |
| [aplanar-json](aplanar-json/README.md) | Lista hojas JSON con rutas JSON Pointer y valores. |
| [comparar-json](comparar-json/README.md) | Compara estructuras JSON ignorando el orden de claves. |
| [csv-a-json](csv-a-json/README.md) | Convierte CSV con cabecera a una lista JSON de cadenas. |
| [detectar-delimitador](detectar-delimitador/README.md) | Estima el delimitador de un archivo tabular. |
| [estadisticas-csv](estadisticas-csv/README.md) | Estadísticas de una columna numérica; rechaza valores vacíos. |
| [filtrar-csv](filtrar-csv/README.md) | Filtra CSV por igualdad literal en una columna. |
| [formatear-json](formatear-json/README.md) | Valida y formatea JSON en un archivo nuevo. |
| [fusionar-json](fusionar-json/README.md) | Fusiona objetos JSON de primer nivel; rechaza claves repetidas. |
| [inventario-xml](inventario-xml/README.md) | Lista frecuencias de etiquetas en XML local sin DTD. |
| [json-a-csv](json-a-csv/README.md) | Convierte una lista de objetos planos JSON en CSV. |
| [ndjson-a-json](ndjson-a-json/README.md) | Convierte JSON por línea a un array JSON; omite líneas vacías. |
| [ordenar-csv](ordenar-csv/README.md) | Ordena CSV por columna, alfabéticamente o como decimal. |
| [seleccionar-csv](seleccionar-csv/README.md) | Selecciona columnas de un CSV en el orden pedido. |
| [transponer-csv](transponer-csv/README.md) | Transpone filas y columnas de una matriz CSV rectangular. |

### Desarrollo (12)

| Herramienta | Uso |
| --- | --- |
| [codificar-base64](codificar-base64/README.md) | Codifica un archivo como Base64 ASCII en una copia nueva. |
| [codificar-url](codificar-url/README.md) | Escapa un componente de URL sin realizar peticiones. |
| [convertir-epoch](convertir-epoch/README.md) | Convierte segundos Unix a fecha UTC ISO 8601. |
| [crear-gitignore](crear-gitignore/README.md) | Crea .gitignore para Python con cachés, entornos y secretos habituales. |
| [decodificar-base64](decodificar-base64/README.md) | Decodifica Base64 estricto a un archivo nuevo. |
| [decodificar-url](decodificar-url/README.md) | Decodifica escapes porcentuales UTF-8 sin navegar. |
| [generar-contrasena](generar-contrasena/README.md) | Genera contraseña con aleatoriedad criptográfica. |
| [generar-token](generar-token/README.md) | Genera token URL-safe con secrets. |
| [generar-uuid](generar-uuid/README.md) | Genera identificadores UUID v4 aleatorios. |
| [probar-regex](probar-regex/README.md) | Prueba una expresión regular sobre una cadena local. |
| [revisar-requirements](revisar-requirements/README.md) | Detecta nombres repetidos y referencias locales en requirements; no busca vulnerabilidades. |
| [servidor-local](servidor-local/README.md) | Sirve una carpeta por HTTP solo en 127.0.0.1; Ctrl+C detiene. |

### Productividad (10)

| Herramienta | Uso |
| --- | --- |
| [calendario-html](calendario-html/README.md) | Genera un calendario mensual HTML imprimible. |
| [checklist-html](checklist-html/README.md) | Convierte una línea por tarea en lista HTML imprimible. |
| [convertir-unidades](convertir-unidades/README.md) | Convierte longitud, masa, almacenamiento o temperatura. |
| [crear-proyecto](crear-proyecto/README.md) | Crea estructura nueva con documentación, recursos, código y exportaciones. |
| [indice-markdown](indice-markdown/README.md) | Lista encabezados Markdown fuera de bloques de código. |
| [nota-diaria](nota-diaria/README.md) | Crea una nota Markdown del día sin sobrescribir notas previas. |
| [pomodoro](pomodoro/README.md) | Temporizador de trabajo y descanso con reloj monotónico. |
| [resumen-gastos](resumen-gastos/README.md) | Suma importes CSV categoria,importe con decimales exactos. |
| [resumen-horas](resumen-horas/README.md) | Suma horas por proyecto desde CSV proyecto,horas. |
| [resumen-tareas](resumen-tareas/README.md) | Resume tareas de CSV tarea,estado por estado. |

### Red (6)

| Herramienta | Uso |
| --- | --- |
| [analizar-url](analizar-url/README.md) | Descompone una URL localmente sin abrirla; omite contraseña. |
| [cabeceras-http](cabeceras-http/README.md) | Consulta cabeceras HTTP/HTTPS con HEAD y timeout. |
| [calcular-subred](calcular-subred/README.md) | Calcula red, máscara y rango sin enumerar todos los hosts. |
| [certificado-tls](certificado-tls/README.md) | Consulta certificado TLS validando cadena y nombre de servidor. |
| [comprobar-tcp](comprobar-tcp/README.md) | Comprueba una conexión TCP con tiempo máximo. |
| [resolver-dns](resolver-dns/README.md) | Resuelve IPv4/IPv6 usando el DNS del sistema. |

### Sistema (6)

| Herramienta | Uso |
| --- | --- |
| [espacio-disco](espacio-disco/README.md) | Consulta espacio total, usado y libre en una ruta. |
| [informacion-sistema](informacion-sistema/README.md) | Resumen del sistema y Python sin nombres de usuario. |
| [listar-procesos](listar-procesos/README.md) | Consulta procesos mediante tasklist en Windows o ps en Unix. |
| [localizar-programa](localizar-programa/README.md) | Localiza un ejecutable en PATH sin ejecutarlo. |
| [nombres-entorno](nombres-entorno/README.md) | Lista nombres de variables de entorno, sin mostrar valores. |
| [revisar-path](revisar-path/README.md) | Detecta entradas inexistentes y repetidas del PATH. |

### Documentos (6)

| Herramienta | Uso |
| --- | --- |
| [convertir-codificacion](convertir-codificacion/README.md) | Convierte texto desde una codificación explícita a UTF-8 estricto. |
| [escapar-html](escapar-html/README.md) | Escapa texto para mostrarlo como HTML sin interpretarlo. |
| [html-a-texto](html-a-texto/README.md) | Extrae texto de HTML local omitiendo scripts y estilos. |
| [manifiesto-sha256](manifiesto-sha256/README.md) | Crea manifiesto JSON de rutas relativas, tamaños y SHA-256. |
| [markdown-a-html](markdown-a-html/README.md) | Convierte un subconjunto de Markdown a HTML estático escapado. |
| [verificar-manifiesto](verificar-manifiesto/README.md) | Verifica un manifiesto SHA-256 y rechaza rutas fuera del origen. |

### Diseño y Windows (18)

| Herramienta | Uso |
| --- | --- |
| [alineacion-barra-w11](alineacion-barra-w11/README.md) | Alinear la barra de tareas de Windows 11 |
| [animaciones-interfaz](animaciones-interfaz/README.md) | Consultar o ajustar animaciones del área cliente |
| [aplicar-fondo-windows](aplicar-fondo-windows/README.md) | Aplicar y restaurar un fondo de escritorio |
| [avatar-cuadrado](avatar-cuadrado/README.md) | Preparar un avatar cuadrado |
| [contraste-colores](contraste-colores/README.md) | Comprobar contraste de texto |
| [fondo-degradado-png](fondo-degradado-png/README.md) | Crear fondo PNG para Windows |
| [fondo-degradado-svg](fondo-degradado-svg/README.md) | Fondo con degradado vectorial |
| [fondo-desenfocado](fondo-desenfocado/README.md) | Crear un fondo desenfocado desde una foto |
| [fondo-mosaico-svg](fondo-mosaico-svg/README.md) | Fondo geométrico con semilla |
| [fondo-ondas-svg](fondo-ondas-svg/README.md) | Fondo de ondas vectoriales |
| [fondo-orbitas-svg](fondo-orbitas-svg/README.md) | Fondo de órbitas minimalistas |
| [hoja-contacto](hoja-contacto/README.md) | Crear una hoja de contacto de imágenes |
| [icono-monograma-svg](icono-monograma-svg/README.md) | Icono vectorial con iniciales |
| [imagen-a-ico](imagen-a-ico/README.md) | Crear iconos ICO multirresolución |
| [paleta-desde-imagen](paleta-desde-imagen/README.md) | Extraer colores de una imagen |
| [panel-inspiracion-svg](panel-inspiracion-svg/README.md) | Panel visual con tipografía y colores |
| [rejilla-puntos-svg](rejilla-puntos-svg/README.md) | Rejilla de puntos para diseño |
| [zonas-escritorio-svg](zonas-escritorio-svg/README.md) | Fondo con zonas para organizar iconos |

## Ejemplos y resultados

[Galería de diseño](ejemplos/README.md) y [datos de prueba](ejemplos/datos).
Los ejemplos son sintéticos y no contienen datos personales.

## Comportamiento y límites

Las salidas se crean sin sobrescribir archivos existentes. Si una escritura falla,
puede quedar un archivo parcial: revísalo y usa otro nombre al reintentar. La copia
ZIP y la unión de partes eliminan su salida incompleta. No hay borrado masivo,
instalación de programas ni cambios automáticos al importar módulos.

Los recorridos de archivos omiten enlaces/junctions encontrados durante el recorrido;
no son una defensa contra cambios concurrentes de rutas. Los informes, las rutas,
los datos exportados y los secretos generados pueden ser privados: revísalos antes
de compartirlos. Las herramientas de texto/datos cargan habitualmente el archivo
en memoria; están pensadas para archivos locales de tamaño moderado.

Los generadores SVG no cambian el escritorio; Windows necesita exportarlos a PNG/JPEG
para usarlos como fondo. Las herramientas de imágenes exportan píxeles y no conservan
EXIF ni animación. La configuración real de Windows depende de la versión y políticas
del equipo; lee los límites y la forma de revertir en cada README.

## Pruebas

`python -m unittest discover -s tests -v`. GitHub Actions ejecuta comprobaciones en
Windows y Linux. Las pruebas usan archivos desechables y conexiones locales; no
cambian temas, fondos, barra de tareas o preferencias del equipo. No sustituyen la
validación manual de los tres ajustes en Windows 11.

Este repositorio contiene herramientas Python y lanzadores CMD opcionales.
`Scripts-Windows` y `Activar-Windows` se mantienen separados y sin cambios.
