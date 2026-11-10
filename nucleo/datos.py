"""Datos JSON, CSV y XML; ninguna conversión ejecuta contenido."""
from . import *
SRC=arg('origen')
DST=arg('destino')
COL=arg('columna')

@tool('formatear-json','Datos','Valida y formatea JSON en un archivo nuevo.',SRC,DST)
def pretty(a):
    write_json(a.destino,load_json(a.origen))

@tool('aplanar-json','Datos','Lista hojas JSON con rutas JSON Pointer y valores.',SRC,DST)
def flatten(a):
    result=[]
    def visit(value,path):
        if isinstance(value,dict) and value:
            for k,v in value.items():
                visit(v,path+'/'+k.replace('~','~0').replace('/','~1'))
        elif isinstance(value,list) and value:
            for i,v in enumerate(value):
                visit(v,path+'/'+str(i))
        else:
            result.append({'ruta':path,'valor':value})
    visit(load_json(a.origen),'')
    write_json(a.destino,result)

@tool('json-a-csv','Datos','Convierte una lista de objetos planos JSON en CSV.',SRC,DST)
def json_csv(a):
    rows=load_json(a.origen)
    if not isinstance(rows,list) or not rows or any(not isinstance(row,dict) for row in rows):
        raise ValueError('Se necesita una lista no vacía de objetos.')
    headers=list(dict.fromkeys(k for row in rows for k in row))
    if any(isinstance(v,(dict,list)) for row in rows for v in row.values()):
        raise ValueError('Solo se admiten valores planos.')
    write_table(a.destino,headers,rows)

@tool('csv-a-json','Datos','Convierte CSV con cabecera a una lista JSON de cadenas.',SRC,DST)
def csv_json(a):
    headers,rows=table(a.origen)
    write_json(a.destino,rows)

@tool('seleccionar-csv','Datos','Selecciona columnas de un CSV en el orden pedido.',SRC,DST,arg('columnas',nargs='+'))
def select(a):
    headers,rows=table(a.origen)
    if len(set(a.columnas))!=len(a.columnas) or any(c not in headers for c in a.columnas):
        raise ValueError('Columnas inexistentes o repetidas.')
    write_table(a.destino,a.columnas,[{k:row[k] for k in a.columnas} for row in rows])

@tool('filtrar-csv','Datos','Filtra CSV por igualdad literal en una columna.',SRC,DST,COL,arg('valor'))
def filter_csv(a):
    headers,rows=table(a.origen)
    if a.columna not in headers:
        raise ValueError('Columna inexistente.')
    write_table(a.destino,headers,[r for r in rows if r[a.columna]==a.valor])

@tool('ordenar-csv','Datos','Ordena CSV por columna, alfabéticamente o como decimal.',SRC,DST,COL,arg('--numerico',action='store_true'))
def sort_csv(a):
    from decimal import Decimal,InvalidOperation
    headers,rows=table(a.origen)
    if a.columna not in headers:
        raise ValueError('Columna inexistente.')
    def key(row):
        if not a.numerico:
            return row[a.columna].casefold()
        try:
            value=Decimal(row[a.columna])
            if not value.is_finite():
                raise ValueError('Solo se admiten números finitos.')
            return value
        except InvalidOperation:
            raise ValueError('Valor no numérico en la columna.')
    ordered=sorted(rows,key=key)
    write_table(a.destino,headers,ordered)

@tool('estadisticas-csv','Datos','Estadísticas de una columna numérica; rechaza valores vacíos.',SRC,COL)
def stats(a):
    import statistics,math
    headers,rows=table(a.origen)
    if a.columna not in headers or not rows:
        raise ValueError('Columna inexistente o CSV sin datos.')
    values=[float(r[a.columna]) for r in rows]
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Solo se admiten números finitos.')
    return {'cantidad':len(values),'suma':math.fsum(values),'media':statistics.mean(values),'mediana':statistics.median(values),'minimo':min(values),'maximo':max(values)}

@tool('transponer-csv','Datos','Transpone filas y columnas de una matriz CSV rectangular.',SRC,DST)
def transpose(a):
    with Path(a.origen).open(encoding='utf-8-sig',newline='') as stream:
        rows=list(csv.reader(stream))
    if not rows or any(len(row)!=len(rows[0]) for row in rows):
        raise ValueError('Se necesita una matriz CSV rectangular.')
    with Path(a.destino).open('x',encoding='utf-8-sig',newline='') as stream:
        csv.writer(stream).writerows(zip(*rows))

@tool('detectar-delimitador','Datos','Estima el delimitador de un archivo tabular.',SRC)
def delimiter(a):
    with Path(a.origen).open(encoding='utf-8-sig') as stream:
        sample=stream.read(65536)
    dialect=csv.Sniffer().sniff(sample,delimiters=',;\t|')
    return {'delimitador':dialect.delimiter,'comillas':dialect.quotechar}

@tool('comparar-json','Datos','Compara estructuras JSON ignorando el orden de claves.',arg('izquierda'),arg('derecha'))
def compare_json(a):
    # Canonicalizar evita equiparar True y 1 por igualdad de Python.
    left=json.dumps(load_json(a.izquierda),sort_keys=True,ensure_ascii=False)
    right=json.dumps(load_json(a.derecha),sort_keys=True,ensure_ascii=False)
    return {'iguales':left==right}

@tool('fusionar-json','Datos','Fusiona objetos JSON de primer nivel; rechaza claves repetidas.',DST,arg('archivos',nargs='+'))
def merge_json(a):
    result={}
    for name in a.archivos:
        value=load_json(name)
        if not isinstance(value,dict):
            raise ValueError('Cada archivo debe contener un objeto.')
        overlap=result.keys()&value.keys()
        if overlap:
            raise ValueError('Claves repetidas: '+', '.join(sorted(overlap)))
        result.update(value)
    write_json(a.destino,result)

@tool('ndjson-a-json','Datos','Convierte JSON por línea a un array JSON; omite líneas vacías.',SRC,DST)
def ndjson(a):
    write_json(a.destino,[json.loads(line) for line in read(a.origen).splitlines() if line.strip()])

@tool('inventario-xml','Datos','Lista frecuencias de etiquetas en XML local sin DTD.',SRC)
def xml_inventory(a):
    import collections
    import xml.etree.ElementTree as ET
    text=read(a.origen)
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('No se admiten DTD ni entidades personalizadas.')
    try:
        return dict(collections.Counter(e.tag for e in ET.fromstring(text).iter()))
    except ET.ParseError as exc:
        raise ValueError(str(exc))
