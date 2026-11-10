"""Detecta nombres repetidos y referencias locales en requirements; no busca vulnerabilidades."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nucleo import main
if __name__ == "__main__":
    main('revisar-requirements')
