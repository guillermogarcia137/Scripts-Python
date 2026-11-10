"""Registro y utilidades compartidas. Solo biblioteca estándar."""
import argparse
import csv
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path
import stat
import sys

TOOLS = {}

def arg(name, **kwargs):
    return ((name,), kwargs)

def tool(name, category, description, *arguments):
    def decorate(function):
        if name in TOOLS:
            raise ValueError('Nombre de herramienta repetido: '+name)
        TOOLS[name] = (category, description, arguments, function)
        return function
    return decorate

def read(path):
    return Path(path).read_text(encoding='utf-8-sig')

def write(path, content):
    with Path(path).open('x',encoding='utf-8',newline='') as stream:
        stream.write(content)

def dump(value):
    print(json.dumps(value,ensure_ascii=False,indent=2,default=str,allow_nan=False))

def load_json(path):
    def reject_constant(value):
        raise ValueError('Constante no válida en JSON: '+value)
    return json.loads(read(path),parse_constant=reject_constant)

def write_json(path, value):
    write(path,json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def linked(path):
    info=path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info,'st_file_attributes',0)&0x400)

def files(root):
    root=Path(root)
    if not root.is_dir() or linked(root):
        raise ValueError('El origen debe ser una carpeta sin enlace.')
    def fail(error):
        raise error
    for base, dirs, names in os.walk(root,followlinks=False,onerror=fail):
        dirs[:]=sorted(n for n in dirs if not linked(Path(base)/n))
        for name in sorted(names):
            path=Path(base)/name
            if not linked(path) and path.is_file():
                yield path

def table(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        headers=reader.fieldnames
        if not headers or len(set(headers))!=len(headers):
            raise ValueError('CSV sin cabecera o con columnas repetidas.')
        rows=list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            raise ValueError('CSV con filas de longitud irregular.')
    return headers,rows

def write_table(path,headers,rows):
    with Path(path).open('x',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def positive(value):
    value=int(value)
    if value<1:
        raise argparse.ArgumentTypeError('Debe ser mayor que cero.')
    return value

def main(selected=None):
    from . import archivos, texto, datos, desarrollo, productividad, red_sistema
    parser=argparse.ArgumentParser(description='Scripts-Python: herramientas independientes con un núcleo común.')
    if selected is None:
        sub=parser.add_subparsers(dest='comando',required=True)
        for name,(category,description,arguments,function) in sorted(TOOLS.items()):
            p=sub.add_parser(name,help=description,description=description)
            for flags,kwargs in arguments:
                p.add_argument(*flags,**kwargs)
        args=parser.parse_args()
        selected=args.comando
    else:
        category,description,arguments,function=TOOLS[selected]
        parser.description=description
        for flags,kwargs in arguments:
            parser.add_argument(*flags,**kwargs)
        args=parser.parse_args()
    try:
        result=TOOLS[selected][3](args)
        if result is not None:
            dump(result)
    except (OSError,ValueError,KeyError,csv.Error,re.error,zipfile.BadZipFile,EOFError) as exc:
        parser.exit(1,f'Error: {exc}\n')
    except KeyboardInterrupt:
        parser.exit(130,'Cancelado.\n')
