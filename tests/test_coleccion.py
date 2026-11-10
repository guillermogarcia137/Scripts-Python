"""Pruebas de contratos observables, colisiones y resultados, sin cambiar Windows."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from nucleo import main, TOOLS, archivos, texto, datos, desarrollo, productividad, red_sistema

def run(name,*args):
    output=io.StringIO()
    with patch.object(sys,'argv',[name,*map(str,args)]),contextlib.redirect_stdout(output):
        main(name)
    return output.getvalue()

def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/name/'script.py')
    value=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

class CatalogTests(unittest.TestCase):
    def test_exactly_100_documented_tools_and_all_help(self):
        catalog=json.loads((ROOT/'catalogo.json').read_text(encoding='utf-8'))
        self.assertEqual(len(catalog),100)
        self.assertEqual(len({item['nombre'] for item in catalog}),100)
        for item in catalog:
            name=item['nombre']
            with self.subTest(name=name):
                self.assertTrue((ROOT/name/'README.md').is_file())
                result=subprocess.run([sys.executable,str(ROOT/name/'script.py'),'--help'],capture_output=True,timeout=20)
                self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))

    def test_documented_general_examples(self):
        # Todos los ejemplos no interactivos/offline se ejecutan en una copia desechable.
        excluded={'servidor-local','pomodoro','comprobar-tcp','cabeceras-http','certificado-tls','resolver-dns'}
        for name in sorted(TOOLS.keys()-excluded):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                shutil.copytree(ROOT/'ejemplos',root/'ejemplos')
                shutil.copy(ROOT/'README.md',root/'README.md')
                shutil.copy(ROOT/'requirements.txt',root/'requirements.txt')
                line=next(l for l in (ROOT/name/'README.md').read_text(encoding='utf-8').splitlines() if l.startswith('py cli.py '))
                args=shlex.split(line)[3:]
                previous=Path.cwd()
                os.chdir(root)
                try:
                    if name in ('listar-zip','comprobar-zip'):
                        run('copia-zip','ejemplos/datos','copia.zip')
                    if name=='unir-archivo':
                        run('dividir-archivo','ejemplos/datos/notas.txt','partes','--mb','1')
                    if name=='verificar-manifiesto':
                        run('manifiesto-sha256','ejemplos/datos','manifiesto.json')
                    run(name,*args)
                finally:
                    os.chdir(previous)

class IntegrityTests(unittest.TestCase):
    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); src=root/'in.txt'; dst=root/'out.txt'
            src.write_text('hola'); dst.write_text('no tocar')
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as error:
                run('reemplazar-texto',src,dst,'hola','otro')
            self.assertEqual(error.exception.code,1)
            self.assertEqual(dst.read_text(),'no tocar')

    def test_split_join_roundtrip_and_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); src=root/'input.bin'; parts=root/'partes'
            payload=bytes(range(256))*9000
            src.write_bytes(payload)
            run('dividir-archivo',src,parts,'--mb','1')
            run('unir-archivo',parts/'manifiesto.json',root/'joined.bin')
            self.assertEqual((root/'joined.bin').read_bytes(),payload)
            (parts/'parte-000000.bin').write_bytes(b'alterado')
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                run('unir-archivo',parts/'manifiesto.json',root/'bad.bin')
            self.assertFalse((root/'bad.bin').exists())

    def test_manifest_rejects_outside_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); source=root/'source';source.mkdir()
            manifest=root/'m.json'
            manifest.write_text(json.dumps({'version':1,'archivos':[{'ruta':'../fuera','sha256':'0'*64,'bytes':0}]}))
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                run('verificar-manifiesto',source,manifest)

    def test_csv_numeric_sort_and_budget_precision(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); src=root/'data.csv';dst=root/'sorted.csv'
            src.write_text('n\n10\n2\n')
            run('ordenar-csv',src,dst,'n','--numerico')
            from nucleo import table
            self.assertEqual([r['n'] for r in table(dst)[1]],['2','10'])
            src.write_text('categoria,importe\nA,0.10\nA,0.20\n')
            self.assertEqual(json.loads(run('resumen-gastos',src))['total'],'0.30')

    def test_zip_and_duplicates_preserve_content(self):
        import zipfile
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';source.mkdir()
            (source/'a').write_bytes(b'igual');(source/'b').write_bytes(b'igual')
            run('copia-zip',source,root/'copy.zip')
            with zipfile.ZipFile(root/'copy.zip') as archive:
                self.assertEqual(archive.read('a'),b'igual')
            self.assertEqual(len(json.loads(run('buscar-duplicados',source))),1)
            self.assertEqual(len(list(source.iterdir())),2)

    def test_html_is_escaped_and_scripts_omitted(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);src=root/'src';dst=root/'dst'
            src.write_text('# <script>alert(1)</script>')
            run('markdown-a-html',src,dst)
            self.assertNotIn('<script>',dst.read_text())
            src.write_text('<p>Visible</p><script>secret()</script><style>hidden</style>')
            run('html-a-texto',src,root/'plain')
            self.assertEqual((root/'plain').read_text().strip(),'Visible')

    def test_invalid_regex_zip_and_json_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'bad.txt'
            source.write_text('NaN')
            for name,args in [('buscar-regex',[source,'[']),
                              ('listar-zip',[source]),
                              ('formatear-json',[source,Path(temp)/'out.json'])]:
                with self.subTest(name=name),contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as error:
                    run(name,*args)
                self.assertEqual(error.exception.code,1)

    def test_local_tcp_http_and_dns(self):
        from functools import partial
        from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self,*args):
                pass
        with tempfile.TemporaryDirectory() as temp:
            Path(temp,'index.html').write_text('local')
            server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=temp))
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                port=server.server_address[1]
                self.assertTrue(json.loads(run('comprobar-tcp','127.0.0.1',port))['conectado'])
                self.assertEqual(json.loads(run('cabeceras-http',f'http://127.0.0.1:{port}'))['estado'],200)
                self.assertTrue(json.loads(run('resolver-dns','localhost')))
            finally:
                server.shutdown();server.server_close();thread.join()

class DesignTests(unittest.TestCase):
    def test_svg_xml_dimensions_and_text_escaping(self):
        names=[p.name for p in ROOT.iterdir() if p.is_dir() and p.name.endswith('-svg')]
        self.assertEqual(len(names),8)
        for name in names:
            with self.subTest(name=name):
                svg=module(name).render(800,450,'#10152E','#46C9B5','<script>&',11)
                xml=ET.fromstring(svg)
                self.assertEqual(xml.attrib['width'],'800')
                self.assertEqual(xml.attrib['height'],'450')
                self.assertNotIn('<script>',svg)

    def test_contrast_reference_values(self):
        contrast=module('contraste-colores').contrast
        self.assertAlmostEqual(contrast('#000000','#FFFFFF'),21)
        self.assertAlmostEqual(contrast('#ABCDEF','#ABCDEF'),1)

    def test_png_ico_crop_palette_and_collage(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source.png'
            Image.new('RGB',(400,200),(255,0,0)).save(source)
            cases=[('fondo-degradado-png',[str(root/'gradient.png'),'--ancho','320','--alto','180']),
                   ('fondo-desenfocado',[str(source),str(root/'blur.png'),'--ancho','320','--alto','180']),
                   ('avatar-cuadrado',[str(source),str(root/'avatar.png'),'--lado','128']),
                   ('imagen-a-ico',[str(source),str(root/'icon.ico')]),
                   ('hoja-contacto',[str(root),str(root/'contact.png'),'--columnas','2']),
                   ('paleta-desde-imagen',[str(source)])]
            for name,args in cases:
                result=subprocess.run([sys.executable,str(ROOT/name/'script.py'),*args],capture_output=True,timeout=20)
                self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
                if name=='paleta-desde-imagen':
                    self.assertEqual(json.loads(result.stdout)[0]['hex'],'#FF0000')
            with Image.open(root/'avatar.png') as image:
                self.assertEqual(image.size,(128,128))
            with Image.open(root/'icon.ico') as image:
                self.assertEqual(len(image.ico.sizes()),7)
            before=(root/'gradient.png').read_bytes()
            result=subprocess.run([sys.executable,str(ROOT/'fondo-degradado-png/script.py'),str(root/'gradient.png')],capture_output=True,timeout=20)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual((root/'gradient.png').read_bytes(),before)

if __name__=='__main__':
    unittest.main()
