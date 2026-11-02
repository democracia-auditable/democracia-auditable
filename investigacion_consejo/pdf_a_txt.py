"""Extrae el texto de los PDF de fuentes/pdf a fuentes/txt (uno por fichero, con marcas de página)."""
import glob
import os
import sys
import pypdf

AQUI = os.path.dirname(os.path.abspath(__file__))
for p in sorted(glob.glob(os.path.join(AQUI, "fuentes", "pdf", "*.pdf"))):
    salida = os.path.join(AQUI, "fuentes", "txt", os.path.basename(p)[:-4] + ".txt")
    if os.path.exists(salida) and "--todo" not in sys.argv:
        continue
    try:
        paginas = pypdf.PdfReader(p).pages
        texto = "\n".join(f"--- p{i + 1}\n{pg.extract_text() or ''}" for i, pg in enumerate(paginas))
    except Exception as e:
        texto = f"ERROR {e}"
    open(salida, "w", encoding="utf-8").write(texto)
    print(os.path.basename(p), len(texto))
