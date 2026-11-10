"""Crear fondo PNG para Windows."""
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
    from PIL import ImageColor
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destino', type=Path)
    parser.add_argument('--ancho', type=size, default=1920)
    parser.add_argument('--alto', type=size, default=1080)
    parser.add_argument('--inicio', default='#10152E')
    parser.add_argument('--fin', default='#46C9B5')
    args = parser.parse_args()
    if args.ancho*args.alto > 40_000_000:
        parser.error('Máximo 40 megapíxeles.')
    a,b = ImageColor.getrgb(args.inicio), ImageColor.getrgb(args.fin)
    if len(a)!=3 or len(b)!=3:
        parser.error('Usa colores RGB sin transparencia.')
    image = Image.new('RGB',(args.ancho,args.alto))
    draw = ImageDraw.Draw(image)
    for y in range(args.alto):
        t=y/(args.alto-1)
        color=tuple(round(x*(1-t)+z*t) for x,z in zip(a,b))
        draw.line((0,y,args.ancho,y), fill=color)
    save_new(image,args.destino)
    print(args.destino)

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
