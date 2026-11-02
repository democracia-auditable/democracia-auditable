"""Ejecuta la regla congelada regla_e4t_v2.py sin modificarla (su huella está en el preregistro).
La copia congelada original lleva la ruta absoluta del equipo donde se escribió (en la copia publicada, sustituida por
una relativa; ver INFORME_TERMINACION.md); este lanzador antepone las rutas relativas del proyecto y la ejecuta tal cual. Uso: python -I -X utf8 ejecutar_regla_congelada.py 50000 1e13 2019 2023"""
import os
import runpy
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "fase0_placsp")]
sys.argv = [os.path.join(AQUI, "regla_e4t_v2.py"), *sys.argv[1:]]
runpy.run_path(sys.argv[0], run_name="__main__")
