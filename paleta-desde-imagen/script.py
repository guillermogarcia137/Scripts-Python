"""Extraer colores de una imagen."""
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
    import json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('origen',type=Path)
    parser.add_argument('--colores',type=int,choices=range(2,13),default=6)
    args=parser.parse_args()
    image=load_image(args.origen)
    image.thumbnail((256,256))
    quantized=image.quantize(colors=args.colores)
    palette=quantized.getpalette()
    counts=sorted(quantized.getcolors(),reverse=True)
    total=sum(count for count,_ in counts)
    print(json.dumps([{'hex':'#'+''.join(f'{c:02X}' for c in palette[index*3:index*3+3]),'porcentaje':round(count*100/total,2)} for count,index in counts],indent=2))

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
