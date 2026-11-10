"""Convierte un subconjunto de Markdown a HTML estático escapado."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nucleo import main
if __name__ == "__main__":
    main('markdown-a-html')
