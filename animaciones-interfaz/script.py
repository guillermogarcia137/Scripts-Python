"""Consultar o ajustar animaciones del área cliente."""
import argparse
import sys

def require_windows(parser):
    if sys.platform != 'win32':
        parser.error('Esta utilidad solo funciona en Windows.')

def main():
    import ctypes
    from ctypes import wintypes
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('modo',choices=['estado','activar','desactivar'],nargs='?',default='estado')
    args=parser.parse_args()
    require_windows(parser)
    api=ctypes.WinDLL('user32',use_last_error=True).SystemParametersInfoW
    api.argtypes=[wintypes.UINT,wintypes.UINT,ctypes.c_void_p,wintypes.UINT]
    api.restype=wintypes.BOOL
    enabled=wintypes.BOOL()
    if not api(0x1042,0,ctypes.byref(enabled),0):
        raise ctypes.WinError(ctypes.get_last_error())
    print('Estado anterior: '+('activar' if enabled.value else 'desactivar'))
    if args.modo!='estado':
        if not api(0x1043,0,ctypes.c_void_p(int(args.modo=='activar')),3):
            raise ctypes.WinError(ctypes.get_last_error())
        print('Preferencia guardada y notificada a las aplicaciones.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
