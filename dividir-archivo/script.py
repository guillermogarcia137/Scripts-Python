"""Divide en partes y genera manifiesto SHA-256 en carpeta nueva."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nucleo import main
if __name__ == "__main__":
    main('dividir-archivo')
