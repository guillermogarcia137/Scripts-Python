"""Transformaciones explícitas en archivos UTF-8 nuevos."""
from . import *
import re
import collections
SRC=arg('origen')
DST=arg('destino')

@tool('contar-lineas','Texto','Cuenta líneas, líneas vacías y caracteres.',SRC)
def line_count(a):
    text=read(a.origen)
    lines=text.splitlines()
    return {'lineas':len(lines),'vacias':sum(not l.strip() for l in lines),'caracteres':len(text)}

@tool('frecuencia-palabras','Texto','Frecuencias de palabras Unicode.',SRC,arg('--cantidad',type=positive,default=30))
def words(a):
    return collections.Counter(re.findall(r'\b\w+\b',read(a.origen).casefold())).most_common(a.cantidad)

@tool('quitar-lineas-repetidas','Texto','Elimina líneas repetidas conservando su primer orden.',SRC,DST)
def dedupe(a):
    write(a.destino,'\n'.join(dict.fromkeys(read(a.origen).splitlines()))+'\n')

@tool('ordenar-lineas','Texto','Ordena líneas alfabéticamente sin distinguir mayúsculas.',SRC,DST,arg('--inverso',action='store_true'))
def sort_lines(a):
    write(a.destino,'\n'.join(sorted(read(a.origen).splitlines(),key=str.casefold,reverse=a.inverso))+'\n')

@tool('buscar-regex','Texto','Busca un patrón en un archivo local con números de línea.',SRC,arg('patron'))
def search(a):
    regex=re.compile(a.patron)
    return [{'linea':i,'texto':line} for i,line in enumerate(read(a.origen).splitlines(),1) if regex.search(line)]

@tool('reemplazar-texto','Texto','Reemplaza texto literal y guarda una copia nueva.',SRC,DST,arg('buscar'),arg('reemplazo'))
def replace(a):
    if not a.buscar:
        raise ValueError('El texto buscado no puede estar vacío.')
    text=read(a.origen)
    result=text.replace(a.buscar,a.reemplazo)
    write(a.destino,result)
    return {'reemplazos':text.count(a.buscar)}

@tool('normalizar-espacios','Texto','Quita espacios finales y compacta espacios horizontales.',SRC,DST)
def whitespace(a):
    write(a.destino,'\n'.join(re.sub(r'[ \t]+',' ',line).rstrip() for line in read(a.origen).splitlines())+'\n')

@tool('numerar-lineas','Texto','Crea una copia de texto con números de línea.',SRC,DST)
def number(a):
    write(a.destino,'\n'.join(f'{i:5d}  {line}' for i,line in enumerate(read(a.origen).splitlines(),1))+'\n')

@tool('unir-textos','Texto','Une archivos UTF-8 en el orden indicado.',DST,arg('archivos',nargs='+'))
def merge(a):
    content='\n'.join(read(p) for p in a.archivos)
    write(a.destino,content)

@tool('diferencias-texto','Texto','Diferencias unificadas entre dos archivos UTF-8.',arg('izquierda'),arg('derecha'))
def diff(a):
    import difflib
    print(''.join(difflib.unified_diff(read(a.izquierda).splitlines(True),read(a.derecha).splitlines(True),fromfile=a.izquierda,tofile=a.derecha)),end='')

@tool('extraer-emails','Texto','Extrae candidatos de correo de texto local; no valida buzones.',SRC)
def emails(a):
    return sorted(set(re.findall(r'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+',read(a.origen))))

@tool('extraer-enlaces','Texto','Extrae candidatos HTTP/HTTPS sin abrirlos.',SRC)
def urls(a):
    return sorted(set(url.rstrip('.,;!?)') for url in re.findall(r'https?://[^\s<>"\x27]+',read(a.origen))))

@tool('crear-slug','Texto','Convierte un título en slug ASCII para nombres o URLs.',arg('texto'))
def slug(a):
    import unicodedata
    text=unicodedata.normalize('NFKD',a.texto).encode('ascii','ignore').decode().lower()
    return {'slug':re.sub(r'[^a-z0-9]+','-',text).strip('-')}

@tool('ajustar-parrafos','Texto','Reajusta el ancho de párrafos conservando separaciones vacías.',SRC,DST,arg('--ancho',type=positive,default=80))
def wrap(a):
    import textwrap
    paragraphs=re.split(r'\n\s*\n',read(a.origen))
    write(a.destino,'\n\n'.join(textwrap.fill(' '.join(p.split()),width=a.ancho) for p in paragraphs)+'\n')
