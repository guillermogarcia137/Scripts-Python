"""Herramientas locales para desarrollo y conversiones."""
from . import *
import re

@tool('generar-uuid','Desarrollo','Genera identificadores UUID v4 aleatorios.',arg('--cantidad',type=positive,default=1))
def uuids(a):
    import uuid
    if a.cantidad>10000:
        raise ValueError('Máximo 10000 identificadores.')
    return [str(uuid.uuid4()) for _ in range(a.cantidad)]

@tool('generar-contrasena','Desarrollo','Genera contraseña con aleatoriedad criptográfica.',arg('--longitud',type=positive,default=24))
def password(a):
    import secrets,string
    if not 12<=a.longitud<=1024:
        raise ValueError('Longitud entre 12 y 1024.')
    groups=[string.ascii_lowercase,string.ascii_uppercase,string.digits,'!@#$%*-_=+']
    chars=''.join(groups)
    while True:
        value=''.join(secrets.choice(chars) for _ in range(a.longitud))
        if all(any(c in g for c in value) for g in groups):
            return {'contrasena':value}

@tool('generar-token','Desarrollo','Genera token URL-safe con secrets.',arg('--bytes',type=positive,default=32))
def token(a):
    import secrets
    if a.bytes>4096:
        raise ValueError('Máximo 4096 bytes.')
    return {'token':secrets.token_urlsafe(a.bytes),'entropia_bits':a.bytes*8}

@tool('codificar-base64','Desarrollo','Codifica un archivo como Base64 ASCII en una copia nueva.',arg('origen'),arg('destino'))
def b64_encode(a):
    import base64
    write(a.destino,base64.b64encode(Path(a.origen).read_bytes()).decode('ascii')+'\n')

@tool('decodificar-base64','Desarrollo','Decodifica Base64 estricto a un archivo nuevo.',arg('origen'),arg('destino'))
def b64_decode(a):
    import base64,binascii
    try:
        value=base64.b64decode(''.join(read(a.origen).split()),validate=True)
    except binascii.Error as exc:
        raise ValueError(str(exc))
    with Path(a.destino).open('xb') as stream:
        stream.write(value)

@tool('codificar-url','Desarrollo','Escapa un componente de URL sin realizar peticiones.',arg('texto'))
def url_encode(a):
    from urllib.parse import quote
    return {'codificado':quote(a.texto,safe='')}

@tool('decodificar-url','Desarrollo','Decodifica escapes porcentuales UTF-8 sin navegar.',arg('texto'))
def url_decode(a):
    from urllib.parse import unquote
    return {'decodificado':unquote(a.texto,errors='strict')}

@tool('convertir-epoch','Desarrollo','Convierte segundos Unix a fecha UTC ISO 8601.',arg('segundos',type=float))
def epoch(a):
    from datetime import datetime,timezone
    try:
        return {'utc':datetime.fromtimestamp(a.segundos,timezone.utc).isoformat()}
    except (OverflowError,OSError) as exc:
        raise ValueError(str(exc))

@tool('probar-regex','Desarrollo','Prueba una expresión regular sobre una cadena local.',arg('patron'),arg('texto'))
def regex(a):
    try:
        pattern=re.compile(a.patron)
        return [{'inicio':m.start(),'fin':m.end(),'texto':m.group(),'grupos':m.groups()} for m in pattern.finditer(a.texto)]
    except re.error as exc:
        raise ValueError(str(exc))

@tool('crear-gitignore','Desarrollo','Crea .gitignore para Python con cachés, entornos y secretos habituales.',arg('destino'))
def gitignore(a):
    write(a.destino,'__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\n.env.*\n!.env.example\n.pytest_cache/\n.coverage\nhtmlcov/\nbuild/\ndist/\n*.egg-info/\n')

@tool('revisar-requirements','Desarrollo','Detecta nombres repetidos y referencias locales en requirements; no busca vulnerabilidades.',arg('origen'))
def requirements(a):
    seen={}
    special=[]
    for i,line in enumerate(read(a.origen).splitlines(),1):
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        match=re.match(r'^([A-Za-z0-9][A-Za-z0-9_.-]*)(?:\[|\s|[<>=!~;@]|$)',line)
        if match and not line.startswith(('-','http:','https:','git+')):
            name=re.sub(r'[-_.]+','-',match[1]).lower()
            seen.setdefault(name,[]).append(i)
        else:
            special.append({'linea':i,'referencia':line})
    return {'nombres_repetidos':{k:v for k,v in seen.items() if len(v)>1},'referencias_a_revisar':special,'nota':'No instala paquetes ni consulta avisos de seguridad.'}

@tool('servidor-local','Desarrollo','Sirve una carpeta por HTTP solo en 127.0.0.1; Ctrl+C detiene.',arg('carpeta'),arg('--puerto',type=int,default=8000))
def server(a):
    import functools
    from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
    if not 1<=a.puerto<=65535:
        raise ValueError('Puerto entre 1 y 65535.')
    root=Path(a.carpeta).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Se necesita una carpeta.')
    class Handler(SimpleHTTPRequestHandler):
        def translate_path(self,path):
            result=Path(super().translate_path(path)).resolve()
            if result!=root and root not in result.parents:
                return str(root/'__ruta_no_permitida__')
            return str(result)
    handler=functools.partial(Handler,directory=str(root))
    with ThreadingHTTPServer(('127.0.0.1',a.puerto),handler) as http:
        print(f'http://127.0.0.1:{a.puerto} — {root}',flush=True)
        http.serve_forever()
