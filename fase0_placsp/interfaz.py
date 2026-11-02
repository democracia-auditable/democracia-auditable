#!/usr/bin/env python3
"""Interfaz gráfica de «Democracia Auditable», pensada para quien no programa. Dos pestañas:

  El estudio: conseguir los datos oficiales, analizarlos y ver el resultado. Por debajo ejecuta
    los mismos programas que la línea de comandos (`descargar_datos.py`, `medir_ejecucion.py`) como
    procesos aparte, así que los resultados son idénticos. Al terminar, `informe_legible.py` prepara
    `informe.html` (se abre en el navegador) y `lista_obras.csv` (se abre en Excel).
  Preguntar por obras: el protocolo para organizaciones (`../protocolo_obras/`). Prepara el ciclo del
    mes (`ciclo_mensual.py`), abre solicitudes, registro y pendientes, y ejecuta las órdenes de
    `registro.py` (validar, pendientes, resumen, exportar). No envía nada a ningún sitio.

Solo biblioteca estándar (tkinter viene con Python en Windows y macOS; en algunas
distribuciones de Linux hay que instalar el paquete python3-tk).

Uso:
    python interfaz.py
"""
from __future__ import annotations

import glob
import json
import os
import queue
import re
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, font as tkfont, messagebox, ttk

CARPETA = os.path.dirname(os.path.abspath(__file__))
PROGRAMA = os.path.join(CARPETA, "medir_ejecucion.py")
DESCARGA = os.path.join(CARPETA, "descargar_datos.py")
MANIFIESTO = os.path.join(CARPETA, "manifiesto_descarga_estudio.json")
RESULTADOS_ESTUDIO = os.path.join(CARPETA, "resultados_v2_4")
PROTOCOLO = os.path.normpath(os.path.join(CARPETA, "..", "protocolo_obras"))


def _primera_con_zips(carpetas: list[str]) -> str:
    """La primera carpeta que tenga ZIP oficiales (en ella o en sus subcarpetas); si ninguna, la primera."""
    for c in carpetas:
        if glob.glob(os.path.join(c, "**", "licitacionesPerfilesContratanteCompleto3_*.zip"), recursive=True):
            return c
    return carpetas[0]


# Los datos pueden estar junto al programa o en la carpeta `datos/` del proyecto completo.
DATOS_POR_DEFECTO = _primera_con_zips([os.path.join(CARPETA, "datos"), os.path.normpath(os.path.join(CARPETA, "..", "datos"))])
SIN_VENTANA = getattr(subprocess, "CREATE_NO_WINDOW", 0)   # Windows: que no aparezcan ventanas negras

COLOR_TEXTO_SUAVE = "#5a6676"
COLOR_OK = "#1b7f4b"
COLOR_AVISO = "#8a5a00"
COLOR_ERROR = "#b42318"


def abrir(ruta: str) -> None:
    if sys.platform.startswith("win"):
        os.startfile(ruta)  # noqa: S606 — abre con la aplicación predeterminada
    elif sys.platform == "darwin":
        subprocess.Popen(["open", ruta])
    else:
        subprocess.Popen(["xdg-open", ruta])


def parar_todo(proceso: subprocess.Popen) -> None:
    """Para el proceso Y los que haya lanzado (el análisis reparte la lectura entre varios). En
    Windows, `terminate()` solo para el principal y los demás seguirían trabajando."""
    if proceso.poll() is not None:
        return
    if sys.platform.startswith("win"):
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proceso.pid)], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, creationflags=SIN_VENTANA)
    else:
        import signal
        try:
            os.killpg(proceso.pid, signal.SIGTERM)
        except OSError:
            proceso.terminate()


def gb(n: int) -> str:
    return f"{n / 1e9:.1f}".replace(".", ",") + " GB"


PREFIJO_ZIP = "licitacionesPerfilesContratanteCompleto3_"   # así se llaman los ZIP oficiales


def buscar_zips(carpeta: str) -> list[str]:
    """ZIP oficiales en la carpeta y en todas sus subcarpetas. Si el mismo fichero aparece en dos
    sitios, se usa una sola vez."""
    vistos: dict[str, str] = {}
    for ruta in sorted(glob.glob(os.path.join(carpeta, "**", PREFIJO_ZIP + "*.zip"), recursive=True)):
        vistos.setdefault(os.path.basename(ruta).lower(), ruta)
    return sorted(vistos.values())


CODIGO_ORG = re.compile(r"[A-Za-z0-9_-]{2,20}")
PRIORIDADES = {"Las más antiguas (por defecto)": "antiguedad",
               "Primero las que tienen la coincidencia «terminación licitada de nuevo»": "terminacion"}


TOPES = ("4", "3", "2", "1")   # máximo por órgano y mes; más de 4 solo por línea de comandos y con justificación


def orden_ciclo(organizacion: str, trabajo: str, prioridad: str = "antiguedad", zips: list[str] | None = None,
                minimo: str = "1000000", tope: str = "4", muestra: str = "200", reutilizar: bool = False,
                festivos: str = "") -> list[str]:
    """Orden de `ciclo_mensual.py`. Con `zips`, usa esos ficheros y no descarga nada."""
    if str(tope) not in TOPES:
        raise ValueError("el tope por órgano y mes tiene que estar entre 1 y 4")
    cmd = [sys.executable, "-I", "-u", "-X", "utf8", os.path.join(PROTOCOLO, "ciclo_mensual.py"),
           "--organizacion", organizacion, "--trabajo", trabajo, "--prioridad", prioridad,
           "--min", str(minimo), "--tope", str(tope), "--muestra", str(muestra)]
    if zips is not None:
        cmd += ["--sin-descarga", "--datos", os.pathsep.join(zips)]
    if reutilizar:
        cmd.append("--reutilizar-escaneo")
    if festivos:
        cmd += ["--festivos", festivos]
    return cmd


def mas_reciente(patron: str) -> str | None:
    rutas = sorted(glob.glob(patron))
    return rutas[-1] if rutas else None


def leer_manifiesto() -> dict:
    try:
        with open(MANIFIESTO, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"ficheros": []}


class Plegable(ttk.Frame):
    """Apartado que se abre y se cierra con un clic."""

    def __init__(self, padre, titulo: str) -> None:
        super().__init__(padre)
        self.titulo = titulo
        self.abierto = False
        self.boton = ttk.Button(self, text="▸ " + titulo, style="Enlace.TButton", command=self.alternar)
        self.boton.pack(anchor="w")
        self.contenido = ttk.Frame(self, padding=(18, 4, 0, 4))

    def alternar(self) -> None:
        self.abierto = not self.abierto
        self.boton.configure(text=("▾ " if self.abierto else "▸ ") + self.titulo)
        if self.abierto:
            self.contenido.pack(fill="both", expand=True)
        else:
            self.contenido.pack_forget()


def nitidez_windows() -> None:
    """En pantallas con escalado (125 %, 150 %…) Windows estira la ventana y el texto sale borroso."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            pass


class Aplicacion(tk.Tk):
    def __init__(self) -> None:
        nitidez_windows()
        super().__init__()
        self.title("¿Cómo terminaron las obras públicas?")
        self.k = self.winfo_fpixels("1i") / 96          # escala de la pantalla (1 = 100 %)
        self.geometry(f"{int(880 * self.k)}x{int(780 * self.k)}")
        self.minsize(int(720 * self.k), int(560 * self.k))
        self.cola: queue.Queue = queue.Queue()
        self.proceso: subprocess.Popen | None = None
        self.salida_json: list[str] = []
        self.zips: list[str] = []
        self.manifiesto = leer_manifiesto()
        self.descarga_destino: str | None = None
        self.carpeta_resultado = RESULTADOS_ESTUDIO
        self.cancelado = False
        self._estilos()
        self._construir()
        if os.path.isdir(DATOS_POR_DEFECTO):
            self._poner_zips(buscar_zips(DATOS_POR_DEFECTO))
        self._mostrar_resultado_previo()
        self.after(100, self._leer_cola)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)

    # ---------------------------------------------------------------- aspecto
    def _estilos(self) -> None:
        base = tkfont.nametofont("TkDefaultFont")
        base.configure(size=11)
        tkfont.nametofont("TkTextFont").configure(size=11)
        familia = base.actual("family")
        self.f_titulo = (familia, 18, "bold")
        self.f_paso = (familia, 13, "bold")
        self.f_cifra = (familia, 34, "bold")
        self.f_normal = (familia, 11)
        self.f_peque = (familia, 10)
        e = ttk.Style(self)
        e.configure("Grande.TButton", font=(familia, 12, "bold"), padding=(18, 10))
        e.configure("TButton", padding=(10, 6))
        e.configure("Enlace.TButton", relief="flat", padding=(0, 2))
        e.configure("Paso.TLabelframe.Label", font=self.f_paso)
        e.configure("Paso.TLabelframe", padding=14)

    def _etiqueta(self, padre, texto="", **kw) -> ttk.Label:
        kw.setdefault("wraplength", int(780 * self.k))
        kw.setdefault("justify", "left")
        return ttk.Label(padre, text=texto, **kw)

    # ---------------------------------------------------------------- interfaz
    def _construir(self) -> None:
        lienzo = tk.Canvas(self, highlightthickness=0)
        barra = ttk.Scrollbar(self, orient="vertical", command=lienzo.yview)
        lienzo.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        lienzo.pack(side="left", fill="both", expand=True)
        marco = ttk.Frame(lienzo, padding=(22, 18, 22, 18))
        ventana = lienzo.create_window((0, 0), window=marco, anchor="nw")
        marco.bind("<Configure>", lambda _: lienzo.configure(scrollregion=lienzo.bbox("all")))
        lienzo.bind("<Configure>", lambda ev: lienzo.itemconfigure(ventana, width=ev.width))
        lienzo.bind_all("<MouseWheel>", lambda ev: lienzo.yview_scroll(int(-ev.delta / 120), "units"))
        self.lienzo = lienzo

        # Cabecera
        ttk.Label(marco, text="¿Cómo terminaron las obras públicas?", font=self.f_titulo).pack(anchor="w")
        self._etiqueta(marco, "Trabaja con los datos públicos de contratación del sector público. No usa inteligencia "
                              "artificial, solo se conecta a internet si le pides que descargue los datos y nunca "
                              "envía nada a ninguna administración.").pack(anchor="w", pady=(4, 8))
        pestanas = ttk.Notebook(marco)
        pestanas.pack(fill="x")
        hojas = []
        for texto in ("  El estudio  ", "  Preguntar por obras (protocolo para organizaciones)  "):
            hoja = ttk.Frame(pestanas)
            pestanas.add(hoja, text=texto)
            hojas.append(ttk.Frame(hoja, padding=(4, 12, 4, 4)))
        estudio, protocolo = hojas

        def cambiar(_evento=None):
            # Tk da a todas las pestañas la altura de la más larga: solo se coloca el contenido de la visible.
            visible = pestanas.index("current")
            for i, h in enumerate(hojas):
                if i == visible:
                    h.pack(fill="x")
                else:
                    h.pack_forget()
            self.lienzo.yview_moveto(0)
        pestanas.bind("<<NotebookTabChanged>>", cambiar)
        estudio.pack(fill="x")
        self.pestanas = pestanas
        marco_general, marco = marco, estudio
        self._etiqueta(marco, "Cuenta en cuántas obras se puede saber, con los datos abiertos, cómo terminaron.",
                       foreground=COLOR_TEXTO_SUAVE).pack(anchor="w", pady=(0, 8))
        atajo = ttk.Frame(marco)
        atajo.pack(fill="x", pady=(0, 10))
        ttk.Button(atajo, text="Ver los resultados del estudio ya hechos",
                   command=self._ver_estudio).pack(side="left")
        self._etiqueta(atajo, "  No hace falta descargar ni analizar nada para leerlos.",
                       foreground=COLOR_TEXTO_SUAVE, wraplength=int(480 * self.k)).pack(side="left")

        # Paso 1
        p1 = ttk.LabelFrame(marco, text="Paso 1 · Los datos oficiales", style="Paso.TLabelframe")
        p1.pack(fill="x", pady=6)
        self._etiqueta(p1, "Son 13 ficheros ZIP de la Plataforma de Contratación del Sector Público (unos 7,6 GB). "
                           "Si no los tienes, el programa los descarga de la web oficial y comprueba que son "
                           "exactamente los mismos que usó el estudio.").pack(anchor="w")
        fila = ttk.Frame(p1)
        fila.pack(fill="x", pady=(10, 4))
        self.boton_descargar = ttk.Button(fila, text="Descargar los datos…", command=self._descargar)
        self.boton_descargar.pack(side="left")
        ttk.Button(fila, text="Ya los tengo: buscarlos en una carpeta…",
                   command=self._elegir_carpeta_datos).pack(side="left", padx=8)
        ttk.Button(fila, text="Elegirlos uno a uno…", command=self._elegir_ficheros).pack(side="left")
        estado = ttk.Frame(p1)
        estado.pack(fill="x", pady=(6, 0))
        self.estado_datos = self._etiqueta(estado, "", font=self.f_normal, wraplength=int(640 * self.k))
        self.estado_datos.pack(side="left")
        self.boton_vaciar = ttk.Button(estado, text="Quitar todos", command=lambda: self._poner_zips([]))
        self.boton_parar_descarga = ttk.Button(fila, text="Cancelar la descarga", command=self._detener)
        self.barra_descarga = ttk.Progressbar(p1, mode="determinate", maximum=1000)
        self.texto_descarga = self._etiqueta(p1, "", foreground=COLOR_TEXTO_SUAVE)

        # Paso 2
        p2 = ttk.LabelFrame(marco, text="Paso 2 · Analizar", style="Paso.TLabelframe")
        p2.pack(fill="x", pady=6)
        self._etiqueta(p2, "Lee todos los anuncios de los ficheros (con los del estudio, unos 2,5 millones) y busca, obra por "
                           "obra, señales de cómo terminó. "
                           "Tarda unos minutos; puedes seguir usando el ordenador mientras tanto.").pack(anchor="w")
        fila = ttk.Frame(p2)
        fila.pack(fill="x", pady=(10, 4))
        self.boton_medir = ttk.Button(fila, text="▶  Empezar el análisis", style="Grande.TButton", command=self._medir)
        self.boton_medir.pack(side="left")
        self.boton_parar = ttk.Button(fila, text="Cancelar", command=self._detener)
        self.barra = ttk.Progressbar(p2, mode="determinate", maximum=1000)
        self.texto_progreso = self._etiqueta(p2, "", foreground=COLOR_TEXTO_SUAVE)

        # Paso 3
        p3 = ttk.LabelFrame(marco, text="Paso 3 · El resultado", style="Paso.TLabelframe")
        p3.pack(fill="x", pady=6)
        self.cifra = ttk.Label(p3, text="", font=self.f_cifra)   # se muestra cuando hay resultado
        self.frase = self._etiqueta(p3, "Aquí aparecerá el resultado cuando termine el análisis.", font=self.f_normal)
        self.frase.pack(anchor="w")
        self.aviso = self._etiqueta(
            p3, "Ojo: la cifra no dice que las obras estén sin terminar ni que nadie incumpla nada. Dice que "
                "en estos datos públicos no aparece cómo terminaron. El informe lo explica. La lista de obras que "
                "genera tu análisis se queda en tu ordenador: el proyecto no publica listas de casos reales.",
            foreground=COLOR_AVISO)
        fila = ttk.Frame(p3)
        fila.pack(fill="x", pady=(10, 0))
        self.boton_informe = ttk.Button(fila, text="Abrir el informe", style="Grande.TButton",
                                        command=self._abrir_informe, state="disabled")
        self.boton_informe.pack(side="left")
        self.boton_lista = ttk.Button(fila, text="Abrir la lista de obras (Excel)", command=self._abrir_lista,
                                      state="disabled")
        self.boton_lista.pack(side="left", padx=8)
        self.boton_carpeta = ttk.Button(fila, text="Abrir la carpeta", command=self._abrir_carpeta, state="disabled")
        self.boton_carpeta.pack(side="left")

        # Opciones avanzadas
        avanzadas = Plegable(marco, "Opciones avanzadas")
        avanzadas.pack(fill="x", pady=(14, 0))
        c = avanzadas.contenido
        fila = ttk.Frame(c)
        fila.pack(fill="x")
        ttk.Label(fila, text="Guardar los resultados en:").pack(side="left")
        self.salida = tk.StringVar(value=os.path.join(CARPETA, "resultados"))
        ttk.Entry(fila, textvariable=self.salida).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(fila, text="Cambiar…", command=self._elegir_salida).pack(side="left")
        self.huellas = tk.BooleanVar(value=True)
        ttk.Checkbutton(c, text="Calcular las huellas digitales de los datos (más lento; sirve para demostrar "
                                "qué ficheros se usaron)", variable=self.huellas).pack(anchor="w", pady=(8, 0))
        fila = ttk.Frame(c)
        fila.pack(anchor="w", pady=(6, 0))
        ttk.Label(fila, text="Tareas a la vez (más = más rápido, pero usa más memoria):").pack(side="left")
        self.procesos = tk.IntVar(value=max(1, (os.cpu_count() or 2) - 1))
        ttk.Spinbox(fila, from_=1, to=max(1, os.cpu_count() or 1), width=4,
                    textvariable=self.procesos).pack(side="left", padx=6)
        fila = ttk.Frame(c)
        fila.pack(anchor="w", pady=(8, 0))
        ttk.Button(fila, text="Comprobar que el programa funciona", command=self._pruebas).pack(side="left")
        ttk.Button(fila, text="Leer el método (METODO.md)",
                   command=lambda: abrir(os.path.join(CARPETA, "METODO.md"))).pack(side="left", padx=8)

        self._construir_protocolo(protocolo)

        # Detalles técnicos (comunes a las dos pestañas)
        marco = marco_general
        self.detalles = Plegable(marco, "Detalles técnicos (lo que va escribiendo el programa)")
        self.detalles.pack(fill="x", pady=(4, 0))
        self.registro = tk.Text(self.detalles.contenido, height=12, wrap="word", state="disabled",
                                font=("Consolas", 9))
        self.registro.pack(fill="both", expand=True)

        self._actualizar_estado_datos()

    # ---------------------------------------------------------------- pestaña del protocolo
    def _construir_protocolo(self, marco) -> None:
        self.botones_protocolo: list[ttk.Button] = []

        def boton(padre, texto, orden, **kw):
            b = ttk.Button(padre, text=texto, command=orden, **kw)
            self.botones_protocolo.append(b)
            return b

        self._etiqueta(marco, "Para organizaciones que quieran preguntar a las administraciones cómo terminaron obras "
                              "concretas. El programa prepara borradores de solicitud, un registro y avisos de plazo "
                              "provisionales. No envía nada: cada solicitud la revisa y la presenta la organización, "
                              "identificándose, por la sede electrónica del órgano.").pack(anchor="w")
        self._etiqueta(marco, "Diseño sin probar y sin revisión jurídica: no lo uséis con solicitudes reales sin que un "
                              "jurista revise los plazos, el órgano de garantía y las plantillas. Si lo probáis, empezad "
                              "con un piloto pequeño (20–30 solicitudes).", foreground=COLOR_AVISO).pack(anchor="w", pady=(6, 0))
        fila = ttk.Frame(marco)
        fila.pack(anchor="w", pady=(6, 4))
        ttk.Button(fila, text="Leer la guía paso a paso", command=lambda: self._abrir_protocolo("GUIA.md")).pack(side="left")
        ttk.Button(fila, text="Leer las reglas y su justificación",
                   command=lambda: self._abrir_protocolo("PROTOCOLO_OBRAS.md")).pack(side="left", padx=8)

        # Paso 1: el ciclo del mes
        p1 = ttk.LabelFrame(marco, text="Paso 1 · Preparar las solicitudes del mes", style="Paso.TLabelframe")
        p1.pack(fill="x", pady=6)
        self._etiqueta(p1, "Una vez al mes. Busca las obras de 1 M€ o más cuyo plazo terminó hace más de cuatro meses "
                           "sin que conste su final, y prepara una solicitud redactada para cada una (como mucho 4 por "
                           "órgano al mes, nunca dos veces la misma obra). La primera vez sortea además una muestra fija "
                           "de 200 obras antiguas.").pack(anchor="w")
        fila = ttk.Frame(p1)
        fila.pack(fill="x", pady=(10, 0))
        ttk.Label(fila, text="Código de vuestra organización:").pack(side="left")
        self.organizacion = tk.StringVar()
        ttk.Entry(fila, textvariable=self.organizacion, width=14).pack(side="left", padx=6)
        self._etiqueta(fila, "breve, sin espacios ni nombres de personas (por ejemplo, ORG1)",
                       foreground=COLOR_TEXTO_SUAVE, wraplength=int(420 * self.k)).pack(side="left")

        self.datos_protocolo = tk.StringVar(value=DATOS_POR_DEFECTO)
        hay_datos = bool(buscar_zips(DATOS_POR_DEFECTO)) if os.path.isdir(DATOS_POR_DEFECTO) else False
        self.modo_datos = tk.StringVar(value="tengo" if hay_datos else "descargar")
        ttk.Radiobutton(p1, text="Descargar los datos nuevos de la Plataforma de Contratación (la primera vez, varias "
                                 "horas y unos 15 GB; después, minutos)", value="descargar",
                        variable=self.modo_datos).pack(anchor="w", pady=(10, 0))
        fila = ttk.Frame(p1)
        fila.pack(fill="x")
        ttk.Radiobutton(fila, text="Usar los datos que ya tengo, en:", value="tengo",
                        variable=self.modo_datos).pack(side="left")
        ttk.Entry(fila, textvariable=self.datos_protocolo).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(fila, text="Cambiar…", command=self._elegir_datos_protocolo).pack(side="left")
        self._etiqueta(p1, "Si usáis datos propios, tienen que estar al día: con datos de hace meses faltarán obras.",
                       foreground=COLOR_TEXTO_SUAVE).pack(anchor="w", padx=(24, 0))

        fila = ttk.Frame(p1)
        fila.pack(fill="x", pady=(10, 0))
        ttk.Label(fila, text="Si hay que aplazar obras por el tope, van primero:").pack(side="left")
        self.prioridad = tk.StringVar(value=next(iter(PRIORIDADES)))
        ttk.Combobox(fila, textvariable=self.prioridad, values=list(PRIORIDADES), state="readonly",
                     width=58).pack(side="left", padx=6)
        self._etiqueta(p1, "La coincidencia marca obras para las que el mismo órgano licitó después «la terminación» "
                           "de una obra de título casi igual. En la comparación hecha, marcó 10 de 273 contratos con "
                           "indicios de resolución y 2 de 558 con terminación ordinaria; esas cifras no se pueden "
                           "trasladar a otras obras. Una marca obliga a verificar; su ausencia no informa sobre el estado "
                           "de la obra.", foreground=COLOR_TEXTO_SUAVE).pack(anchor="w", pady=(4, 0))
        ttk.Button(p1, text="¿Qué es exactamente esta coincidencia y cuáles son sus límites?", style="Enlace.TButton",
                   command=lambda: self._abrir_protocolo("SENAL_TERMINACION.md")).pack(anchor="w")

        fila = ttk.Frame(p1)
        fila.pack(fill="x", pady=(10, 4))
        self.boton_ciclo = boton(fila, "▶  Preparar el ciclo de este mes", self._ciclo, style="Grande.TButton")
        self.boton_ciclo.pack(side="left")
        self.boton_parar_ciclo = ttk.Button(fila, text="Cancelar", command=self._detener)
        self.barra_ciclo = ttk.Progressbar(p1, mode="determinate", maximum=5)
        self.texto_ciclo = self._etiqueta(p1, "", foreground=COLOR_TEXTO_SUAVE)

        # Paso 2: presentar y anotar
        p2 = ttk.LabelFrame(marco, text="Paso 2 · Presentar las solicitudes y anotarlo todo", style="Paso.TLabelframe")
        p2.pack(fill="x", pady=6)
        self._etiqueta(p2, "Abrid cada solicitud, completad lugar, fecha e identificación, y presentadla por la sede "
                           "electrónica del órgano como «solicitud de acceso a información pública». Anotad en el "
                           "registro la fecha de envío y la referencia; después, la respuesta, los documentos recibidos "
                           "y sus fechas. El registro se abre con una hoja de cálculo: guardadlo como CSV (UTF-8).").pack(anchor="w")
        fila = ttk.Frame(p2)
        fila.pack(fill="x", pady=(10, 0))
        ttk.Button(fila, text="Qué toca hacer este mes", command=self._abrir_resumen_ciclo).pack(side="left")
        ttk.Button(fila, text="Las solicitudes", command=self._abrir_solicitudes).pack(side="left", padx=8)
        ttk.Button(fila, text="El registro", command=lambda: self._abrir_trabajo("registro.csv")).pack(side="left")
        ttk.Button(fila, text="Lo pendiente y sus fechas", command=self._abrir_pendientes).pack(side="left", padx=8)
        fila = ttk.Frame(p2)
        fila.pack(fill="x", pady=(6, 0))
        ttk.Button(fila, text="Plantilla de reclamación por silencio",
                   command=lambda: self._abrir_protocolo(os.path.join("plantillas", "reclamacion_silencio.txt"))).pack(side="left")
        ttk.Button(fila, text="Abrir la carpeta de trabajo", command=lambda: self._abrir_trabajo("")).pack(side="left", padx=8)

        # Paso 3: seguimiento
        p3 = ttk.LabelFrame(marco, text="Paso 3 · Seguimiento y resultados", style="Paso.TLabelframe")
        p3.pack(fill="x", pady=6)
        self._etiqueta(p3, "Después de anotar en el registro, comprobad que no hay errores y mirad qué vence. Los "
                           "plazos se calculan con sábados, domingos y festivos nacionales: si añadís un fichero con "
                           "los festivos de vuestra comunidad y municipio (una fecha por línea; detrás, si solo vale para "
                           "una comunidad o un órgano, su nombre o «organo:ID»), se tienen en cuenta. Las fechas "
                           "calculadas son provisionales: comprobadlas a mano antes de reclamar y anotadlas en "
                           "«fecha_limite_verificada»; solo esas cuentan para decir si se respondió en plazo.").pack(anchor="w")
        fila = ttk.Frame(p3)
        fila.pack(fill="x", pady=(8, 0))
        ttk.Label(fila, text="Festivos propios (opcional):").pack(side="left")
        self.festivos = tk.StringVar()
        ttk.Entry(fila, textvariable=self.festivos).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(fila, text="Elegir…", command=self._elegir_festivos).pack(side="left")
        fila = ttk.Frame(p3)
        fila.pack(fill="x", pady=(10, 0))
        boton(fila, "Comprobar el registro", lambda: self._registro("validar")).pack(side="left")
        boton(fila, "Ver qué vence", lambda: self._registro("pendientes")).pack(side="left", padx=8)
        boton(fila, "Resumen de resultados", lambda: self._registro("resumen")).pack(side="left")
        boton(fila, "Preparar el borrador para publicar", self._exportar).pack(side="left", padx=8)
        self._etiqueta(p3, "Lo que responde el programa:", foreground=COLOR_TEXTO_SUAVE).pack(anchor="w", pady=(10, 2))
        self.salida_protocolo = tk.Text(p3, height=9, wrap="word", state="disabled", font=("Consolas", 10))
        self.salida_protocolo.pack(fill="x")

        # Opciones avanzadas
        avanzadas = Plegable(marco, "Opciones avanzadas")
        avanzadas.pack(fill="x", pady=(14, 0))
        c = avanzadas.contenido
        fila = ttk.Frame(c)
        fila.pack(fill="x")
        ttk.Label(fila, text="Carpeta de trabajo (lotes, registro y pendientes):").pack(side="left")
        self.trabajo = tk.StringVar(value=PROTOCOLO)
        ttk.Entry(fila, textvariable=self.trabajo).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(fila, text="Cambiar…", command=self._elegir_trabajo).pack(side="left")
        fila = ttk.Frame(c)
        fila.pack(anchor="w", pady=(8, 0))
        self.minimo, self.tope, self.muestra = tk.StringVar(value="1000000"), tk.StringVar(value="4"), tk.StringVar(value="200")
        ttk.Label(fila, text="Importe mínimo sin IVA (€):").pack(side="left")
        ttk.Entry(fila, textvariable=self.minimo, width=10).pack(side="left", padx=4)
        ttk.Label(fila, text="  Máximo por órgano y mes:").pack(side="left")
        ttk.Combobox(fila, textvariable=self.tope, values=TOPES, state="readonly", width=3).pack(side="left", padx=4)
        ttk.Label(fila, text="  Tamaño de la muestra fija:").pack(side="left")
        ttk.Entry(fila, textvariable=self.muestra, width=5).pack(side="left", padx=4)
        self._etiqueta(c, "Cambiadlo solo si lo habéis decidido y declarado de antemano. El máximo por órgano y mes "
                          "protege frente al riesgo de que las solicitudes se consideren abusivas: aquí solo se puede "
                          "bajar (de 4 a 1); subirlo exige la línea de comandos y una justificación que queda escrita.",
                       foreground=COLOR_TEXTO_SUAVE).pack(anchor="w", pady=(2, 0))
        self.reutilizar = tk.BooleanVar(value=False)
        ttk.Checkbutton(c, text="Reutilizar la última búsqueda de obras (más rápido; solo si los datos no han cambiado)",
                        variable=self.reutilizar).pack(anchor="w", pady=(8, 0))
        fila = ttk.Frame(c)
        fila.pack(anchor="w", pady=(8, 0))
        boton(fila, "Comprobar que las herramientas funcionan", self._pruebas_protocolo).pack(side="left")

    def _escribir_protocolo(self, texto: str, limpiar: bool = False) -> None:
        self.salida_protocolo.configure(state="normal")
        if limpiar:
            self.salida_protocolo.delete("1.0", "end")
        self.salida_protocolo.insert("end", texto)
        self.salida_protocolo.see("end")
        self.salida_protocolo.configure(state="disabled")

    def _abrir_protocolo(self, relativo: str) -> None:
        abrir(os.path.join(PROTOCOLO, relativo))

    def _abrir_trabajo(self, nombre: str) -> None:
        ruta = os.path.join(self.trabajo.get(), nombre)
        if os.path.exists(ruta):
            abrir(ruta)
        else:
            messagebox.showinfo("Todavía no existe", f"Aún no hay «{nombre or ruta}». Se crea al preparar el primer ciclo (paso 1).")

    def _abrir_reciente(self, patron: str, descripcion: str) -> None:
        ruta = mas_reciente(os.path.join(self.trabajo.get(), patron))
        if ruta:
            abrir(ruta)
        else:
            messagebox.showinfo("Todavía no existe", f"Aún no hay {descripcion}. Se crea al preparar el ciclo del mes (paso 1).")

    def _abrir_resumen_ciclo(self) -> None:
        self._abrir_reciente("resumen_ciclo_*.md", "resumen de ningún ciclo")

    def _abrir_pendientes(self) -> None:
        self._abrir_reciente("pendientes_*.csv", "lista de pendientes")

    def _abrir_solicitudes(self) -> None:
        """Abre las carpetas de solicitudes del último ciclo (cada mes hay hasta dos lotes: flujo y muestra)."""
        rutas = sorted(glob.glob(os.path.join(self.trabajo.get(), "lote_*", "solicitudes")))
        if not rutas:
            messagebox.showinfo("Todavía no existe", "Aún no hay ninguna solicitud preparada. Se preparan en el paso 1.")
            return
        fecha = lambda r: os.path.basename(os.path.dirname(r))[5:15]  # noqa: E731   lote_AAAA-MM-DD_…
        for r in rutas:
            if fecha(r) == fecha(rutas[-1]):
                abrir(r)

    def _elegir_datos_protocolo(self) -> None:
        carpeta = filedialog.askdirectory(title="Carpeta con los ZIP de la Plataforma (los ficheros no se ven aquí)",
                                          initialdir=self.datos_protocolo.get() or CARPETA)
        if carpeta:
            self.datos_protocolo.set(carpeta)
            self.modo_datos.set("tengo")

    def _elegir_festivos(self) -> None:
        ruta = filedialog.askopenfilename(title="Fichero de festivos (una fecha AAAA-MM-DD por línea)",
                                          filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if ruta:
            self.festivos.set(ruta)

    def _elegir_trabajo(self) -> None:
        carpeta = filedialog.askdirectory(title="Carpeta de trabajo del protocolo", initialdir=self.trabajo.get())
        if carpeta:
            self.trabajo.set(carpeta)

    def _ciclo(self) -> None:
        org = self.organizacion.get().strip()
        if not CODIGO_ORG.fullmatch(org):
            messagebox.showwarning("Falta el código", "Escribid un código breve para vuestra organización: de 2 a 20 "
                                                      "letras o cifras, sin espacios (por ejemplo, ORG1). No uséis el "
                                                      "nombre de una persona.")
            return
        for nombre, var in (("importe mínimo", self.minimo), ("tamaño de la muestra", self.muestra)):
            if not var.get().strip().isdigit():
                messagebox.showwarning("Opción no válida", f"El {nombre} tiene que ser un número entero (Opciones avanzadas).")
                return
        zips = None
        if self.modo_datos.get() == "tengo":
            zips = buscar_zips(self.datos_protocolo.get())
            if not zips:
                messagebox.showwarning("No se han encontrado los datos",
                                       f"En «{self.datos_protocolo.get()}» no hay ficheros de la Plataforma "
                                       f"({PREFIJO_ZIP}….zip). Elegid otra carpeta o marcad «Descargar».")
                return
            texto = f"Se usarán {len(zips)} ficheros de datos que ya tenéis."
        else:
            texto = "Se descargarán los datos que falten (la primera vez, varias horas)."
        if not messagebox.askyesno("Preparar el ciclo del mes",
                                   f"{texto}\n\nDespués se buscarán las obras y se prepararán las solicitudes. "
                                   "Buscar las obras lee todos los anuncios y puede tardar bastante: dejad el "
                                   "ordenador encendido.\n\nNo se envía nada a ninguna administración. ¿Empezar?"):
            return
        cmd = orden_ciclo(org, self.trabajo.get(), PRIORIDADES[self.prioridad.get()], zips, self.minimo.get().strip(),
                          self.tope.get().strip(), self.muestra.get().strip(), self.reutilizar.get(), self.festivos.get().strip())
        self._escribir_protocolo("", limpiar=True)
        self.boton_parar_ciclo.pack(side="left", padx=10)
        self.barra_ciclo.pack(fill="x", pady=(8, 2))
        self.barra_ciclo["value"] = 0
        self.texto_ciclo.pack(anchor="w")
        self.texto_ciclo.configure(text="Empezando…", foreground=COLOR_TEXTO_SUAVE)
        self._lanzar(cmd, self._ciclo_terminado, self._progreso_ciclo_y_salida, cwd=PROTOCOLO)

    def _progreso_ciclo_y_salida(self, linea: str) -> None:
        self._progreso_ciclo(linea)
        if linea.startswith(("línea ", "El registro tiene errores", "No se escribió", "La muestra fija", "Falló")) or "quedó a medias" in linea:
            self._escribir_protocolo(linea)

    PASOS_CICLO = {"1.": "Datos listos. Buscando las obras sin final publicado (es lo que más tarda)…",
                   "2.": "Obras localizadas. Preparando las solicitudes…",
                   "3.": "Solicitudes preparadas. Actualizando el registro y los plazos…",
                   "4.": "Registro al día. Escribiendo el resumen…",
                   "5.": "Terminado."}

    def _progreso_ciclo(self, linea: str) -> None:
        if linea.startswith("Descargando"):
            self.texto_ciclo.configure(text=linea.strip().replace(" …", "…"))
        clave = linea[:2]
        if clave in self.PASOS_CICLO:
            self.barra_ciclo["value"] = int(clave[0])
            self.texto_ciclo.configure(text=self.PASOS_CICLO[clave])

    def _ciclo_terminado(self, codigo: int) -> None:
        self.boton_parar_ciclo.pack_forget()
        if codigo != 0:
            self.texto_ciclo.configure(
                text="Cancelado. Al volver a pulsar el botón, el ciclo se reanuda: reutiliza lo ya preparado hoy y no "
                     "lo rehace." if self.cancelado else
                "No se ha podido completar. El motivo está abajo y en «Detalles técnicos». Si el registro tiene "
                "errores, corregidlos y volved a pulsar: el ciclo se reanuda sin rehacer lo ya preparado.",
                foreground=COLOR_AVISO if self.cancelado else COLOR_ERROR)
            return
        self.barra_ciclo["value"] = 5
        self.texto_ciclo.configure(text="✓ Ciclo preparado. Abajo tenéis qué toca hacer; las solicitudes, el registro "
                                        "y lo pendiente se abren con los botones del paso 2.", foreground=COLOR_OK)
        resumen = mas_reciente(os.path.join(self.trabajo.get(), "resumen_ciclo_*.md"))
        if resumen:
            with open(resumen, encoding="utf-8") as f:
                self._escribir_protocolo(f.read(), limpiar=True)

    def _registro(self, orden: str, extra: list[str] | None = None) -> None:
        registro = os.path.join(self.trabajo.get(), "registro.csv")
        if not os.path.exists(registro):
            messagebox.showinfo("Todavía no hay registro", "El registro se crea al preparar el primer ciclo (paso 1).")
            return
        if orden != "validar":
            # Antes de calcular nada, el registro tiene que estar bien: si no, las fechas y las cifras serían erróneas.
            def tras_validar(codigo):
                if codigo == 0:
                    self._registro_sin_validar(orden, extra)
                else:
                    self._escribir_protocolo("\nEl registro tiene errores (arriba): corregidlos antes de calcular plazos, "
                                             "ver el resumen o exportar.\n")
            self._escribir_protocolo("Comprobando el registro antes de seguir…\n", limpiar=True)
            self._lanzar([sys.executable, "-I", "-X", "utf8", os.path.join(PROTOCOLO, "registro.py"), "validar",
                          "--registro", registro, *self._festivos_cmd()], tras_validar,
                         lambda linea: self._escribir_protocolo(linea) if linea.startswith(("línea", "AVISO")) else None,
                         cwd=PROTOCOLO)
            return
        self._registro_sin_validar(orden, extra)

    def _festivos_cmd(self) -> list[str]:
        return ["--festivos", self.festivos.get().strip()] if self.festivos.get().strip() else []

    def _registro_sin_validar(self, orden: str, extra: list[str] | None = None) -> None:
        registro = os.path.join(self.trabajo.get(), "registro.csv")
        cmd = [sys.executable, "-I", "-X", "utf8", os.path.join(PROTOCOLO, "registro.py"), orden, "--registro", registro]
        if orden in ("validar", "pendientes", "exportar"):
            cmd += self._festivos_cmd()
        cmd += extra or []
        titulos = {"validar": "Comprobación del registro", "pendientes": "Lo que vence (fecha · obra · qué hacer)",
                   "resumen": "Resumen de resultados", "exportar": "Borrador para publicar"}
        self._escribir_protocolo(f"{titulos[orden]}\n\n", limpiar=True)

        def terminado(codigo):
            if orden == "validar" and codigo == 1:
                self._escribir_protocolo("\nHay errores que corregir en el registro (arriba se dice cuáles).\n")
            elif codigo not in (0,):
                self._escribir_protocolo("\nNo se ha podido completar: el motivo está arriba.\n")
        self._lanzar(cmd, terminado, lambda linea: self._escribir_protocolo(linea), cwd=PROTOCOLO)

    def _exportar(self) -> None:
        salida = os.path.join(self.trabajo.get(), "registro_publico_BORRADOR.csv")
        if messagebox.askyesno("Preparar el borrador para publicar",
                               "Se creará «registro_publico_BORRADOR.csv», sin datos del solicitante ni notas internas "
                               "y SIN identificadores de obra ni de órgano (enlace, expediente, órgano, garante).\n\n"
                               "Es un BORRADOR: antes de publicarlo hay que revisarlo. Incluir los identificadores es una "
                               "decisión editorial que se toma aparte (línea de comandos, --con-identificadores). El "
                               "programa no publica nada.\n\n¿Prepararlo?"):
            self._registro("exportar", ["--salida", salida])

    def _pruebas_protocolo(self) -> None:
        self._escribir_protocolo("Comprobando las herramientas del protocolo…\n", limpiar=True)

        def terminado(codigo):
            if codigo == 0:
                messagebox.showinfo("Pruebas", "✓ Todas las pruebas pasan: las herramientas funcionan como se espera.")
            else:
                messagebox.showwarning("Pruebas", "Alguna prueba falla. Mira «Detalles técnicos».")
        self._lanzar([sys.executable, "-I", "-X", "utf8", os.path.join(PROTOCOLO, "test_protocolo.py")], terminado,
                     cwd=PROTOCOLO)

    # ---------------------------------------------------------------- datos
    def _nombres_estudio(self) -> set[str]:
        return {f["nombre"] for f in self.manifiesto.get("ficheros", [])}

    def _poner_zips(self, rutas) -> None:
        self.zips = sorted(set(rutas))
        self._actualizar_estado_datos()

    def _anadir_zips(self, rutas) -> None:
        """Suma a lo ya elegido (los datos pueden estar en varias carpetas), sin repetir ficheros."""
        nombres = {os.path.basename(z).lower() for z in self.zips}
        self._poner_zips(self.zips + [r for r in rutas if os.path.basename(r).lower() not in nombres])

    def _actualizar_estado_datos(self) -> None:
        if not self.zips:
            self.estado_datos.configure(text="Todavía no hay datos elegidos.", foreground=COLOR_TEXTO_SUAVE)
            self.boton_medir.configure(state="disabled")
            self.boton_vaciar.pack_forget()
            return
        self.boton_vaciar.pack(side="right")
        nombres = {os.path.basename(z) for z in self.zips}
        tam = sum(os.path.getsize(z) for z in self.zips if os.path.exists(z))
        estudio = self._nombres_estudio()
        s = "s" if len(self.zips) != 1 else ""
        texto = f"{len(self.zips)} fichero{s} listo{s} ({gb(tam)})."
        if estudio and estudio - nombres:
            faltan = estudio - nombres
            texto = (f"⚠ {texto} Faltan {len(faltan)} de los que usó el estudio, así que el resultado no será "
                     "comparable con el publicado. Si están en otra carpeta, búscalos también ahí: se suman.")
            color = COLOR_AVISO
        elif estudio and nombres - estudio:
            texto = (f"✓ {texto} Están los {len(estudio)} del estudio y {len(nombres - estudio)} más: el análisis "
                     "los leerá todos y la cifra puede diferir un poco de la publicada. Para repetir exactamente el "
                     f"estudio, pulsa «Quitar todos» y elige solo esos {len(estudio)} con «Elegirlos uno a uno…».")
            color = COLOR_AVISO
        else:
            texto = "✓ " + texto + (" Son los ficheros del estudio." if nombres == estudio else "")
            color = COLOR_OK
        self.estado_datos.configure(text=texto, foreground=color)
        self.boton_medir.configure(state="normal" if not self.proceso else "disabled")

    def _elegir_carpeta_datos(self) -> None:
        messagebox.showinfo(
            "Buscar los datos",
            "Ahora se abrirá una ventana para elegir la CARPETA donde están los datos.\n\n"
            "En esa ventana no se ven los ficheros, solo las carpetas: es normal. Entra en la carpeta "
            "(o en una que la contenga) y pulsa «Seleccionar carpeta». El programa buscará los ZIP "
            "dentro, también en sus subcarpetas.")
        carpeta = filedialog.askdirectory(title="Elige la carpeta donde están los datos (los ficheros no se ven aquí)",
                                          initialdir=DATOS_POR_DEFECTO if os.path.isdir(DATOS_POR_DEFECTO) else CARPETA)
        if not carpeta:
            return
        zips = buscar_zips(carpeta)
        if not zips:
            messagebox.showwarning(
                "No se han encontrado los datos",
                f"En «{carpeta}» y sus subcarpetas no hay ficheros de la Plataforma de Contratación.\n\n"
                f"Se llaman así: {PREFIJO_ZIP}2023.zip, {PREFIJO_ZIP}202601.zip…\n\n"
                "Si no los tienes, usa «Descargar los datos».")
            return
        self._anadir_zips(zips)

    def _elegir_ficheros(self) -> None:
        rutas = filedialog.askopenfilenames(
            title="Elige los ZIP (puedes marcar varios con Ctrl o todos con Ctrl+E)",
            initialdir=DATOS_POR_DEFECTO if os.path.isdir(DATOS_POR_DEFECTO) else CARPETA,
            filetypes=[("Datos de la Plataforma de Contratación", PREFIJO_ZIP + "*.zip"), ("Todos los ZIP", "*.zip")])
        if rutas:
            self._anadir_zips(rutas)

    def _elegir_salida(self) -> None:
        carpeta = filedialog.askdirectory(title="Carpeta donde guardar los resultados")
        if carpeta:
            self.salida.set(carpeta)

    # ---------------------------------------------------------------- procesos
    def _escribir(self, texto: str) -> None:
        self.registro.configure(state="normal")
        self.registro.insert("end", texto)
        self.registro.see("end")
        self.registro.configure(state="disabled")

    def _ocupado(self, si: bool) -> None:
        estado = "disabled" if si else "normal"
        self.boton_descargar.configure(state=estado)
        self.boton_medir.configure(state="disabled" if si or not self.zips else "normal")
        for b in self.botones_protocolo:
            b.configure(state=estado)

    def _lanzar(self, cmd: list[str], al_terminar, al_leer=None, cwd: str = CARPETA) -> None:
        if self.proceso:
            messagebox.showinfo("Espera", "Ya hay una tarea en marcha. Espera a que termine o cancélala.")
            return
        self.salida_json = []
        self.cancelado = False
        self._escribir("\n> " + " ".join(os.path.basename(x) if os.path.isabs(x) else x for x in cmd[1:4])
                       + (" …" if len(cmd) > 4 else "") + "\n")
        entorno = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")   # el avance llega al momento
        self.proceso = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.DEVNULL, text=True, encoding="utf-8",
                                        errors="replace", env=entorno, creationflags=SIN_VENTANA,
                                        start_new_session=not sys.platform.startswith("win"))
        self._ocupado(True)
        proceso = self.proceso

        def leer(flujo, etiqueta):
            for linea in flujo:
                self.cola.put((etiqueta, linea, al_leer))
        hilos = [threading.Thread(target=leer, args=(proceso.stdout, "out"), daemon=True),
                 threading.Thread(target=leer, args=(proceso.stderr, "err"), daemon=True)]
        for h in hilos:
            h.start()

        def esperar():
            codigo = proceso.wait()
            for h in hilos:
                h.join()
            self.cola.put(("fin", codigo, al_terminar))
        threading.Thread(target=esperar, daemon=True).start()

    def _leer_cola(self) -> None:
        try:
            while True:
                etiqueta, dato, funcion = self.cola.get_nowait()
                if etiqueta == "fin":
                    self.proceso = None
                    self._ocupado(False)
                    funcion(dato)
                    continue
                if etiqueta == "out":
                    self.salida_json.append(dato)
                self._escribir(dato)
                if funcion:
                    funcion(dato)
        except queue.Empty:
            pass
        self.after(100, self._leer_cola)

    def _detener(self) -> None:
        if self.proceso and messagebox.askyesno("Cancelar", "¿Seguro que quieres cancelar la tarea en marcha?"):
            self.cancelado = True
            parar_todo(self.proceso)
            self._escribir("\nCancelado.\n")

    def destroy(self) -> None:
        for pendiente in self.tk.call("after", "info"):   # sin esto, Tk avisa de tareas huérfanas al cerrar
            self.after_cancel(pendiente)
        super().destroy()

    def _cerrar(self) -> None:
        if self.proceso:
            if not messagebox.askyesno("Salir", "Hay una tarea en marcha. Si sales, se cancelará. ¿Salir?"):
                return
            parar_todo(self.proceso)
        self.destroy()

    # ---------------------------------------------------------------- paso 1: descargar
    def _descargar(self) -> None:
        if not messagebox.askyesno(
                "Descargar los datos",
                "Se descargarán desde la web oficial del Ministerio de Hacienda los 13 ficheros del estudio "
                "(unos 7,6 GB).\n\nEl servidor es lento: puede tardar varias horas. Deja el ordenador "
                "encendido. Si se corta, vuelve a pulsar «Descargar» y seguirá con los que falten.\n\n¿Empezar?"):
            return
        destino = filedialog.askdirectory(title="Carpeta donde guardar los datos", initialdir=CARPETA)
        if not destino:
            return
        self.descarga_destino = destino
        self.barra_descarga.pack(fill="x", pady=(8, 2))
        self.texto_descarga.pack(anchor="w")
        self.texto_descarga.configure(text="Empezando la descarga…", foreground=COLOR_TEXTO_SUAVE)
        self.boton_parar_descarga.pack(side="left", padx=(8, 0))
        self._lanzar([sys.executable, DESCARGA, "reproducir", "--manifiesto", MANIFIESTO, "--destino", destino],
                     self._descarga_terminada)
        self.after(1000, self._vigilar_descarga)

    def _vigilar_descarga(self) -> None:
        """Mide el avance por el tamaño de lo que ya hay en disco (ZIP completos y el .part en curso)."""
        if not self.proceso or not self.descarga_destino:
            return
        total = sum(f["bytes"] for f in self.manifiesto["ficheros"]) or 1
        hecho = 0
        for f in self.manifiesto["ficheros"]:
            for ruta in (os.path.join(self.descarga_destino, f["nombre"]),
                         os.path.join(self.descarga_destino, f["nombre"] + ".part")):
                if os.path.exists(ruta):
                    hecho += os.path.getsize(ruta)
        self.barra_descarga["value"] = min(1000, 1000 * hecho / total)
        texto = f"Descargado {gb(hecho)} de {gb(total)} ({100 * hecho / total:.0f} %)."
        if hecho >= total:
            texto = "Descarga completa. Comprobando que los ficheros son idénticos a los del estudio…"
        self.texto_descarga.configure(text=texto)
        self.after(2000, self._vigilar_descarga)

    def _descarga_terminada(self, codigo: int) -> None:
        self.boton_parar_descarga.pack_forget()
        destino = self.descarga_destino
        self.descarga_destino = None
        self._anadir_zips(buscar_zips(destino))
        if codigo == 0:
            self.barra_descarga["value"] = 1000
            self.texto_descarga.configure(text="✓ Datos descargados y comprobados: son idénticos a los del estudio.",
                                          foreground=COLOR_OK)
        elif any("DISTINTO" in linea for linea in self.salida_json):
            self.texto_descarga.configure(
                text="Descarga terminada, pero algún fichero es distinto del que usó el estudio (Hacienda los "
                     "regenera a veces). Puedes analizarlos igual, pero el resultado podrá variar un poco.",
                foreground=COLOR_AVISO)
        elif self.cancelado:
            self.texto_descarga.configure(
                text="Descarga cancelada. Cuando quieras, vuelve a pulsar «Descargar» y elige la misma carpeta: "
                     "seguirá con los ficheros que falten.", foreground=COLOR_AVISO)
        else:
            self.texto_descarga.configure(
                text="La descarga se ha interrumpido. Comprueba la conexión y vuelve a pulsar «Descargar» con la "
                     "misma carpeta: seguirá con los ficheros que falten.", foreground=COLOR_ERROR)

    # ---------------------------------------------------------------- paso 2: analizar
    def _medir(self) -> None:
        if not self.zips:
            messagebox.showwarning("Faltan los datos", "Primero elige o descarga los datos (paso 1).")
            return
        salida = self.salida.get()
        cmd = [sys.executable, PROGRAMA, *self.zips, "--salida", salida, "--procesos", str(int(self.procesos.get()))]
        if not self.huellas.get():
            cmd.append("--sin-huellas")
        self.boton_parar.pack(side="left", padx=10)
        self.barra.pack(fill="x", pady=(8, 2))
        self.texto_progreso.pack(anchor="w")
        self.barra.configure(mode="indeterminate")
        self.barra.start(15)
        self.texto_progreso.configure(text="Preparando la lectura de los ficheros…", foreground=COLOR_TEXTO_SUAVE)
        self._lanzar(cmd, self._medicion_terminada, self._progreso_medicion)

    def _progreso_medicion(self, linea: str) -> None:
        m = re.match(r"\s*(\d+)/(\d+) ficheros, (\d+) entradas", linea)
        if not m:
            return
        i, n, entradas = map(int, m.groups())
        if str(self.barra["mode"]) != "determinate":
            self.barra.stop()
            self.barra.configure(mode="determinate")
        self.barra["value"] = 1000 * i / n
        miles = f"{entradas:,}".replace(",", ".")
        self.texto_progreso.configure(
            text=f"Leyendo: {100 * i / n:.0f} % ({miles} anuncios)." if i < n
            else "Lectura terminada. Calculando el resultado y escribiendo el informe…")

    def _medicion_terminada(self, codigo: int) -> None:
        self.barra.stop()
        self.boton_parar.pack_forget()
        if codigo != 0:
            self.barra.configure(mode="determinate")
            self.barra["value"] = 0
            self.texto_progreso.configure(
                text="Análisis cancelado. Puedes volver a empezarlo cuando quieras." if self.cancelado else
                "El análisis no ha terminado por un error. Abre «Detalles técnicos» para ver qué ha pasado.",
                foreground=COLOR_AVISO if self.cancelado else COLOR_ERROR)
            return
        self.barra.configure(mode="determinate")
        self.barra["value"] = 1000
        try:
            import informe_legible
            r = informe_legible.generar(self.salida.get(), CARPETA)
        except Exception as error:  # noqa: BLE001 — se muestra al usuario
            self.texto_progreso.configure(text=f"Análisis terminado, pero no se pudo preparar el informe: {error}",
                                          foreground=COLOR_ERROR)
            self._activar_resultado(self.salida.get())
            return
        self.texto_progreso.configure(text="✓ Análisis terminado.", foreground=COLOR_OK)
        self._mostrar_cifras(r, self.salida.get(), propio=True)
        self._abrir_informe()

    # ---------------------------------------------------------------- paso 3: resultado
    def _mostrar_cifras(self, r: dict, carpeta: str, propio: bool) -> None:
        miles = lambda n: f"{n:,}".replace(",", ".")  # noqa: E731
        self.cifra.configure(text=r["porcentaje"])
        self.cifra.pack(anchor="w", before=self.frase)
        origen = "" if propio else "Resultado del estudio publicado. "
        self.frase.configure(
            text=f"{origen}De las {miles(r['vencidas'])} obras que ya deberían haber terminado, en "
                 f"{miles(r['sin_fin'])} no aparece en los datos públicos ninguna señal de cómo terminaron "
                 f"(datos hasta el {r['corte']}).")
        self.aviso.pack(anchor="w", pady=(6, 0), before=self.boton_informe.master)
        self._activar_resultado(carpeta)

    def _activar_resultado(self, carpeta: str) -> None:
        self.carpeta_resultado = carpeta
        for b in (self.boton_informe, self.boton_lista, self.boton_carpeta):
            b.configure(state="normal")

    def _mostrar_resultado_previo(self) -> None:
        """Si ya hay un análisis hecho en la carpeta de resultados, lo enseña al abrir."""
        carpeta = self.salida.get()
        if os.path.exists(os.path.join(carpeta, "resumen.json")):
            try:
                import informe_legible
                self._mostrar_cifras(informe_legible.generar(carpeta, CARPETA), carpeta, propio=True)
                self.frase.configure(text="Último análisis hecho en este ordenador. " + self.frase.cget("text"))
            except Exception:  # noqa: BLE001 — si falla, simplemente no se enseña
                pass

    def _ver_estudio(self) -> None:
        ruta = os.path.join(RESULTADOS_ESTUDIO, "informe.html")
        if not os.path.exists(ruta):
            try:
                import informe_legible
                informe_legible.generar(RESULTADOS_ESTUDIO, CARPETA, publico=True)
            except Exception:  # noqa: BLE001
                messagebox.showinfo("No encontrado", "No está el informe del estudio en la carpeta del programa. Puedes "
                                                     "regenerarlo repitiendo el análisis (pasos 1 y 2).")
                return
        abrir(ruta)

    def _abrir_informe(self) -> None:
        ruta = os.path.join(self.carpeta_resultado, "informe.html")
        abrir(ruta if os.path.exists(ruta) else os.path.join(self.carpeta_resultado, "informe.md"))

    def _abrir_lista(self) -> None:
        ruta = os.path.join(self.carpeta_resultado, "lista_obras.csv")
        if os.path.exists(ruta):
            abrir(ruta)

    def _abrir_carpeta(self) -> None:
        abrir(self.carpeta_resultado)

    # ---------------------------------------------------------------- pruebas
    def _pruebas(self) -> None:
        if not self.detalles.abierto:
            self.detalles.alternar()

        def terminado(codigo):
            if codigo == 0:
                messagebox.showinfo("Pruebas", "✓ Todas las pruebas pasan: el programa funciona como se espera.")
            else:
                messagebox.showwarning("Pruebas", "Alguna prueba falla. Mira «Detalles técnicos».")
        self._lanzar([sys.executable, "-m", "unittest", "-v", "test_medir_ejecucion"], terminado)


if __name__ == "__main__":
    Aplicacion().mainloop()
