"""Fondo con zonas para organizar iconos."""
import argparse
import math
import random
import re
from html import escape
from pathlib import Path

def color(value):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise argparse.ArgumentTypeError('Usa #RRGGBB entre comillas.')
    return value

def dimension(value):
    number = int(value)
    if not 64 <= number <= 7680:
        raise argparse.ArgumentTypeError('Dimensión entre 64 y 7680.')
    return number

def render(width, height, primary, secondary, text, seed):
    w, h = width, height
    rng = random.Random(seed)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    parts.append(f'<rect width="{w}" height="{h}" fill="{primary}"/>')
    for i,label in enumerate(('TRABAJO','PERSONAL','TEMPORAL')):
        x = w*(.035+i*.325)
        parts.append(f'<rect x="{x}" y="{h*.12}" width="{w*.29}" height="{h*.76}" rx="{h*.025}" fill="{secondary}" fill-opacity=".05" stroke="{secondary}" stroke-opacity=".35"/>')
        parts.append(f'<text x="{x+w*.018}" y="{h*.09}" font-family="Segoe UI,sans-serif" font-size="{h*.021}" letter-spacing="3" fill="{secondary}">{label}</text>')
    parts.append('</svg>')
    return '\n'.join(parts)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destino', type=Path)
    parser.add_argument('--ancho', type=dimension, default=1920)
    parser.add_argument('--alto', type=dimension, default=1080)
    parser.add_argument('--primario', type=color, default='#0B1026')
    parser.add_argument('--secundario', type=color, default='#56DCC6')
    parser.add_argument('--texto', default='NOVA')
    parser.add_argument('--semilla', type=int, default=11)
    args = parser.parse_args()
    if args.destino.suffix.lower() != '.svg':
        parser.error('El destino debe ser .svg.')
    content = render(args.ancho, args.alto, args.primario, args.secundario, args.texto, args.semilla)
    with args.destino.open('x', encoding='utf-8') as output:
        output.write(content)
    print(args.destino)

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
