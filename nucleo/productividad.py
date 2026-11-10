"""Notas, organización y pequeños informes sin servicios externos."""
from . import *
from datetime import date
import html

@tool('nota-diaria','Productividad','Crea una nota Markdown del día sin sobrescribir notas previas.',arg('carpeta'))
def note(a):
    path=Path(a.carpeta)/(date.today().isoformat()+'.md')
    write(path,f'# {date.today().isoformat()}\n\n## Prioridades\n- [ ] \n\n## Notas\n\n## Hecho\n')
    return {'nota':str(path)}

@tool('crear-proyecto','Productividad','Crea estructura nueva con documentación, recursos, código y exportaciones.',arg('destino'))
def project(a):
    root=Path(a.destino)
    root.mkdir()
    for name in ('documentos','recursos','src','exportaciones'):
        (root/name).mkdir()
    write(root/'README.md','# Proyecto\n\n## Objetivo\n\n## Tareas\n- [ ] Definir alcance\n')

@tool('pomodoro','Productividad','Temporizador de trabajo y descanso con reloj monotónico.',arg('--trabajo',type=positive,default=25),arg('--descanso',type=positive,default=5),arg('--ciclos',type=positive,default=1))
def pomodoro(a):
    import time
    if a.trabajo>180 or a.descanso>60 or a.ciclos>12:
        raise ValueError('Máximos: trabajo 180, descanso 60, ciclos 12.')
    for i in range(a.ciclos):
        for phase,minutes in [('Trabajo',a.trabajo),('Descanso',a.descanso)]:
            end=time.monotonic()+minutes*60
            print(f'{phase}, ciclo {i+1}/{a.ciclos}: {minutes} minutos',flush=True)
            while time.monotonic()<end:
                time.sleep(min(1,max(0,end-time.monotonic())))
            print('\aFin: '+phase,flush=True)

@tool('checklist-html','Productividad','Convierte una línea por tarea en lista HTML imprimible.',arg('origen'),arg('destino'))
def checklist(a):
    tasks=[html.escape(line.strip()) for line in read(a.origen).splitlines() if line.strip()]
    write(a.destino,'<!doctype html><meta charset="utf-8"><title>Lista de tareas</title><style>body{font:18px system-ui;max-width:760px;margin:3rem auto}li{margin:1rem}input{margin-right:1rem}</style><h1>Tareas</h1><p>Marcas temporales: no se guardan al recargar. Puedes imprimir la lista.</p><ul style="list-style:none">'+''.join('<li><label><input type="checkbox">'+task+'</label></li>' for task in tasks)+'</ul>')

@tool('indice-markdown','Productividad','Lista encabezados Markdown fuera de bloques de código.',arg('origen'))
def toc(a):
    import re
    headings=[]
    fence=None
    for i,line in enumerate(read(a.origen).splitlines(),1):
        stripped=line.lstrip()
        if stripped.startswith(('```','~~~')):
            marker=stripped[:3]
            fence=None if fence==marker else marker if fence is None else fence
            continue
        if fence:
            continue
        match=re.match(r'^(#{1,6})\s+(.+?)\s*#*$',line)
        if match:
            headings.append({'linea':i,'nivel':len(match[1]),'titulo':match[2]})
    return headings

@tool('resumen-horas','Productividad','Suma horas por proyecto desde CSV proyecto,horas.',arg('origen'))
def hours(a):
    from decimal import Decimal,InvalidOperation
    headers,rows=table(a.origen)
    if not {'proyecto','horas'}<=set(headers):
        raise ValueError('Se necesitan columnas proyecto y horas.')
    totals={}
    try:
        for row in rows:
            value=Decimal(row['horas'])
            if not value.is_finite() or value<0:
                raise ValueError('Horas negativas o no finitas.')
            totals[row['proyecto']]=totals.get(row['proyecto'],Decimal(0))+value
    except InvalidOperation:
        raise ValueError('Horas no numéricas; usa punto decimal.')
    return {k:str(v) for k,v in sorted(totals.items())}

@tool('calendario-html','Productividad','Genera un calendario mensual HTML imprimible.',arg('ano',type=int),arg('mes',type=int),arg('destino'))
def calendar_html(a):
    import calendar
    if not 1<=a.ano<=9999 or not 1<=a.mes<=12:
        raise ValueError('Año 1..9999 y mes 1..12.')
    content=calendar.HTMLCalendar(firstweekday=0).formatmonth(a.ano,a.mes)
    write(a.destino,'<!doctype html><meta charset="utf-8"><title>Calendario</title><style>body{font:18px system-ui}table{width:100%;border-collapse:collapse}td,th{border:1px solid #bbb;padding:1rem;text-align:center}td{height:4rem}</style>'+content)

@tool('resumen-tareas','Productividad','Resume tareas de CSV tarea,estado por estado.',arg('origen'))
def tasks(a):
    from collections import Counter
    headers,rows=table(a.origen)
    if not {'tarea','estado'}<=set(headers):
        raise ValueError('Se necesitan columnas tarea y estado.')
    return {'total':len(rows),'por_estado':dict(Counter(row['estado'].strip().casefold() or 'sin estado' for row in rows))}

@tool('convertir-unidades','Productividad','Convierte longitud, masa, almacenamiento o temperatura.',arg('valor',type=float),arg('desde'),arg('hasta'))
def units(a):
    import math
    if not math.isfinite(a.valor):
        raise ValueError('Usa un valor finito.')
    groups=[{'m':1,'km':1000,'cm':.01,'mm':.001,'in':.0254,'ft':.3048},{'kg':1,'g':.001,'lb':.45359237},{'B':1,'KB':1000,'MB':1e6,'GB':1e9,'KiB':1024,'MiB':1024**2,'GiB':1024**3}]
    if a.desde in ('C','F','K') and a.hasta in ('C','F','K'):
        c=a.valor if a.desde=='C' else (a.valor-32)*5/9 if a.desde=='F' else a.valor-273.15
        if c < -273.15:
            raise ValueError('Temperatura inferior al cero absoluto.')
        result=c if a.hasta=='C' else c*9/5+32 if a.hasta=='F' else c+273.15
    else:
        group=next((g for g in groups if a.desde in g and a.hasta in g),None)
        if group is None:
            raise ValueError('Unidades incompatibles. Usa m/km/cm/mm/in/ft, kg/g/lb, B/KB/MB/GB/KiB/MiB/GiB o C/F/K.')
        result=a.valor*group[a.desde]/group[a.hasta]
    return {'valor':result,'unidad':a.hasta}

@tool('resumen-gastos','Productividad','Suma importes CSV categoria,importe con decimales exactos.',arg('origen'))
def budget(a):
    from decimal import Decimal,InvalidOperation
    headers,rows=table(a.origen)
    if not {'categoria','importe'}<=set(headers):
        raise ValueError('Se necesitan columnas categoria e importe.')
    totals={}
    try:
        for row in rows:
            value=Decimal(row['importe'])
            if not value.is_finite():
                raise ValueError('Importe no finito.')
            totals[row['categoria']]=totals.get(row['categoria'],Decimal(0))+value
    except InvalidOperation:
        raise ValueError('Importes no numéricos; usa punto decimal.')
    return {'por_categoria':{k:str(v) for k,v in sorted(totals.items())},'total':str(sum(totals.values(),Decimal(0)))}
