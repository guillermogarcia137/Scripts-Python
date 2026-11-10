"""Alinear la barra de tareas de Windows 11."""
import argparse
import sys

def require_windows(parser):
    if sys.platform != 'win32':
        parser.error('Esta utilidad solo funciona en Windows.')

def main():
    import platform
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('modo',choices=['estado','izquierda','centro'],nargs='?',default='estado')
    args=parser.parse_args()
    require_windows(parser)
    if int(platform.version().split('.')[-1]) < 22000:
        parser.error('Requiere Windows 11 (build 22000 o posterior).')
    import winreg
    path=r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_READ) as key:
        try:
            previous,kind=winreg.QueryValueEx(key,'TaskbarAl')
            print(f'Valor anterior TaskbarAl: {previous} (0=izquierda, 1=centro)')
        except FileNotFoundError:
            print('Sin valor explícito: Windows decide la alineación predeterminada.')
    if args.modo!='estado':
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,path,0,winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key,'TaskbarAl',0,winreg.REG_DWORD,int(args.modo=='centro'))
        print('Guardado. Cierra y abre sesión si no se actualiza; no se reinicia Explorer.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Error: {exc}')
