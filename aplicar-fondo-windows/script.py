"""Aplicar y restaurar un fondo de escritorio."""
import argparse
import sys

def require_windows(parser):
    if sys.platform != 'win32':
        parser.error('Esta utilidad solo funciona en Windows.')

def main():
    import ctypes
    import json
    from ctypes import wintypes
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('accion',choices=['estado','aplicar','restaurar'],nargs='?',default='estado')
    parser.add_argument('--imagen',type=Path)
    parser.add_argument('--copia',type=Path,help='JSON nuevo al aplicar; JSON anterior al restaurar')
    args=parser.parse_args()
    require_windows(parser)
    api=ctypes.WinDLL('user32',use_last_error=True).SystemParametersInfoW
    api.argtypes=[wintypes.UINT,wintypes.UINT,ctypes.c_void_p,wintypes.UINT]
    api.restype=wintypes.BOOL
    current=ctypes.create_unicode_buffer(32768)
    if not api(0x73,len(current),current,0):
        raise ctypes.WinError(ctypes.get_last_error())
    print('Fondo anterior: '+current.value)
    if args.accion=='estado':
        return
    if args.copia is None:
        parser.error('--copia es obligatorio para aplicar o restaurar.')
    if args.accion=='aplicar':
        if args.imagen is None:
            parser.error('--imagen es obligatorio al aplicar.')
        target=args.imagen.resolve(strict=True)
        if not target.is_file() or target.suffix.lower() not in ('.png','.jpg','.jpeg','.bmp'):
            parser.error('Selecciona una imagen PNG, JPEG o BMP existente.')
        with args.copia.open('x',encoding='utf-8') as output:
            json.dump({'version':1,'fondo':current.value},output,ensure_ascii=False,indent=2)
        value=str(target)
    else:
        backup=json.loads(args.copia.read_text(encoding='utf-8'))
        if not isinstance(backup,dict) or backup.get('version')!=1 or not isinstance(backup.get('fondo'),str):
            raise ValueError('Copia de fondo inválida.')
        value=backup['fondo']
        if value and not Path(value).is_file():
            raise ValueError('La imagen anterior ya no existe; vuelve a colocarla en su ruta.')
    buffer=ctypes.create_unicode_buffer(value)
    if not api(0x14,0,buffer,3):
        raise ctypes.WinError(ctypes.get_last_error())
    print('Fondo actualizado. Se conserva el JSON de recuperación.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
