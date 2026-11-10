"""Crear una hoja de contacto de imágenes."""
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
    parser.add_argument('carpeta',type=Path)
    parser.add_argument('destino',type=Path)
    parser.add_argument('--columnas',type=int,choices=range(1,9),default=4)
    parser.add_argument('--limite',type=int,choices=range(1,101),default=24)
    args=parser.parse_args()
    target=args.destino.resolve()
    files=sorted(p for p in args.carpeta.iterdir() if p.is_file() and p.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.bmp') and p.resolve()!=target)[:args.limite]
    if not files:
        parser.error('No hay imágenes compatibles.')
    width,height=256,210
    rows=(len(files)+args.columnas-1)//args.columnas
    if rows*height*args.columnas*width >40_000_000:
        parser.error('La hoja supera 40 megapíxeles: reduce el límite.')
    canvas=Image.new('RGB',(args.columnas*width,rows*height),'#10152E')
    draw=ImageDraw.Draw(canvas)
    for i,path in enumerate(files):
        image=ImageOps.contain(load_image(path),(width-24,height-50),method=Image.Resampling.LANCZOS)
        x,y=(i%args.columnas)*width,(i//args.columnas)*height
        canvas.paste(image,(x+(width-image.width)//2,y+12))
        label=path.stem[:25].encode('ascii','replace').decode('ascii')
        draw.text((x+12,y+height-26),label,fill='#D6E9F0')
    save_new(canvas,args.destino)

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
