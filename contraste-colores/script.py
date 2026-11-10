"""Comprobar contraste de texto."""
import argparse
import json
import re

def luminance(color):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        raise ValueError('Usa colores #RRGGBB.')
    channels = [int(color[i:i+2], 16)/255 for i in (1,3,5)]
    linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in channels]
    return sum(v*w for v,w in zip(linear,(.2126,.7152,.0722)))

def contrast(a,b):
    low,high = sorted((luminance(a),luminance(b)))
    return (high+.05)/(low+.05)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('texto')
    parser.add_argument('fondo')
    args = parser.parse_args()
    ratio = contrast(args.texto,args.fondo)
    print(json.dumps({'ratio':round(ratio,3), 'AA_normal':ratio>=4.5,
                      'AA_grande':ratio>=3, 'AAA_normal':ratio>=7}, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
