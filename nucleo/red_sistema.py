"""Consultas de red, sistema y conversiones de documentos."""
from . import *

@tool('resolver-dns','Red','Resuelve IPv4/IPv6 usando el DNS del sistema.',arg('servidor'))
def dns(a):
    import socket
    return sorted(set(info[4][0] for info in socket.getaddrinfo(a.servidor,None)))

@tool('comprobar-tcp','Red','Comprueba una conexión TCP con tiempo máximo.',arg('servidor'),arg('puerto',type=int),arg('--timeout',type=positive,default=5))
def tcp(a):
    import socket,time
    if not 1<=a.puerto<=65535:
        raise ValueError('Puerto entre 1 y 65535.')
    start=time.monotonic()
    with socket.create_connection((a.servidor,a.puerto),timeout=a.timeout):
        return {'conectado':True,'latencia_ms':round((time.monotonic()-start)*1000,2)}

@tool('cabeceras-http','Red','Consulta cabeceras HTTP/HTTPS con HEAD y timeout.',arg('url'),arg('--timeout',type=positive,default=10))
def headers(a):
    from urllib.request import Request,urlopen
    from urllib.parse import urlsplit
    if urlsplit(a.url).scheme not in ('http','https'):
        raise ValueError('Solo HTTP o HTTPS.')
    with urlopen(Request(a.url,method='HEAD'),timeout=a.timeout) as response:
        return {'url_final':response.url,'estado':response.status,'cabeceras':dict(response.headers)}

@tool('certificado-tls','Red','Consulta certificado TLS validando cadena y nombre de servidor.',arg('servidor'),arg('--puerto',type=int,default=443))
def certificate(a):
    import ssl,socket
    if not 1<=a.puerto<=65535:
        raise ValueError('Puerto entre 1 y 65535.')
    context=ssl.create_default_context()
    with socket.create_connection((a.servidor,a.puerto),timeout=10) as raw:
        with context.wrap_socket(raw,server_hostname=a.servidor) as secured:
            cert=secured.getpeercert()
            return {'servidor':a.servidor,'protocolo':secured.version(),'emisor':cert.get('issuer'),'valido_desde':cert.get('notBefore'),'valido_hasta':cert.get('notAfter'),'nombres':cert.get('subjectAltName')}

@tool('analizar-url','Red','Descompone una URL localmente sin abrirla; omite contraseña.',arg('url'))
def parse_url(a):
    from urllib.parse import urlsplit,parse_qs
    value=urlsplit(a.url)
    return {'esquema':value.scheme,'servidor':value.hostname,'puerto':value.port,'ruta':value.path,'parametros':parse_qs(value.query,keep_blank_values=True),'fragmento':value.fragment,'contiene_credenciales':value.username is not None}

@tool('calcular-subred','Red','Calcula red, máscara y rango sin enumerar todos los hosts.',arg('cidr'))
def subnet(a):
    import ipaddress
    net=ipaddress.ip_network(a.cidr,strict=False)
    first=next(net.hosts(),None)
    last=net.broadcast_address if net.version==6 or net.num_addresses<=2 else net.broadcast_address-1
    return {'red':str(net),'mascara':str(net.netmask),'direcciones':net.num_addresses,'primer_host':str(first),'ultimo_host':str(last),'broadcast':str(net.broadcast_address) if net.version==4 else None}

@tool('informacion-sistema','Sistema','Resumen del sistema y Python sin nombres de usuario.',)
def system(a):
    import platform
    return {'sistema':platform.system(),'version':platform.version(),'arquitectura':platform.machine(),'python':platform.python_version(),'procesadores_logicos':os.cpu_count()}

@tool('espacio-disco','Sistema','Consulta espacio total, usado y libre en una ruta.',arg('ruta',nargs='?',default='.'))
def disk(a):
    import shutil
    usage=shutil.disk_usage(a.ruta)
    return {'total_bytes':usage.total,'usado_bytes':usage.used,'libre_bytes':usage.free,'usado_porcentaje':round(usage.used*100/usage.total,2)}

@tool('revisar-path','Sistema','Detecta entradas inexistentes y repetidas del PATH.',)
def path_check(a):
    paths=os.environ.get('PATH','').split(os.pathsep)
    seen=set()
    result=[]
    for p in paths:
        normalized=os.path.normcase(os.path.abspath(p))
        result.append({'ruta':p,'existe':bool(p) and Path(p).is_dir(),'repetida':normalized in seen})
        seen.add(normalized)
    return result

@tool('nombres-entorno','Sistema','Lista nombres de variables de entorno, sin mostrar valores.',)
def env(a):
    return sorted(os.environ)

@tool('listar-procesos','Sistema','Consulta procesos mediante tasklist en Windows o ps en Unix.',)
def processes(a):
    import subprocess
    command=['tasklist','/FO','CSV'] if os.name=='nt' else ['ps','-eo','pid,comm']
    result=subprocess.run(command,capture_output=True,text=True,errors='replace',timeout=20,check=False)
    if result.returncode:
        raise ValueError(result.stderr.strip() or 'Falló la consulta de procesos.')
    print(result.stdout,end='')

@tool('localizar-programa','Sistema','Localiza un ejecutable en PATH sin ejecutarlo.',arg('programa'))
def which(a):
    import shutil
    return {'programa':a.programa,'ruta':shutil.which(a.programa)}

@tool('markdown-a-html','Documentos','Convierte un subconjunto de Markdown a HTML estático escapado.',arg('origen'),arg('destino'))
def markdown(a):
    import html,re
    parts=['<!doctype html><meta charset="utf-8"><title>Documento</title><style>body{font:18px system-ui;max-width:850px;margin:3rem auto;line-height:1.6}pre{overflow:auto;background:#eee;padding:1rem}</style>']
    code=False
    for line in read(a.origen).splitlines():
        if line.startswith('```'):
            parts.append('</code></pre>' if code else '<pre><code>')
            code=not code
        elif code:
            parts.append(html.escape(line)+'\n')
        else:
            heading=re.match(r'^(#{1,6})\s+(.*)',line)
            if heading:
                n=len(heading[1]); parts.append(f'<h{n}>'+html.escape(heading[2])+f'</h{n}>')
            elif line.strip():
                parts.append('<p>'+html.escape(line)+'</p>')
    if code:
        parts.append('</code></pre>')
    write(a.destino,'\n'.join(parts))

@tool('escapar-html','Documentos','Escapa texto para mostrarlo como HTML sin interpretarlo.',arg('origen'),arg('destino'))
def escape_html(a):
    import html
    write(a.destino,html.escape(read(a.origen),quote=True))

@tool('html-a-texto','Documentos','Extrae texto de HTML local omitiendo scripts y estilos.',arg('origen'),arg('destino'))
def html_text(a):
    from html.parser import HTMLParser
    class Extractor(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.hidden=0
            self.parts=[]
        def handle_starttag(self,tag,attrs):
            if tag in ('script','style'):
                self.hidden+=1
            if not self.hidden and tag in ('p','div','br','li','h1','h2','h3','tr'):
                self.parts.append('\n')
        def handle_endtag(self,tag):
            if tag in ('script','style') and self.hidden:
                self.hidden-=1
            elif not self.hidden and tag in ('p','div','li','h1','h2','h3','tr'):
                self.parts.append('\n')
        def handle_data(self,data):
            if not self.hidden:
                self.parts.append(data)
    parser=Extractor()
    parser.feed(read(a.origen)); parser.close()
    write(a.destino,''.join(parser.parts).strip()+'\n')

@tool('convertir-codificacion','Documentos','Convierte texto desde una codificación explícita a UTF-8 estricto.',arg('origen'),arg('destino'),arg('--desde',default='cp1252'))
def encoding(a):
    import codecs
    try:
        codecs.lookup(a.desde)
    except LookupError:
        raise ValueError('Codificación desconocida.')
    text=Path(a.origen).read_bytes().decode(a.desde,errors='strict')
    write(a.destino,text)

@tool('manifiesto-sha256','Documentos','Crea manifiesto JSON de rutas relativas, tamaños y SHA-256.',arg('origen'),arg('destino'))
def manifest(a):
    root=Path(a.origen)
    entries=[{'ruta':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files(root)]
    write_json(a.destino,{'version':1,'archivos':entries})

@tool('verificar-manifiesto','Documentos','Verifica un manifiesto SHA-256 y rechaza rutas fuera del origen.',arg('origen'),arg('manifiesto'))
def verify(a):
    import re
    root=Path(a.origen).resolve(strict=True)
    data=load_json(a.manifiesto)
    if not isinstance(data,dict) or data.get('version')!=1 or not isinstance(data.get('archivos'),list):
        raise ValueError('Manifiesto inválido.')
    errors=[]
    for row in data['archivos']:
        if not isinstance(row,dict) or not isinstance(row.get('ruta'),str) or not re.fullmatch(r'[0-9a-f]{64}',str(row.get('sha256',''))):
            raise ValueError('Entrada inválida.')
        path=(root/row['ruta']).resolve()
        if path==root or root not in path.parents:
            raise ValueError('El manifiesto intenta salir del origen.')
        try:
            if path.stat().st_size!=row['bytes'] or digest(path)!=row['sha256']:
                errors.append(row['ruta'])
        except OSError:
            errors.append(row['ruta'])
    if errors:
        raise ValueError('Archivos ausentes o distintos: '+', '.join(errors))
    return {'verificado':True,'archivos':len(data['archivos'])}
