"""Crear un fondo desenfocado desde una foto."""
import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageDraw

def save_new(image, destination, fmt='PNG', **options):
    destination = Path(destination)
    expected = '.ico' if fmt == 'ICO' else '.png'
    if destination.suffix.lower() != expected:
        raise ValueError(f'Usa un destino {expected}.')
    # Exclusivo; no abre ni sobrescribe un archivo anterior.
    with destination.open('xb') as stream:
        image.save(stream, format=fmt, **options)

def load_image(path):
    with Image.open(path) as original:
        if original.width*original.height > 40_000_000:
            raise ValueError('La imagen supera 40 megapíxeles.')
        return ImageOps.exif_transpose(original).convert('RGB')

def size(value):
    value = int(value)
    if not 64 <= value <= 7680:
        raise argparse.ArgumentTypeError('Dimensión entre 64 y 7680.')
    return value

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('origen',type=Path)
    parser.add_argument('destino',type=Path)
    parser.add_argument('--ancho',type=size,default=1920)
    parser.add_argument('--alto',type=size,default=1080)
    parser.add_argument('--radio',type=int,choices=range(1,101),default=35,metavar='1..100')
    args=parser.parse_args()
    if args.ancho*args.alto>40_000_000:
        parser.error('Máximo 40 megapíxeles.')
    image=ImageOps.fit(load_image(args.origen),(args.ancho,args.alto),method=Image.Resampling.LANCZOS)
    save_new(image.filter(ImageFilter.GaussianBlur(args.radio)),args.destino)

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
