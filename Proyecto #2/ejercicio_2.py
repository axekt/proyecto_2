"""
EJERCICIO 2: Histograma con PIL (Pillow)
========================================

Calcula y grafica el histograma de una imagen fotográfica (imagen "a")
utilizando EXCLUSIVAMENTE la librería PIL:

    - Cálculo del histograma:   Image.histogram()
    - Estadísticas:             ImageStat.Stat
    - Gráfica:                  ImageDraw / ImageFont (dibujada píxel a píxel
                                sobre un lienzo de PIL, sin Matplotlib ni NumPy)
    - Visualización:            Image.show() y Image.save()
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageStat

directorio = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Ruta de la imagen: reemplazar el nombre por el archivo local.
# ---------------------------------------------------------------------------
RUTA_IMAGEN_A = os.path.join(directorio, "mono.png")
RUTA_SALIDA = os.path.join(directorio, "ejercicio_2_resultado.png")

# Paleta de colores del gráfico
COLOR_FONDO = (243, 245, 250)
COLOR_PANEL = (255, 255, 255)
COLOR_BORDE = (214, 219, 230)
COLOR_TEXTO = (35, 40, 55)
COLOR_SECUNDARIO = (110, 118, 135)
COLOR_GRILLA = (232, 235, 242)
COLORES_CANAL = {
    "Gris": (70, 75, 90),
    "R": (226, 61, 74),
    "G": (46, 168, 96),
    "B": (52, 110, 230),
}


# ===========================================================================
# Cálculo
# ===========================================================================
def cargar_imagen(ruta):
    """
    Abre una imagen con PIL y la convierte a modo RGB.

    Parámetros
    ----------
    ruta : str
        Ruta del archivo.

    Retorna
    -------
    PIL.Image.Image en modo RGB.
    """
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró la imagen: {ruta}")
    return Image.open(ruta).convert("RGB")


def calcular_histogramas(img_rgb):
    """
    Calcula los histogramas de la imagen usando Image.histogram().

    Para una imagen RGB, histogram() devuelve una lista de 768 valores
    (256 por canal, concatenados R, G, B). Para la imagen en escala de
    grises (modo "L") devuelve 256 valores.

    Retorna
    -------
    dict {"Gris": [...256], "R": [...256], "G": [...256], "B": [...256]}
    """
    hist_gris = img_rgb.convert("L").histogram()
    hist_rgb = img_rgb.histogram()

    histogramas = {
        "Gris": hist_gris,
        "R": hist_rgb[0:256],
        "G": hist_rgb[256:512],
        "B": hist_rgb[512:768],
    }

    # Verificación: cada histograma debe sumar el total de píxeles
    total = img_rgb.width * img_rgb.height
    for nombre, hist in histogramas.items():
        assert sum(hist) == total, f"El histograma {nombre} no suma {total}"

    return histogramas


def calcular_estadisticas(img_rgb):
    """
    Calcula estadísticas por canal con ImageStat (media, desviación,
    mediana y extremos).

    Retorna
    -------
    dict {canal: {"media", "desv", "mediana", "min", "max"}}
    """
    est_gris = ImageStat.Stat(img_rgb.convert("L"))
    est_rgb = ImageStat.Stat(img_rgb)

    estadisticas = {}
    for i, canal in enumerate(["Gris", "R", "G", "B"]):
        est, k = (est_gris, 0) if canal == "Gris" else (est_rgb, i - 1)
        estadisticas[canal] = {
            "media": est.mean[k],
            "desv": est.stddev[k],
            "mediana": est.median[k],
            "min": est.extrema[k][0],
            "max": est.extrema[k][1],
        }
    return estadisticas


# ===========================================================================
# Gráfica (solo PIL)
# ===========================================================================
def cargar_fuente(tamano, negrita=False):
    """Carga una fuente TrueType del sistema; si no existe usa la de PIL."""
    candidatos = (["arialbd.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"] if negrita
                  else ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"])
    for nombre in candidatos:
        try:
            return ImageFont.truetype(nombre, tamano)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=tamano)
    except TypeError:                       # Pillow < 10.1
        return ImageFont.load_default()


FUENTE_TITULO = cargar_fuente(28, negrita=True)
FUENTE_PANEL = cargar_fuente(17, negrita=True)
FUENTE_TEXTO = cargar_fuente(13)
FUENTE_TICKS = cargar_fuente(12)


def _formato_numero(valor):
    """Formatea frecuencias grandes de forma compacta (1.2k, 3.4M)."""
    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.1f}M"
    if valor >= 1_000:
        return f"{valor / 1_000:.1f}k"
    return f"{int(valor)}"


def _texto_vertical(lienzo, texto, centro, fuente, color):
    """Escribe un texto rotado 90° (para la etiqueta del eje Y)."""
    caja = fuente.getbbox(texto)
    ancho, alto = caja[2] - caja[0] + 4, caja[3] - caja[1] + 6
    capa = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    ImageDraw.Draw(capa).text((2 - caja[0], 2 - caja[1]), texto, font=fuente, fill=color)
    capa = capa.rotate(90, expand=True)
    lienzo.paste(capa, (int(centro[0] - capa.width / 2), int(centro[1] - capa.height / 2)), capa)


def dibujar_panel(lienzo, caja, titulo, subtitulo=None):
    """Dibuja el fondo redondeado de un panel con su título."""
    draw = ImageDraw.Draw(lienzo, "RGBA")
    x0, y0, x1, _ = caja
    # sombra suave + panel
    draw.rounded_rectangle((x0 + 3, y0 + 4, caja[2] + 3, caja[3] + 4), radius=14, fill=(0, 0, 0, 18))
    draw.rounded_rectangle(caja, radius=14, fill=COLOR_PANEL, outline=COLOR_BORDE, width=1)
    draw.text((x0 + 20, y0 + 14), titulo, font=FUENTE_PANEL, fill=COLOR_TEXTO)
    if subtitulo:
        ancho_sub = draw.textlength(subtitulo, font=FUENTE_TEXTO)
        draw.text((x1 - 20 - ancho_sub, y0 + 17), subtitulo, font=FUENTE_TEXTO, fill=COLOR_SECUNDARIO)


def dibujar_histograma(lienzo, caja, series, titulo, subtitulo=None, modo="barras"):
    """
    Dibuja un histograma dentro de 'caja' usando ImageDraw.

    Parámetros
    ----------
    lienzo : PIL.Image.Image
        Imagen RGB sobre la que se dibuja.
    caja : tuple (x0, y0, x1, y1)
        Región del panel.
    series : list[(list[int], tuple)]
        Lista de pares (histograma de 256 valores, color RGB).
    titulo, subtitulo : str
        Textos del encabezado del panel.
    modo : "barras" | "linea"
        Barras verticales o curvas rellenas semitransparentes.
    """
    dibujar_panel(lienzo, caja, titulo, subtitulo)
    draw = ImageDraw.Draw(lienzo, "RGBA")

    x0, y0, x1, y1 = caja
    gx0, gy0, gx1, gy1 = x0 + 78, y0 + 52, x1 - 24, y1 - 62   # área de trazado
    ancho, alto = gx1 - gx0, gy1 - gy0
    max_valor = max(max(h) for h, _ in series) or 1

    # --- Grilla horizontal y marcas del eje Y ----------------------------
    for i in range(5):
        y = gy1 - alto * i / 4
        draw.line([(gx0, y), (gx1, y)], fill=COLOR_GRILLA, width=1)
        etiqueta = _formato_numero(max_valor * i / 4)
        tw = draw.textlength(etiqueta, font=FUENTE_TICKS)
        draw.text((gx0 - 10 - tw, y - 7), etiqueta, font=FUENTE_TICKS, fill=COLOR_SECUNDARIO)

    # --- Series -----------------------------------------------------------
    paso = ancho / 256
    for hist, color in series:
        if modo == "barras":
            for nivel, valor in enumerate(hist):
                if valor == 0:
                    continue
                bx0 = gx0 + nivel * paso
                by = gy1 - alto * valor / max_valor
                draw.rectangle([bx0, by, bx0 + max(paso - 0.6, 1), gy1], fill=color + (235,))
        else:
            puntos = [(gx0 + ancho * n / 255, gy1 - alto * v / max_valor) for n, v in enumerate(hist)]
            draw.polygon([(gx0, gy1)] + puntos + [(gx1, gy1)], fill=color + (55,))
            draw.line(puntos, fill=color + (255,), width=2, joint="curve")

    # --- Ejes ---------------------------------------------------------------
    draw.line([(gx0, gy0), (gx0, gy1), (gx1, gy1)], fill=COLOR_TEXTO, width=2)

    # --- Barra de gradiente de intensidad bajo el eje X -------------------
    color_ref = series[0][1] if len(series) == 1 else (255, 255, 255)
    for i in range(int(ancho) + 1):
        t = i / ancho
        c = tuple(int(t * comp) for comp in color_ref)
        draw.line([(gx0 + i, gy1 + 4), (gx0 + i, gy1 + 12)], fill=c)

    # --- Marcas del eje X -------------------------------------------------
    for nivel in (0, 32, 64, 96, 128, 160, 192, 224, 255):
        x = gx0 + ancho * nivel / 255
        draw.line([(x, gy1 + 12), (x, gy1 + 17)], fill=COLOR_TEXTO, width=1)
        etiqueta = str(nivel)
        tw = draw.textlength(etiqueta, font=FUENTE_TICKS)
        draw.text((x - tw / 2, gy1 + 19), etiqueta, font=FUENTE_TICKS, fill=COLOR_SECUNDARIO)

    # --- Etiquetas de los ejes --------------------------------------------
    etiqueta_x = "Nivel de intensidad"
    tw = draw.textlength(etiqueta_x, font=FUENTE_TEXTO)
    draw.text((gx0 + ancho / 2 - tw / 2, gy1 + 38), etiqueta_x, font=FUENTE_TEXTO, fill=COLOR_TEXTO)
    _texto_vertical(lienzo, "Frecuencia (n.º de píxeles)", (x0 + 20, gy0 + alto / 2),
                    FUENTE_TEXTO, COLOR_TEXTO)


def dibujar_imagen(lienzo, caja, img, titulo, subtitulo=None):
    """Pega la imagen original centrada y escalada dentro de un panel."""
    dibujar_panel(lienzo, caja, titulo, subtitulo)
    x0, y0, x1, y1 = caja
    max_w, max_h = (x1 - x0) - 40, (y1 - y0) - 70
    factor = min(max_w / img.width, max_h / img.height)
    miniatura = img.resize((int(img.width * factor), int(img.height * factor)), Image.LANCZOS)
    px = x0 + ((x1 - x0) - miniatura.width) // 2
    py = y0 + 52 + (max_h - miniatura.height) // 2
    lienzo.paste(miniatura, (px, py))
    ImageDraw.Draw(lienzo).rectangle((px - 1, py - 1, px + miniatura.width, py + miniatura.height),
                                     outline=COLOR_BORDE)


def graficar_histograma(img_rgb, histogramas, estadisticas, ruta_salida=None, mostrar=True):
    """
    Construye con PIL un lienzo de 2x3 paneles:
        [Imagen original] [Histograma gris]  [Histograma RGB superpuesto]
        [Canal R]         [Canal G]          [Canal B]

    Parámetros
    ----------
    img_rgb : PIL.Image.Image
    histogramas : dict  (salida de calcular_histogramas)
    estadisticas : dict (salida de calcular_estadisticas)
    ruta_salida : str | None
        Si se indica, guarda el lienzo en esa ruta.
    mostrar : bool
        Si es True, abre el resultado con Image.show().

    Retorna
    -------
    PIL.Image.Image con la gráfica completa.
    """
    ancho_panel, alto_panel, margen, encabezado = 600, 400, 24, 90
    ancho_total = 3 * ancho_panel + 4 * margen
    alto_total = encabezado + 2 * alto_panel + 3 * margen
    lienzo = Image.new("RGB", (ancho_total, alto_total), COLOR_FONDO)

    draw = ImageDraw.Draw(lienzo)
    draw.text((margen, 22), "Ejercicio 2: Histograma de la imagen \"a\" (PIL)",
              font=FUENTE_TITULO, fill=COLOR_TEXTO)
    draw.text((margen, 60), f"Tamaño: {img_rgb.width} x {img_rgb.height} px  ·  "
                            f"Total de píxeles: {img_rgb.width * img_rgb.height}  ·  "
                            f"Calculado con Image.histogram() y dibujado con ImageDraw",
              font=FUENTE_TEXTO, fill=COLOR_SECUNDARIO)

    def caja(fila, col):
        x = margen + col * (ancho_panel + margen)
        y = encabezado + margen + fila * (alto_panel + margen)
        return (x, y, x + ancho_panel, y + alto_panel)

    def sub(canal):
        e = estadisticas[canal]
        return f"μ={e['media']:.1f}  σ={e['desv']:.1f}  med={e['mediana']}"

    dibujar_imagen(lienzo, caja(0, 0), img_rgb, "Imagen original \"a\"")
    dibujar_histograma(lienzo, caja(0, 1), [(histogramas["Gris"], COLORES_CANAL["Gris"])],
                       "Histograma – Escala de grises", sub("Gris"))
    dibujar_histograma(lienzo, caja(0, 2),
                       [(histogramas[c], COLORES_CANAL[c]) for c in ("R", "G", "B")],
                       "Histograma RGB superpuesto", modo="linea")
    for col, canal in enumerate(("R", "G", "B")):
        nombre = {"R": "Rojo (R)", "G": "Verde (G)", "B": "Azul (B)"}[canal]
        dibujar_histograma(lienzo, caja(1, col), [(histogramas[canal], COLORES_CANAL[canal])],
                           f"Canal {nombre}", sub(canal))

    if ruta_salida:
        lienzo.save(ruta_salida)
        print(f"\nGráfica guardada como: {os.path.basename(ruta_salida)}")
    if mostrar:
        lienzo.show(title="Ejercicio 2 - Histograma (PIL)")
    return lienzo


# ===========================================================================
# Función principal del ejercicio
# ===========================================================================
def histograma_pil(ruta, ruta_salida=None, mostrar=True):
    """
    Recibe la ruta de una imagen fotográfica, calcula su histograma
    (escala de grises y por canal RGB) y lo grafica usando solo PIL.

    Retorna
    -------
    (histogramas, estadisticas, lienzo)
    """
    img = cargar_imagen(ruta)
    print(f"\nImagen: {os.path.basename(ruta)}")
    print(f"  Tamaño: {img.width} x {img.height} píxeles  |  Modo: {img.mode}")

    histogramas = calcular_histogramas(img)
    estadisticas = calcular_estadisticas(img)

    print(f"\n  {'Canal':<6}{'Media':>9}{'Desv.':>9}{'Mediana':>9}{'Mín':>6}{'Máx':>6}"
          f"{'Moda':>7}{'Frec. moda':>12}")
    for canal, hist in histogramas.items():
        e = estadisticas[canal]
        moda = hist.index(max(hist))
        print(f"  {canal:<6}{e['media']:>9.2f}{e['desv']:>9.2f}{e['mediana']:>9}"
              f"{e['min']:>6}{e['max']:>6}{moda:>7}{hist[moda]:>12}")

    lienzo = graficar_histograma(img, histogramas, estadisticas, ruta_salida, mostrar)
    return histogramas, estadisticas, lienzo


if __name__ == "__main__":
    print("=" * 60)
    print("  EJERCICIO 2: Histograma con PIL")
    print("=" * 60)

    histograma_pil(RUTA_IMAGEN_A, ruta_salida=RUTA_SALIDA)

    print("\n" + "=" * 60)
    print("  Ejercicio 2 completado exitosamente.")
    print("=" * 60)
