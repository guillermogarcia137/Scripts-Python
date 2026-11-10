"""Fondo de órbitas minimalistas."""
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
    for i in range(12):
        radius = h * (.12 + i*.055)
        parts.append(f'<circle cx="{w*.73}" cy="{h*.48}" r="{radius}" fill="none" stroke="{secondary}" stroke-width="{max(1,h/700)}" opacity="{.65-i*.035}"/>')
    parts.append(f'<circle cx="{w*.73}" cy="{h*.48}" r="{h*.055}" fill="{secondary}"/>')
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
