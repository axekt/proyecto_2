"""
EJERCICIO 1: Cálculo de Momentos y Centroides
=============================================

a) Figura 1.a -> Área, Centroide (cruz dibujada) y Centroide mediante Momentos.
b) Figura 1.b -> Momento m(2,3), Momento Central mu(2,3) y
                 Momento Central Normalizado eta(2,3).
c) Figura 1.c -> Primeros tres momentos invariantes de Hu (H1, H2, H3).

Convención de coordenadas (la misma que usa OpenCV):
    x -> índice de columna,  y -> índice de fila,  origen en la esquina
    superior izquierda. f(x, y) = 1 si el píxel pertenece al objeto, 0 si es fondo.

Fórmulas utilizadas:
    Momento espacial:              m_pq  = Σ Σ x^p · y^q · f(x, y)
    Centroide:                     x̄ = m10 / m00 ,  ȳ = m01 / m00
    Momento central:               mu_pq = Σ Σ (x - x̄)^p · (y - ȳ)^q · f(x, y)
    Momento central normalizado:   eta_pq = mu_pq / mu00^γ ,  γ = (p + q) / 2 + 1
    Momentos de Hu:
        H1 = eta20 + eta02
        H2 = (eta20 - eta02)^2 + 4·eta11^2
        H3 = (eta30 - 3·eta12)^2 + (3·eta21 - eta03)^2
"""

import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

directorio = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Rutas de las imágenes: reemplazar los nombres por los archivos locales.
# ---------------------------------------------------------------------------
RUTA_FIGURA_1A = os.path.join(directorio, "a.png")
RUTA_FIGURA_1B = os.path.join(directorio, "b.png")
RUTA_FIGURA_1C = os.path.join(directorio, "c.png")
RUTA_SALIDA = os.path.join(directorio, "ejercicio_1_resultado.png")


# ===========================================================================
# Funciones auxiliares
# ===========================================================================
def cargar_imagen_binaria(ruta):
    """
    Carga una imagen y la binariza separando la figura del fondo.

    Se aplica un umbral de Otsu invertido (figuras de color sobre fondo
    claro). Si tras el umbral más de la mitad de los píxeles quedan como
    objeto, se asume que el fondo era oscuro y se invierte la máscara.

    Parámetros
    ----------
    ruta : str
        Ruta del archivo de imagen.

    Retorna
    -------
    img_bgr : np.ndarray
        Imagen original en formato BGR (OpenCV).
    binaria : np.ndarray (uint8)
        Máscara binaria con valores 0 (fondo) y 1 (objeto).
    """
    img_bgr = cv2.imread(ruta, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {ruta}")

    gris = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, binaria = cv2.threshold(gris, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    if binaria.mean() > 0.5:          # el objeto no debería ocupar más que el fondo
        binaria = 1 - binaria

    return img_bgr, binaria.astype(np.uint8)


def obtener_coordenadas(binaria):
    """
    Genera las mallas de coordenadas X (columnas) e Y (filas) de la imagen.

    Retorna
    -------
    x, y : np.ndarray (float64)
        Matrices del mismo tamaño que la imagen con la coordenada de cada píxel.
    """
    filas, columnas = np.indices(binaria.shape, dtype=np.float64)
    return columnas, filas


def momento_espacial(binaria, p, q):
    """
    Calcula el momento espacial (raw moment) de orden (p, q):
        m_pq = Σ Σ x^p · y^q · f(x, y)
    """
    x, y = obtener_coordenadas(binaria)
    f = binaria.astype(np.float64)
    return float(np.sum((x ** p) * (y ** q) * f))


def centroide_por_momentos(binaria):
    """
    Calcula el centroide a partir de los momentos de orden 0 y 1:
        x̄ = m10 / m00 ,  ȳ = m01 / m00
    """
    m00 = momento_espacial(binaria, 0, 0)
    if m00 == 0:
        raise ValueError("La imagen no contiene ningún objeto (m00 = 0).")
    return momento_espacial(binaria, 1, 0) / m00, momento_espacial(binaria, 0, 1) / m00


def momento_central(binaria, p, q):
    """
    Calcula el momento central de orden (p, q) (invariante a traslación):
        mu_pq = Σ Σ (x - x̄)^p · (y - ȳ)^q · f(x, y)
    """
    x, y = obtener_coordenadas(binaria)
    f = binaria.astype(np.float64)
    x_c, y_c = centroide_por_momentos(binaria)
    return float(np.sum(((x - x_c) ** p) * ((y - y_c) ** q) * f))


def momento_central_normalizado(binaria, p, q):
    """
    Calcula el momento central normalizado de orden (p, q)
    (invariante a traslación y escala):
        eta_pq = mu_pq / mu00^γ ,  γ = (p + q) / 2 + 1
    """
    mu00 = momento_central(binaria, 0, 0)
    gamma = (p + q) / 2.0 + 1.0
    return momento_central(binaria, p, q) / (mu00 ** gamma)


def dibujar_cruz(img_bgr, x, y, escala, color, tipo=cv2.MARKER_CROSS, tam=40, grosor=2):
    """
    Dibuja una cruz sobre una imagen previamente ampliada por 'escala'.
    Las coordenadas (x, y) están en píxeles de la imagen original; se
    desplazan +0.5 para apuntar al centro del píxel ampliado.
    """
    punto = (int(round((x + 0.5) * escala)), int(round((y + 0.5) * escala)))
    cv2.drawMarker(img_bgr, punto, color, markerType=tipo,
                   markerSize=tam, thickness=grosor, line_type=cv2.LINE_AA)


# ===========================================================================
# Literal a) Área, centroide y centroide por momentos – Figura 1.a
# ===========================================================================
def analizar_figura_1a(ruta, escala=5):
    """
    Calcula el Área, el Centroide geométrico y el Centroide mediante
    momentos de la Figura 1.a, y dibuja ambos centroides con una cruz.

    - Área: número de píxeles del objeto (equivale a m00 en imagen binaria).
    - Centroide geométrico: promedio de las coordenadas (x, y) de los
      píxeles que pertenecen al objeto.
    - Centroide por momentos: x̄ = m10/m00, ȳ = m01/m00 (se verifica además
      con cv2.moments).

    Parámetros
    ----------
    ruta : str
        Ruta de la Figura 1.a.
    escala : int
        Factor de ampliación de la imagen para visualizar mejor las cruces.

    Retorna
    -------
    dict con las claves: 'area', 'centroide', 'centroide_momentos',
    'centroide_opencv', 'momentos', 'imagen_marcada' (RGB) y 'binaria'.
    """
    img_bgr, binaria = cargar_imagen_binaria(ruta)

    # --- Área -------------------------------------------------------------
    area = int(np.count_nonzero(binaria))

    # --- Centroide geométrico (promedio de coordenadas) -------------------
    ys, xs = np.nonzero(binaria)
    cx_geo, cy_geo = float(xs.mean()), float(ys.mean())

    # --- Centroide mediante momentos (implementación propia) --------------
    m00 = momento_espacial(binaria, 0, 0)
    m10 = momento_espacial(binaria, 1, 0)
    m01 = momento_espacial(binaria, 0, 1)
    cx_mom, cy_mom = m10 / m00, m01 / m00

    # --- Verificación con OpenCV -------------------------------------------
    M = cv2.moments(binaria, binaryImage=True)
    cx_cv, cy_cv = M["m10"] / M["m00"], M["m01"] / M["m00"]

    # --- Dibujo de los centroides sobre la imagen ampliada ----------------
    img_marcada = cv2.resize(img_bgr, None, fx=escala, fy=escala,
                             interpolation=cv2.INTER_NEAREST)
    # Cruz azul: centroide geométrico | Aspa negra: centroide por momentos
    dibujar_cruz(img_marcada, cx_geo, cy_geo, escala, (255, 80, 0),
                 cv2.MARKER_CROSS, tam=50, grosor=3)
    dibujar_cruz(img_marcada, cx_mom, cy_mom, escala, (0, 0, 0),
                 cv2.MARKER_TILTED_CROSS, tam=30, grosor=2)

    print("\n--- a) Figura 1.a: Área y Centroides ---")
    print(f"  Área (píxeles del objeto):        {area}")
    print(f"  m00 = {m00:.0f}   m10 = {m10:.0f}   m01 = {m01:.0f}")
    print(f"  Centroide geométrico  (x, y):     ({cx_geo:.4f}, {cy_geo:.4f})")
    print(f"  Centroide por momentos (x, y):    ({cx_mom:.4f}, {cy_mom:.4f})")
    print(f"  Centroide cv2.moments  (x, y):    ({cx_cv:.4f}, {cy_cv:.4f})")

    return {
        "area": area,
        "centroide": (cx_geo, cy_geo),
        "centroide_momentos": (cx_mom, cy_mom),
        "centroide_opencv": (cx_cv, cy_cv),
        "momentos": {"m00": m00, "m10": m10, "m01": m01},
        "imagen_marcada": cv2.cvtColor(img_marcada, cv2.COLOR_BGR2RGB),
        "binaria": binaria,
    }


# ===========================================================================
# Literal b) Momentos de orden p=2, q=3 – Figura 1.b
# ===========================================================================
def momentos_figura_1b(ruta, p=2, q=3, escala=5):
    """
    Calcula, para la Figura 1.b, los momentos de orden (p, q):
        - Momento espacial               m_pq
        - Momento central                mu_pq
        - Momento central normalizado    eta_pq

    Nota: cv2.moments solo entrega momentos hasta orden 3 (p + q <= 3), por
    lo que el orden (2, 3) -> p + q = 5 se calcula con la implementación
    propia. Para validarla se comparan los momentos de orden (2, 1) contra
    los que entrega OpenCV.

    Parámetros
    ----------
    ruta : str
        Ruta de la Figura 1.b.
    p, q : int
        Órdenes del momento (por defecto p=2, q=3).
    escala : int
        Factor de ampliación para la visualización.

    Retorna
    -------
    dict con 'm', 'mu', 'eta', 'centroide', 'validacion' e 'imagen_marcada'.
    """
    img_bgr, binaria = cargar_imagen_binaria(ruta)

    m_pq = momento_espacial(binaria, p, q)
    mu_pq = momento_central(binaria, p, q)
    eta_pq = momento_central_normalizado(binaria, p, q)
    cx, cy = centroide_por_momentos(binaria)

    # --- Validación de la implementación con OpenCV (orden 2,1) -----------
    M = cv2.moments(binaria, binaryImage=True)
    validacion = {
        "m21": (momento_espacial(binaria, 2, 1), M["m21"]),
        "mu21": (momento_central(binaria, 2, 1), M["mu21"]),
        "nu21": (momento_central_normalizado(binaria, 2, 1), M["nu21"]),
    }

    img_marcada = cv2.resize(img_bgr, None, fx=escala, fy=escala,
                             interpolation=cv2.INTER_NEAREST)
    dibujar_cruz(img_marcada, cx, cy, escala, (0, 0, 255), tam=40, grosor=3)

    print(f"\n--- b) Figura 1.b: Momentos de orden p={p}, q={q} ---")
    print(f"  Centroide (x_c, y_c):                ({cx:.4f}, {cy:.4f})")
    print(f"  Momento de orden        m({p},{q})   = {m_pq:.6e}")
    print(f"  Momento central         mu({p},{q})  = {mu_pq:.6e}")
    print(f"  Momento central normal. eta({p},{q}) = {eta_pq:.6e}")
    print("  Validación contra cv2.moments (orden 2,1):")
    for nombre, (propio, opencv) in validacion.items():
        print(f"    {nombre:<5} propio = {propio: .6e}   OpenCV = {opencv: .6e}")

    return {
        "p": p, "q": q,
        "m": m_pq, "mu": mu_pq, "eta": eta_pq,
        "centroide": (cx, cy),
        "validacion": validacion,
        "imagen_marcada": cv2.cvtColor(img_marcada, cv2.COLOR_BGR2RGB),
        "binaria": binaria,
    }


# ===========================================================================
# Literal c) Primeros tres momentos de Hu – Figura 1.c
# ===========================================================================
def momentos_hu_figura_1c(ruta, escala=3):
    """
    Calcula los tres primeros momentos invariantes de Hu de la Figura 1.c
    a partir de los momentos centrales normalizados:

        H1 = eta20 + eta02
        H2 = (eta20 - eta02)^2 + 4·eta11^2
        H3 = (eta30 - 3·eta12)^2 + (3·eta21 - eta03)^2

    Los resultados se comparan con cv2.HuMoments.

    Parámetros
    ----------
    ruta : str
        Ruta de la Figura 1.c.
    escala : int
        Factor de ampliación para la visualización.

    Retorna
    -------
    dict con 'hu' (H1, H2, H3 propios), 'hu_opencv', 'eta' e 'imagen'.
    """
    img_bgr, binaria = cargar_imagen_binaria(ruta)

    eta = {f"eta{p}{q}": momento_central_normalizado(binaria, p, q)
           for p, q in [(2, 0), (0, 2), (1, 1), (3, 0), (1, 2), (2, 1), (0, 3)]}

    h1 = eta["eta20"] + eta["eta02"]
    h2 = (eta["eta20"] - eta["eta02"]) ** 2 + 4 * eta["eta11"] ** 2
    h3 = (eta["eta30"] - 3 * eta["eta12"]) ** 2 + (3 * eta["eta21"] - eta["eta03"]) ** 2

    hu_cv = cv2.HuMoments(cv2.moments(binaria, binaryImage=True)).flatten()[:3]

    img_ampliada = cv2.resize(img_bgr, None, fx=escala, fy=escala,
                              interpolation=cv2.INTER_NEAREST)

    print("\n--- c) Figura 1.c: Momentos invariantes de Hu ---")
    for i, (propio, opencv) in enumerate(zip((h1, h2, h3), hu_cv), start=1):
        print(f"  H{i}: propio = {propio:.6e}   OpenCV = {opencv:.6e}")

    return {
        "hu": (h1, h2, h3),
        "hu_opencv": tuple(float(v) for v in hu_cv),
        "eta": eta,
        "imagen": cv2.cvtColor(img_ampliada, cv2.COLOR_BGR2RGB),
        "binaria": binaria,
    }


# ===========================================================================
# Visualización de resultados
# ===========================================================================
def _panel_texto(ax, titulo, texto):
    """Dibuja un panel de texto con formato monoespaciado en un eje."""
    ax.axis("off")
    ax.set_title(titulo, fontsize=12, fontweight="bold")
    ax.text(0.02, 0.95, texto, transform=ax.transAxes, va="top", ha="left",
            family="monospace", fontsize=10.5,
            bbox=dict(boxstyle="round,pad=0.8", facecolor="#f4f6fb", edgecolor="#c9d1e3"))


def graficar_resultados(res_a, res_b, res_c, ruta_salida=None, mostrar=True):
    """
    Genera una figura de 3 filas (literales a, b, c) con la imagen procesada a
    la izquierda y los valores calculados a la derecha.
    """
    fig, axes = plt.subplots(3, 2, figsize=(15, 15),
                             gridspec_kw={"width_ratios": [1.1, 1]})
    fig.suptitle("Ejercicio 1: Momentos y Centroides", fontsize=16, fontweight="bold")

    # --- a) ---------------------------------------------------------------
    axes[0, 0].imshow(res_a["imagen_marcada"])
    axes[0, 0].set_title("a) Figura 1.a – Centroides\n"
                         "Cruz azul: geométrico  |  Aspa negra: por momentos", fontsize=11)
    axes[0, 0].axis("off")
    cx, cy = res_a["centroide"]
    mx, my = res_a["centroide_momentos"]
    ox, oy = res_a["centroide_opencv"]
    _panel_texto(axes[0, 1], "a) Área y Centroide", (
        f"Área (píxeles)     = {res_a['area']}\n\n"
        f"m00 = {res_a['momentos']['m00']:.0f}\n"
        f"m10 = {res_a['momentos']['m10']:.0f}\n"
        f"m01 = {res_a['momentos']['m01']:.0f}\n\n"
        f"Centroide geométrico:\n  (x, y) = ({cx:.3f}, {cy:.3f})\n\n"
        f"Centroide por momentos (m10/m00, m01/m00):\n  (x, y) = ({mx:.3f}, {my:.3f})\n\n"
        f"Verificación cv2.moments:\n  (x, y) = ({ox:.3f}, {oy:.3f})"))

    # --- b) ---------------------------------------------------------------
    p, q = res_b["p"], res_b["q"]
    axes[1, 0].imshow(res_b["imagen_marcada"])
    axes[1, 0].set_title("b) Figura 1.b – Centroide (cruz roja)", fontsize=11)
    axes[1, 0].axis("off")
    bx, by = res_b["centroide"]
    texto_val = "\n".join(f"  {k:<5} propio={v[0]: .4e}  cv2={v[1]: .4e}"
                          for k, v in res_b["validacion"].items())
    _panel_texto(axes[1, 1], f"b) Momentos de orden p={p}, q={q}", (
        f"Centroide (x_c, y_c) = ({bx:.3f}, {by:.3f})\n\n"
        f"Momento de orden            m({p},{q})   = {res_b['m']:.6e}\n"
        f"Momento central             mu({p},{q})  = {res_b['mu']:.6e}\n"
        f"Momento central normalizado eta({p},{q}) = {res_b['eta']:.6e}\n\n"
        f"Validación de la implementación (orden 2,1):\n{texto_val}"))

    # --- c) ---------------------------------------------------------------
    axes[2, 0].imshow(res_c["imagen"])
    axes[2, 0].set_title("c) Figura 1.c", fontsize=11)
    axes[2, 0].axis("off")
    texto_hu = "\n".join(
        f"H{i} = {h:.6e}   (cv2: {hc:.6e})"
        for i, (h, hc) in enumerate(zip(res_c["hu"], res_c["hu_opencv"]), start=1))
    texto_eta = "\n".join(f"  {k} = {v: .6e}" for k, v in res_c["eta"].items())
    _panel_texto(axes[2, 1], "c) Momentos invariantes de Hu", (
        f"{texto_hu}\n\n"
        f"Momentos centrales normalizados usados:\n{texto_eta}"))

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    if ruta_salida:
        plt.savefig(ruta_salida, dpi=150, bbox_inches="tight")
        print(f"\nFigura guardada como: {os.path.basename(ruta_salida)}")
    if mostrar:
        plt.show()
    return fig


# ===========================================================================
# Programa principal
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  EJERCICIO 1: Cálculo de Momentos y Centroides")
    print("=" * 60)

    resultado_a = analizar_figura_1a(RUTA_FIGURA_1A)
    resultado_b = momentos_figura_1b(RUTA_FIGURA_1B, p=2, q=3)
    resultado_c = momentos_hu_figura_1c(RUTA_FIGURA_1C)

    graficar_resultados(resultado_a, resultado_b, resultado_c, ruta_salida=RUTA_SALIDA)

    print("\n" + "=" * 60)
    print("  Ejercicio 1 completado exitosamente.")
    print("=" * 60)
