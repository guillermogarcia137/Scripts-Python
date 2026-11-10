"""Sirve una carpeta por HTTP solo en 127.0.0.1; Ctrl+C detiene."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nucleo import main
if __name__ == "__main__":
    main('servidor-local')
