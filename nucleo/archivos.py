"""Operaciones de archivos: las salidas se crean sin sobrescribir."""
from . import *
import zipfile

SRC=arg('origen')
DST=arg('destino')

@tool('inventario-archivos','Archivos','Inventario recursivo CSV con tamaños y fechas UTC.',SRC,DST)
def inventory(a):
    from datetime import datetime,timezone
    root=Path(a.origen)
    rows=[{'ruta':str(p.relative_to(root)),'bytes':p.stat().st_size,'modificado_utc':datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat()} for p in files(root)]
    write_table(a.destino,['ruta','bytes','modificado_utc'],rows)

@tool('hash-archivo','Archivos','Huella SHA-256 de un archivo.',SRC)
def file_hash(a):
    return {'archivo':a.origen,'sha256':digest(a.origen)}

@tool('comparar-carpetas','Archivos','Comparación recursiva por ruta relativa y contenido SHA-256.',arg('izquierda'),arg('derecha'))
def compare(a):
    def index(root):
        return {str(p.relative_to(root)):digest(p) for p in files(root)}
    left,right=index(Path(a.izquierda)),index(Path(a.derecha))
    return [{'ruta':n,'estado':'solo_derecha' if n not in left else 'solo_izquierda' if n not in right else 'igual' if left[n]==right[n] else 'diferente'} for n in sorted(left.keys()|right.keys())]

@tool('buscar-duplicados','Archivos','Duplicados SHA-256; nunca elimina datos.',SRC)
def duplicates(a):
    groups={}
    for p in files(a.origen):
        groups.setdefault(digest(p),[]).append(str(p))
    return [{'sha256':h,'archivos':ps} for h,ps in groups.items() if len(ps)>1]

@tool('copia-zip','Archivos','ZIP nuevo fuera del origen; omite enlaces.',SRC,DST)
def backup(a):
    source=Path(a.origen).resolve(strict=True)
    dest=Path(a.destino).resolve()
    if dest==source or source in dest.parents or dest.suffix.lower()!='.zip':
        raise ValueError('Usa un ZIP nuevo fuera del origen.')
    # Valida y obtiene las rutas antes de abrir el ZIP.
    paths=list(files(source))
    with dest.open('xb') as output:
        try:
            with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
                for p in paths:
                    archive.write(p,p.relative_to(source))
        except BaseException:
            output.close()
            dest.unlink()
            raise

@tool('listar-zip','Archivos','Lista contenido de un ZIP sin extraerlo.',SRC)
def zip_list(a):
    with zipfile.ZipFile(a.origen) as archive:
        return [{'nombre':i.filename,'bytes':i.file_size,'comprimidos':i.compress_size} for i in archive.infolist()]

@tool('comprobar-zip','Archivos','Comprueba CRC de un ZIP sin extraer archivos.',SRC)
def zip_verify(a):
    with zipfile.ZipFile(a.origen) as archive:
        bad=archive.testzip()
        if bad:
            raise ValueError('CRC incorrecto: '+bad)
    return {'valido':True}

@tool('dividir-archivo','Archivos','Divide en partes y genera manifiesto SHA-256 en carpeta nueva.',SRC,DST,arg('--mb',type=positive,default=10))
def split(a):
    source=Path(a.origen)
    if not source.is_file():
        raise ValueError('Indica un archivo de origen.')
    target=Path(a.destino)
    target.mkdir()
    parts=[]
    size=a.mb*1024*1024
    # Copia en bloques pequeños incluso con un tamaño de parte alto.
    with source.open('rb') as stream:
        i=0
        while True:
            data=stream.read(min(size,1024*1024))
            if not data:
                break
            name=f'parte-{i:06d}.bin'
            with (target/name).open('xb') as output:
                remaining=size
                while data:
                    output.write(data)
                    remaining-=len(data)
                    if remaining==0:
                        break
                    data=stream.read(min(remaining,1024*1024))
            parts.append({'nombre':name,'sha256':digest(target/name)})
            i+=1
    write_json(target/'manifiesto.json',{'version':1,'partes':parts})
    return {'partes':len(parts),'carpeta':str(target)}

@tool('unir-archivo','Archivos','Une partes verificadas; elimina salida parcial si falla.',arg('manifiesto'),DST)
def join(a):
    import re
    manifest=Path(a.manifiesto)
    data=load_json(manifest)
    if not isinstance(data,dict) or data.get('version')!=1 or not isinstance(data.get('partes'),list):
        raise ValueError('Manifiesto inválido.')
    parts=[]
    for entry in data['partes']:
        if not isinstance(entry,dict) or not isinstance(entry.get('nombre'),str) or not re.fullmatch(r'parte-\d{6}\.bin',entry['nombre']):
            raise ValueError('Nombre de parte inválido.')
        p=manifest.parent/entry['nombre']
        if linked(p) or digest(p)!=entry['sha256']:
            raise ValueError('Parte modificada: '+p.name)
        parts.append(p)
    import shutil
    target=Path(a.destino)
    with target.open('xb') as output:
        try:
            for p in parts:
                with p.open('rb') as stream:
                    shutil.copyfileobj(stream,output)
        except BaseException:
            output.close()
            target.unlink()
            raise

@tool('buscar-extension','Archivos','Busca archivos recursivamente por extensión.',SRC,arg('extension'))
def extension(a):
    ext=a.extension if a.extension.startswith('.') else '.'+a.extension
    return [str(p) for p in files(a.origen) if p.suffix.casefold()==ext.casefold()]

@tool('archivos-grandes','Archivos','Los archivos de mayor tamaño, sin borrar.',SRC,arg('--cantidad',type=positive,default=20))
def largest(a):
    import heapq
    rows=({'ruta':str(p),'bytes':p.stat().st_size} for p in files(a.origen))
    return heapq.nlargest(a.cantidad,rows,key=lambda row:row['bytes'])

@tool('carpetas-vacias','Archivos','Informa carpetas vacías, sin eliminarlas.',SRC)
def empty_dirs(a):
    root=Path(a.origen)
    if not root.is_dir():
        raise ValueError('Indica una carpeta.')
    result=[]
    for base,dirs,names in os.walk(root,followlinks=False,onerror=lambda e: (_ for _ in ()).throw(e)):
        dirs[:]=[n for n in dirs if not linked(Path(base)/n)]
        if not list(Path(base).iterdir()):
            result.append(base)
    return result

@tool('arbol-archivos','Archivos','Árbol de rutas relativas; omite enlaces y limita la salida.',SRC,arg('--limite',type=positive,default=500))
def tree(a):
    import itertools
    root=Path(a.origen)
    return [p.relative_to(root).as_posix() for p in itertools.islice(files(root),a.limite)]

@tool('firma-archivo','Archivos','Identifica firmas comunes sin confiar en la extensión.',SRC)
def magic(a):
    with Path(a.origen).open('rb') as f:
        data=f.read(16)
    signatures=[(b'\x89PNG\r\n\x1a\n','PNG'),(b'\xff\xd8\xff','JPEG'),(b'%PDF-','PDF'),(b'PK\x03\x04','ZIP o formato basado en ZIP'),(b'GIF8','GIF'),(b'MZ','Ejecutable DOS/Windows')]
    return {'tipo':next((name for sig,name in signatures if data.startswith(sig)),'desconocido'),'cabecera_hex':data.hex()}
