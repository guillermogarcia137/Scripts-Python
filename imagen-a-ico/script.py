"""Crear iconos ICO multirresolución."""
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
    args=parser.parse_args()
    with Image.open(args.origen) as original:
        if original.width*original.height>40_000_000:
            parser.error('Máximo 40 megapíxeles.')
        image=ImageOps.exif_transpose(original).convert('RGBA')
    image=ImageOps.contain(image,(256,256),method=Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(256,256),(0,0,0,0))
    canvas.alpha_composite(image,((256-image.width)//2,(256-image.height)//2))
    save_new(canvas,args.destino,'ICO',sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
