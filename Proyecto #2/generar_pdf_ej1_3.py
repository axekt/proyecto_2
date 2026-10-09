import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable,
    Image as RLImage
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def registrar_fuente_codigo():
    candidatos = [
        r"C:\Windows\Fonts\consola.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/Library/Fonts/Menlo.ttc",
    ]
    for ruta in candidatos:
        if os.path.isfile(ruta):
            try:
                pdfmetrics.registerFont(TTFont("CodeFont", ruta))
                return "CodeFont"
            except Exception:
                continue
    return "Courier"


FUENTE_CODIGO = registrar_fuente_codigo()


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Proyecto #2 — Procesamiento de Imágenes (Ejercicios 1 al 3)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 750, 612 - 54, 750)

        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Documento Técnico Explicativo — Python, OpenCV, PIL, NumPy, Matplotlib")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()


def escapar_codigo(linea):
    """Escapa caracteres XML y conserva la indentación inicial del código."""
    sin_indent = linea.lstrip(" ")
    indent = len(linea) - len(sin_indent)
    texto = sin_indent.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = texto.replace("  ", "&nbsp; ")
    return "&nbsp;" * indent + texto


def build_pdf():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_pdf = os.path.join(directorio_actual, "Resumen_Ejercicios_1_al_3.pdf")

    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    dark_text = colors.HexColor("#2D3748")
    muted_text = colors.HexColor("#4A5568")
    code_bg = colors.HexColor("#F7FAFC")
    code_border = colors.HexColor("#CBD5E0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=1,  # Center
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Header3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#2C5282"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=dark_text,
        spaceAfter=5
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor=muted_text,
        alignment=1
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName=FUENTE_CODIGO,
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1A202C")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=dark_text
    )

    story = []

    # Title Banner Box
    title_table = Table(
        [[Paragraph("<b>PROYECTO ACADÉMICO — PROCESAMIENTO DE IMÁGENES</b><br/><font size=11 color='#4A5568'>Resumen General, Justificación de Librerías y Análisis Línea por Línea (Ejercicios 1 al 3)</font>", title_style)]],
        colWidths=[504]
    )
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 14))

    # SECTION 1: Resumen General
    story.append(Paragraph("1. Resumen General de Cada Ejercicio", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    resumenes = [
        ("Ejercicio 1: Cálculo de Momentos y Centroides",
         "<b>Objetivo:</b> Analizar tres figuras binarias (<i>a.png</i>, <i>b.png</i> y <i>c.png</i>): a) calcular el área y el centroide de la Figura 1.a; "
         "b) obtener el momento de orden p=2, q=3, su momento central y su momento central normalizado para la Figura 1.b; "
         "c) calcular los tres primeros momentos invariantes de Hu para la Figura 1.c.<br/>"
         "<b>Mecanismo:</b> Cada imagen se binariza con el método de Otsu (objeto = 1, fondo = 0). Se implementan desde cero, con NumPy, las fórmulas "
         "m<sub>pq</sub> = &#931;&#931; x<super>p</super> y<super>q</super> f(x,y), el momento central mu<sub>pq</sub> (respecto del centroide) y el normalizado "
         "eta<sub>pq</sub> = mu<sub>pq</sub> / mu<sub>00</sub><super>gamma</super> con gamma = (p+q)/2 + 1. Todos los resultados se validan contra "
         "<code>cv2.moments()</code> y <code>cv2.HuMoments()</code> de OpenCV."),

        ("Ejercicio 2: Histograma de la Imagen \"a\" con PIL",
         "<b>Objetivo:</b> Obtener y graficar el histograma de la imagen <i>mono.png</i> usando exclusivamente la librería PIL/Pillow, tanto en escala de grises como por canal R, G y B.<br/>"
         "<b>Mecanismo:</b> Con <code>Image.histogram()</code> se obtienen las frecuencias (256 valores en gris y 768 en RGB, segmentados por canal), verificando que la suma coincide con el "
         "total de píxeles. <code>ImageStat.Stat</code> calcula media, desviación estándar, mediana y extremos. Toda la gráfica (paneles, grilla, barras, curvas, ejes y etiquetas) se dibuja "
         "manualmente con <code>ImageDraw</code> sobre un lienzo de 6 paneles, sin usar Matplotlib."),

        ("Ejercicio 3: Separación de Planos R, G, B y Conversión a Escala de Grises",
         "<b>Objetivo:</b> Separar los tres planos de color de la imagen <i>flores.png</i> y convertirla a escala de grises.<br/>"
         "<b>Mecanismo:</b> La imagen se carga con OpenCV (que trabaja en BGR) y se convierte a RGB. Con <code>cv2.split()</code> se separan los canales, que se muestran como "
         "intensidad en gris y como imagen 'teñida' con su color puro, junto con el histograma de cada canal (<code>cv2.calcHist()</code>). La conversión a gris se realiza de dos formas: con "
         "<code>cv2.cvtColor(RGB2GRAY)</code> y manualmente con la fórmula de luminancia ITU-R BT.601 (Y = 0.299R + 0.587G + 0.114B), comparando ambos resultados con un mapa de diferencias absolutas.")
    ]

    for titulo, desc in resumenes:
        story.append(Paragraph(titulo, h2_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # SECTION 2: Librerías Utilizadas
    story.append(Paragraph("2. Librerías Utilizadas y Justificación Técnica", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

    lib_data = [
        [Paragraph("<b>Librería / Módulo</b>", table_header_style),
         Paragraph("<b>Funciones Principales Usadas</b>", table_header_style),
         Paragraph("<b>Justificación de Uso en el Proyecto</b>", table_header_style)],

        [Paragraph("<b>OpenCV</b><br/>(<code>cv2</code>)<br/>Ej. 1 y 3", table_cell_style),
         Paragraph("<code>imread()</code>, <code>cvtColor()</code>, <code>threshold()</code> (Otsu), <code>moments()</code>, <code>HuMoments()</code>, <code>resize()</code>, "
                   "<code>drawMarker()</code>, <code>split()</code>, <code>calcHist()</code>, <code>absdiff()</code>, <code>imwrite()</code>", table_cell_style),
         Paragraph("Librería de visión por computadora optimizada en C++. Permite binarizar automáticamente con Otsu, calcular momentos de referencia para validar la implementación propia, "
                   "separar canales y convertir espacios de color de forma eficiente. Se tiene en cuenta que OpenCV carga las imágenes en orden <b>BGR</b>.", table_cell_style)],

        [Paragraph("<b>PIL / Pillow</b><br/>(<code>Image, ImageDraw, ImageFont, ImageStat</code>)<br/>Ej. 2", table_cell_style),
         Paragraph("<code>Image.open()</code>, <code>convert()</code>, <code>histogram()</code>, <code>resize()</code>, <code>paste()</code>, <code>rotate()</code>, "
                   "<code>ImageDraw.rectangle()</code>, <code>rounded_rectangle()</code>, <code>line()</code>, <code>polygon()</code>, <code>text()</code>, <code>ImageStat.Stat</code>", table_cell_style),
         Paragraph("El enunciado del Ejercicio 2 exige usar PIL. <code>histogram()</code> devuelve directamente las frecuencias por nivel, <code>ImageStat</code> entrega las estadísticas "
                   "por banda e <code>ImageDraw</code> permite construir la gráfica completa píxel a píxel, con transparencias (RGBA) y fuentes TrueType.", table_cell_style)],

        [Paragraph("<b>NumPy</b><br/>(<code>numpy</code>)<br/>Ej. 1 y 3", table_cell_style),
         Paragraph("<code>indices()</code>, <code>sum()</code>, <code>nonzero()</code>, <code>count_nonzero()</code>, <code>mean()</code>, <code>zeros()</code>, <code>clip()</code>, "
                   "<code>round()</code>, <code>astype()</code>", table_cell_style),
         Paragraph("Permite expresar las fórmulas de momentos como operaciones vectorizadas sobre mallas de coordenadas (x, y), sin bucles explícitos. También se usa para la conversión "
                   "manual a gris en coma flotante y para construir las imágenes 'teñidas' de cada canal.", table_cell_style)],

        [Paragraph("<b>Matplotlib</b><br/>(<code>pyplot</code>)<br/>Ej. 1 y 3", table_cell_style),
         Paragraph("<code>subplots()</code>, <code>imshow()</code>, <code>text()</code>, <code>plot()</code>, <code>fill_between()</code>, <code>colorbar()</code>, "
                   "<code>tight_layout()</code>, <code>savefig()</code>, <code>show()</code>", table_cell_style),
         Paragraph("Generación de figuras comparativas multipanel: imágenes con centroides marcados, paneles de texto con los resultados numéricos, histogramas por canal y mapas de "
                   "diferencia con barra de color. Exporta a PNG a 150 DPI.", table_cell_style)],

        [Paragraph("<b>os</b>", table_cell_style),
         Paragraph("<code>path.dirname()</code>, <code>path.abspath()</code>, <code>path.join()</code>, <code>path.isfile()</code>, <code>path.basename()</code>", table_cell_style),
         Paragraph("Construye rutas relativas a la ubicación del script, garantizando que el programa funcione en cualquier sistema operativo y desde cualquier directorio de trabajo.", table_cell_style)]
    ]

    lib_table = Table(lib_data, colWidths=[100, 160, 244])
    lib_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(lib_table)
    story.append(Spacer(1, 14))

    # Helper function to render Code Blocks & Line explanations
    def render_section(exercise_num, exercise_title, script_name, blocks_data):
        story.append(PageBreak())
        story.append(Paragraph(f"3.{exercise_num} Ejercicio {exercise_num} — {exercise_title}", h1_style))
        story.append(Paragraph(f"<b>Archivo fuente:</b> <code>{script_name}</code> (Código limpio sin comentarios)", h3_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

        for block_num, b_title, b_code, b_lines in blocks_data:
            block_flowables = []
            block_flowables.append(Paragraph(f"Bloque {block_num}: {b_title}", h2_style))

            # Code box
            code_paragraphs = [Paragraph(f"<font color='#718096'>{ln:3d} | </font>{escapar_codigo(code_line)}", code_style) for ln, code_line in b_code]
            code_table = Table([[code_paragraphs]], colWidths=[504])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), code_bg),
                ('BOX', (0, 0), (-1, -1), 0.8, code_border),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            block_flowables.append(code_table)
            block_flowables.append(Spacer(1, 5))

            # Line by line explanations
            block_flowables.append(Paragraph("<b>Explicación línea por línea:</b>", h3_style))
            for line_range, explanation in b_lines:
                text = f"• <b>Línea {line_range}:</b> {explanation}"
                block_flowables.append(Paragraph(text, body_style))

            block_flowables.append(Spacer(1, 8))
            story.append(KeepTogether(block_flowables))

    # Helper function to append the result figures produced by each exercise
    def render_resultados(figuras):
        existentes = [(n, c) for n, c in figuras if os.path.isfile(os.path.join(directorio_actual, n))]
        if not existentes:
            return
        from PIL import Image as PILImage
        story.append(PageBreak())
        story.append(Paragraph("Resultado obtenido", h2_style))
        for nombre, caption in existentes:
            ruta = os.path.join(directorio_actual, nombre)
            with PILImage.open(ruta) as im:
                w_px, h_px = im.size
            ancho = 504
            alto = ancho * h_px / w_px
            if alto > 520:
                alto = 520
                ancho = alto * w_px / h_px
            story.append(KeepTogether([
                RLImage(ruta, width=ancho, height=alto),
                Spacer(1, 4),
                Paragraph(f"{caption} (<i>{nombre}</i>)", caption_style),
                Spacer(1, 12),
            ]))

    # ==================== EJERCICIO 1 DATA ====================
    ej1_blocks = [
        (1, "Importación de Librerías y Definición de Rutas",
         [(3, 'import os'),
          (5, 'import cv2'),
          (6, 'import numpy as np'),
          (7, 'import matplotlib.pyplot as plt'),
          (9, 'directorio = os.path.dirname(os.path.abspath(__file__))'),
          (14, 'RUTA_FIGURA_1A = os.path.join(directorio, "a.png")'),
          (15, 'RUTA_FIGURA_1B = os.path.join(directorio, "b.png")'),
          (16, 'RUTA_FIGURA_1C = os.path.join(directorio, "c.png")'),
          (17, 'RUTA_SALIDA = os.path.join(directorio, "ejercicio_1_resultado.png")')],
         [("3", "Importa el módulo <code>os</code> para construir rutas de archivo independientes del sistema operativo."),
          ("5-7", "Importa OpenCV (<code>cv2</code>) para lectura, binarización y validación de momentos; NumPy para el cálculo vectorizado; y <code>pyplot</code> de Matplotlib para la figura de resultados."),
          ("9", "Obtiene la carpeta donde se encuentra el script, de modo que las imágenes se localicen sin importar desde dónde se ejecute."),
          ("14-16", "Rutas absolutas de las tres figuras binarias del enunciado: 1.a, 1.b y 1.c."),
          ("17", "Ruta del archivo PNG donde se guardará la figura final con todos los resultados.")]),

        (2, "Carga y Binarización Automática de la Imagen (Otsu)",
         [(23, 'def cargar_imagen_binaria(ruta):'),
          (25, '    img_bgr = cv2.imread(ruta, cv2.IMREAD_COLOR)'),
          (26, '    if img_bgr is None:'),
          (27, '        raise FileNotFoundError(f"No se pudo cargar la imagen: {ruta}")'),
          (29, '    gris = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)'),
          (30, '    _, binaria = cv2.threshold(gris, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)'),
          (32, '    if binaria.mean() > 0.5:'),
          (33, '        binaria = 1 - binaria'),
          (35, '    return img_bgr, binaria.astype(np.uint8)')],
         [("23", "Define la función que transforma cualquier figura en una matriz binaria f(x,y) con valores 0 (fondo) y 1 (objeto)."),
          ("25-27", "Lee la imagen en color (OpenCV la entrega en orden BGR). Si <code>imread</code> devuelve <code>None</code> el archivo no existe o está dañado, y se lanza una excepción descriptiva."),
          ("29", "Convierte la imagen a escala de grises, requisito para la umbralización."),
          ("30", "Aplica el umbral de <b>Otsu</b>, que elige automáticamente el valor de corte óptimo. Con <code>THRESH_BINARY_INV</code> y valor máximo 1, los píxeles oscuros (el objeto) quedan en 1 y el fondo claro en 0."),
          ("32-33", "Medida de seguridad: si más de la mitad de los píxeles quedaron en 1, se asume que se invirtió objeto/fondo y se corrige con <code>1 - binaria</code>."),
          ("35", "Devuelve la imagen original (para dibujar sobre ella) y la máscara binaria como enteros de 8 bits.")]),

        (3, "Mallas de Coordenadas, Momento Espacial y Centroide",
         [(38, 'def obtener_coordenadas(binaria):'),
          (39, '    filas, columnas = np.indices(binaria.shape, dtype=np.float64)'),
          (40, '    return columnas, filas'),
          (43, 'def momento_espacial(binaria, p, q):'),
          (44, '    x, y = obtener_coordenadas(binaria)'),
          (45, '    f = binaria.astype(np.float64)'),
          (46, '    return float(np.sum((x ** p) * (y ** q) * f))'),
          (49, 'def centroide_por_momentos(binaria):'),
          (50, '    m00 = momento_espacial(binaria, 0, 0)'),
          (51, '    if m00 == 0:'),
          (52, '        raise ValueError("La imagen no contiene ningún objeto (m00 = 0).")'),
          (53, '    return momento_espacial(binaria, 1, 0) / m00, momento_espacial(binaria, 0, 1) / m00')],
         [("38-40", "<code>np.indices</code> genera dos matrices del mismo tamaño que la imagen: una con el número de fila (coordenada <i>y</i>) y otra con el de columna (coordenada <i>x</i>) de cada píxel. Se usan en coma flotante para evitar desbordamientos al elevar a potencias."),
          ("43-46", "Implementa el momento espacial de orden (p+q): m<sub>pq</sub> = &#931;&#931; x<super>p</super> y<super>q</super> f(x,y). La multiplicación elemento a elemento y <code>np.sum</code> sustituyen a los dos bucles anidados de la fórmula."),
          ("49-50", "m<sub>00</sub> es la suma de todos los píxeles del objeto, es decir, su <b>área</b>."),
          ("51-52", "Evita una división por cero si la imagen no contiene ningún objeto."),
          ("53", "Devuelve el centroide (x<sub>c</sub>, y<sub>c</sub>) = (m<sub>10</sub>/m<sub>00</sub>, m<sub>01</sub>/m<sub>00</sub>), el 'centro de masa' de la figura.")]),

        (4, "Momento Central y Momento Central Normalizado",
         [(56, 'def momento_central(binaria, p, q):'),
          (57, '    x, y = obtener_coordenadas(binaria)'),
          (58, '    f = binaria.astype(np.float64)'),
          (59, '    x_c, y_c = centroide_por_momentos(binaria)'),
          (60, '    return float(np.sum(((x - x_c) ** p) * ((y - y_c) ** q) * f))'),
          (63, 'def momento_central_normalizado(binaria, p, q):'),
          (64, '    mu00 = momento_central(binaria, 0, 0)'),
          (65, '    gamma = (p + q) / 2.0 + 1.0'),
          (66, '    return momento_central(binaria, p, q) / (mu00 ** gamma)')],
         [("56-59", "Obtiene las coordenadas, la imagen en flotante y el centroide del objeto."),
          ("60", "Momento central: mu<sub>pq</sub> = &#931;&#931; (x - x<sub>c</sub>)<super>p</super> (y - y<sub>c</sub>)<super>q</super> f(x,y). Al medir respecto del centroide, el resultado es <b>invariante a la traslación</b>."),
          ("63-64", "mu<sub>00</sub> coincide con m<sub>00</sub> (el área) y se usa como factor de escala."),
          ("65", "Exponente de normalización gamma = (p+q)/2 + 1, definido por la teoría de momentos."),
          ("66", "Momento central normalizado: eta<sub>pq</sub> = mu<sub>pq</sub> / mu<sub>00</sub><super>gamma</super>. La división hace al descriptor <b>invariante a la escala</b> además de a la traslación.")]),

        (5, "Marcado del Centroide sobre la Imagen Ampliada",
         [(69, 'def dibujar_cruz(img_bgr, x, y, escala, color, tipo=cv2.MARKER_CROSS, tam=40, grosor=2):'),
          (70, '    punto = (int(round((x + 0.5) * escala)), int(round((y + 0.5) * escala)))'),
          (71, '    cv2.drawMarker(img_bgr, punto, color, markerType=tipo,'),
          (72, '                   markerSize=tam, thickness=grosor, line_type=cv2.LINE_AA)')],
         [("69", "Función auxiliar para dibujar un marcador en la posición del centroide, con color, forma, tamaño y grosor configurables."),
          ("70", "Convierte la coordenada del píxel original a la imagen ampliada. Se suma 0.5 para ubicar la marca en el <b>centro</b> del píxel (cada píxel original ocupa un cuadrado de <i>escala x escala</i>)."),
          ("71-72", "<code>cv2.drawMarker</code> dibuja la cruz con antialiasing (<code>LINE_AA</code>) para bordes suaves.")]),

        (6, "Inciso a) Área y Centroide de la Figura 1.a",
         [(78, 'def analizar_figura_1a(ruta, escala=5):'),
          (79, '    img_bgr, binaria = cargar_imagen_binaria(ruta)'),
          (82, '    area = int(np.count_nonzero(binaria))'),
          (85, '    ys, xs = np.nonzero(binaria)'),
          (86, '    cx_geo, cy_geo = float(xs.mean()), float(ys.mean())'),
          (89, '    m00 = momento_espacial(binaria, 0, 0)'),
          (90, '    m10 = momento_espacial(binaria, 1, 0)'),
          (91, '    m01 = momento_espacial(binaria, 0, 1)'),
          (92, '    cx_mom, cy_mom = m10 / m00, m01 / m00'),
          (95, '    M = cv2.moments(binaria, binaryImage=True)'),
          (96, '    cx_cv, cy_cv = M["m10"] / M["m00"], M["m01"] / M["m00"]'),
          (99, '    img_marcada = cv2.resize(img_bgr, None, fx=escala, fy=escala,'),
          (100, '                             interpolation=cv2.INTER_NEAREST)'),
          (102, '    dibujar_cruz(img_marcada, cx_geo, cy_geo, escala, (255, 80, 0),'),
          (103, '                 cv2.MARKER_CROSS, tam=50, grosor=3)'),
          (104, '    dibujar_cruz(img_marcada, cx_mom, cy_mom, escala, (0, 0, 0),'),
          (105, '                 cv2.MARKER_TILTED_CROSS, tam=30, grosor=2)'),
          (107, '    print("\\n--- a) Figura 1.a: Área y Centroides ---")'),
          (108, '    print(f"  Área (píxeles del objeto):        {area}")'),
          (114, '    return {'),
          (115, '        "area": area,'),
          (116, '        "centroide": (cx_geo, cy_geo),'),
          (117, '        "centroide_momentos": (cx_mom, cy_mom),'),
          (120, '        "imagen_marcada": cv2.cvtColor(img_marcada, cv2.COLOR_BGR2RGB),'),
          (122, '    }')],
         [("78-79", "Carga la Figura 1.a y obtiene su versión binaria. El parámetro <code>escala=5</code> define cuánto se ampliará para visualizarla."),
          ("82", "Área = cantidad de píxeles con valor 1, contados con <code>np.count_nonzero</code>."),
          ("85-86", "<b>Centroide geométrico:</b> <code>np.nonzero</code> devuelve las coordenadas (filas, columnas) de los píxeles del objeto; su promedio es el centro geométrico."),
          ("89-92", "<b>Centroide por momentos:</b> se calculan m<sub>00</sub>, m<sub>10</sub> y m<sub>01</sub> con la función propia y se aplica x<sub>c</sub> = m<sub>10</sub>/m<sub>00</sub>, y<sub>c</sub> = m<sub>01</sub>/m<sub>00</sub>. Ambos métodos deben coincidir."),
          ("95-96", "Validación cruzada con <code>cv2.moments</code> de OpenCV (con <code>binaryImage=True</code> trata todo valor distinto de 0 como 1)."),
          ("99-100", "Amplía la imagen 5 veces con <code>INTER_NEAREST</code> (vecino más cercano) para conservar los bordes nítidos de cada píxel y poder ver bien las marcas."),
          ("102-105", "Dibuja el centroide geométrico con una cruz azul (BGR = (255, 80, 0)) y el centroide por momentos con un aspa negra más pequeña; si se superponen, se confirma que ambos coinciden."),
          ("107-112", "Imprime en consola el área, los momentos y los tres centroides con 4 decimales."),
          ("114-122", "Devuelve un diccionario con todos los resultados. La imagen marcada se convierte de BGR a RGB porque Matplotlib espera el orden RGB.")]),

        (7, "Inciso b) Momentos de Orden p=2, q=3 (Figura 1.b)",
         [(128, 'def momentos_figura_1b(ruta, p=2, q=3, escala=5):'),
          (129, '    img_bgr, binaria = cargar_imagen_binaria(ruta)'),
          (131, '    m_pq = momento_espacial(binaria, p, q)'),
          (132, '    mu_pq = momento_central(binaria, p, q)'),
          (133, '    eta_pq = momento_central_normalizado(binaria, p, q)'),
          (134, '    cx, cy = centroide_por_momentos(binaria)'),
          (137, '    M = cv2.moments(binaria, binaryImage=True)'),
          (138, '    validacion = {'),
          (139, '        "m21": (momento_espacial(binaria, 2, 1), M["m21"]),'),
          (140, '        "mu21": (momento_central(binaria, 2, 1), M["mu21"]),'),
          (141, '        "nu21": (momento_central_normalizado(binaria, 2, 1), M["nu21"]),'),
          (142, '    }'),
          (144, '    img_marcada = cv2.resize(img_bgr, None, fx=escala, fy=escala,'),
          (145, '                             interpolation=cv2.INTER_NEAREST)'),
          (146, '    dibujar_cruz(img_marcada, cx, cy, escala, (0, 0, 255), tam=40, grosor=3)'),
          (148, '    print(f"\\n--- b) Figura 1.b: Momentos de orden p={p}, q={q} ---")'),
          (154, '    for nombre, (propio, opencv) in validacion.items():'),
          (155, '        print(f"    {nombre:<5} propio = {propio: .6e}   OpenCV = {opencv: .6e}")'),
          (157, '    return {'),
          (158, '        "p": p, "q": q,'),
          (159, '        "m": m_pq, "mu": mu_pq, "eta": eta_pq,'),
          (164, '    }')],
         [("128-129", "Carga la Figura 1.b. Los parámetros por defecto p=2 y q=3 corresponden al orden pedido en el enunciado (orden total 5)."),
          ("131-133", "Calcula los tres descriptores solicitados: momento espacial m<sub>23</sub>, momento central mu<sub>23</sub> y momento central normalizado eta<sub>23</sub>."),
          ("134", "Calcula el centroide, necesario para el momento central y para marcarlo en la imagen."),
          ("137-142", "<code>cv2.moments</code> solo calcula momentos hasta orden 3, por lo que m<sub>23</sub> no puede compararse directamente. Por eso se valida la implementación propia con el orden (2,1): si m<sub>21</sub>, mu<sub>21</sub> y nu<sub>21</sub> coinciden con OpenCV, las mismas funciones son correctas para (2,3)."),
          ("144-146", "Amplía la imagen y marca el centroide con una cruz roja (BGR = (0, 0, 255))."),
          ("148-155", "Imprime los momentos en notación científica (<code>.6e</code>), ya que los momentos de orden alto alcanzan valores muy grandes, y muestra la tabla de validación."),
          ("157-164", "Devuelve los resultados, la validación y la imagen marcada en RGB.")]),

        (8, "Inciso c) Momentos Invariantes de Hu (Figura 1.c)",
         [(170, 'def momentos_hu_figura_1c(ruta, escala=3):'),
          (171, '    img_bgr, binaria = cargar_imagen_binaria(ruta)'),
          (173, '    eta = {f"eta{p}{q}": momento_central_normalizado(binaria, p, q)'),
          (174, '           for p, q in [(2, 0), (0, 2), (1, 1), (3, 0), (1, 2), (2, 1), (0, 3)]}'),
          (176, '    h1 = eta["eta20"] + eta["eta02"]'),
          (177, '    h2 = (eta["eta20"] - eta["eta02"]) ** 2 + 4 * eta["eta11"] ** 2'),
          (178, '    h3 = (eta["eta30"] - 3 * eta["eta12"]) ** 2 + (3 * eta["eta21"] - eta["eta03"]) ** 2'),
          (180, '    hu_cv = cv2.HuMoments(cv2.moments(binaria, binaryImage=True)).flatten()[:3]'),
          (182, '    img_ampliada = cv2.resize(img_bgr, None, fx=escala, fy=escala,'),
          (183, '                              interpolation=cv2.INTER_NEAREST)'),
          (185, '    print("\\n--- c) Figura 1.c: Momentos invariantes de Hu ---")'),
          (186, '    for i, (propio, opencv) in enumerate(zip((h1, h2, h3), hu_cv), start=1):'),
          (187, '        print(f"  H{i}: propio = {propio:.6e}   OpenCV = {opencv:.6e}")'),
          (189, '    return {'),
          (190, '        "hu": (h1, h2, h3),'),
          (191, '        "hu_opencv": tuple(float(v) for v in hu_cv),'),
          (195, '    }')],
         [("170-171", "Carga y binariza la Figura 1.c."),
          ("173-174", "Comprensión de diccionario que calcula los 7 momentos centrales normalizados de orden 2 y 3 necesarios para las fórmulas de Hu, con claves como <code>'eta20'</code>, <code>'eta11'</code>, etc."),
          ("176", "<b>H1</b> = eta<sub>20</sub> + eta<sub>02</sub>: mide la dispersión total del objeto respecto de su centroide."),
          ("177", "<b>H2</b> = (eta<sub>20</sub> - eta<sub>02</sub>)<super>2</super> + 4 eta<sub>11</sub><super>2</super>: mide la elongación (alargamiento) de la figura."),
          ("178", "<b>H3</b> = (eta<sub>30</sub> - 3 eta<sub>12</sub>)<super>2</super> + (3 eta<sub>21</sub> - eta<sub>03</sub>)<super>2</super>: mide la asimetría de la figura. Los tres son invariantes a traslación, escala y rotación."),
          ("180", "Calcula los 7 momentos de Hu con OpenCV, los aplana a un vector 1D y se queda con los 3 primeros para compararlos."),
          ("182-183", "Amplía la figura x3 para su visualización."),
          ("185-187", "Imprime cada H<sub>i</sub> propio junto al valor de OpenCV para verificar la implementación."),
          ("189-195", "Devuelve los momentos de Hu propios y de OpenCV, los eta utilizados y la imagen en RGB.")]),

        (9, "Panel de Texto y Configuración de la Figura",
         [(201, 'def _panel_texto(ax, titulo, texto):'),
          (203, '    ax.axis("off")'),
          (204, '    ax.set_title(titulo, fontsize=12, fontweight="bold")'),
          (205, '    ax.text(0.02, 0.95, texto, transform=ax.transAxes, va="top", ha="left",'),
          (206, '            family="monospace", fontsize=10.5,'),
          (207, '            bbox=dict(boxstyle="round,pad=0.8", facecolor="#f4f6fb", edgecolor="#c9d1e3"))'),
          (210, 'def graficar_resultados(res_a, res_b, res_c, ruta_salida=None, mostrar=True):'),
          (211, '    fig, axes = plt.subplots(3, 2, figsize=(15, 15),'),
          (212, '                             gridspec_kw={"width_ratios": [1.1, 1]})'),
          (213, '    fig.suptitle("Ejercicio 1: Momentos y Centroides", fontsize=16, fontweight="bold")')],
         [("201-204", "Función auxiliar que convierte un eje de Matplotlib en un panel de texto: oculta los ejes y coloca un título en negrita."),
          ("205-207", "Escribe el texto en la esquina superior izquierda (coordenadas relativas al eje con <code>transAxes</code>), con fuente monoespaciada para alinear columnas y dentro de una caja redondeada de fondo gris azulado."),
          ("210-212", "Crea una cuadrícula de 3 filas (una por inciso) x 2 columnas (imagen | resultados), donde la columna de la imagen es un 10% más ancha."),
          ("213", "Título general de la figura.")]),

        (10, "Composición de los Tres Incisos y Guardado",
         [(216, '    axes[0, 0].imshow(res_a["imagen_marcada"])'),
          (223, '    _panel_texto(axes[0, 1], "a) Área y Centroide", ('),
          (234, '    axes[1, 0].imshow(res_b["imagen_marcada"])'),
          (238, '    texto_val = "\\n".join(f"  {k:<5} propio={v[0]: .4e}  cv2={v[1]: .4e}"'),
          (239, '                          for k, v in res_b["validacion"].items())'),
          (240, '    _panel_texto(axes[1, 1], f"b) Momentos de orden p={p}, q={q}", ('),
          (248, '    axes[2, 0].imshow(res_c["imagen"])'),
          (251, '    texto_hu = "\\n".join('),
          (252, '        f"H{i} = {h:.6e}   (cv2: {hc:.6e})"'),
          (253, '        for i, (h, hc) in enumerate(zip(res_c["hu"], res_c["hu_opencv"]), start=1))'),
          (255, '    _panel_texto(axes[2, 1], "c) Momentos invariantes de Hu", ('),
          (259, '    plt.tight_layout(rect=[0, 0, 1, 0.97])'),
          (260, '    if ruta_salida:'),
          (261, '        plt.savefig(ruta_salida, dpi=150, bbox_inches="tight")'),
          (263, '    if mostrar:'),
          (264, '        plt.show()'),
          (265, '    return fig')],
         [("216-230", "Fila 1 (inciso a): muestra la Figura 1.a con los dos centroides marcados y, a la derecha, el área, los momentos m<sub>00</sub>, m<sub>10</sub>, m<sub>01</sub> y los centroides geométrico, por momentos y de OpenCV."),
          ("233-245", "Fila 2 (inciso b): muestra la Figura 1.b con su centroide y un panel con m<sub>23</sub>, mu<sub>23</sub>, eta<sub>23</sub> y la tabla de validación de orden (2,1) generada con <code>join</code>."),
          ("248-257", "Fila 3 (inciso c): muestra la Figura 1.c y un panel con H1, H2 y H3 (propios y de OpenCV) más los momentos normalizados usados."),
          ("259", "Ajusta automáticamente los espacios entre subplots, reservando el 3% superior para el título."),
          ("260-265", "Si se indicó una ruta, guarda la figura a 150 DPI; si <code>mostrar</code> es verdadero, abre la ventana interactiva. Devuelve la figura para posible reutilización.")]),

        (11, "Programa Principal",
         [(271, 'if __name__ == "__main__":'),
          (272, '    print("=" * 60)'),
          (273, '    print("  EJERCICIO 1: Cálculo de Momentos y Centroides")'),
          (276, '    resultado_a = analizar_figura_1a(RUTA_FIGURA_1A)'),
          (277, '    resultado_b = momentos_figura_1b(RUTA_FIGURA_1B, p=2, q=3)'),
          (278, '    resultado_c = momentos_hu_figura_1c(RUTA_FIGURA_1C)'),
          (280, '    graficar_resultados(resultado_a, resultado_b, resultado_c, ruta_salida=RUTA_SALIDA)'),
          (282, '    print("\\n" + "=" * 60)'),
          (283, '    print("  Ejercicio 1 completado exitosamente.")')],
         [("271", "El bloque solo se ejecuta al correr el archivo directamente, no al importarlo como módulo (lo que permite reutilizar sus funciones)."),
          ("272-274", "Imprime el encabezado del ejercicio."),
          ("276-278", "Ejecuta en orden los tres incisos: a) área y centroide, b) momentos de orden (2,3) y c) momentos de Hu."),
          ("280", "Genera y guarda la figura comparativa con los tres resultados."),
          ("282-284", "Imprime el mensaje de finalización.")])
    ]
    render_section(1, "Cálculo de Momentos y Centroides", "ejercicio_1.py", ej1_blocks)
    render_resultados([("ejercicio_1_resultado.png", "Figura 1. Resultados de los incisos a), b) y c) del Ejercicio 1")])

    # ==================== EJERCICIO 2 DATA ====================
    ej2_blocks = [
        (1, "Importaciones, Rutas y Paleta de Colores",
         [(1, 'import os'),
          (3, 'from PIL import Image, ImageDraw, ImageFont, ImageStat'),
          (5, 'directorio = os.path.dirname(os.path.abspath(__file__))'),
          (10, 'RUTA_IMAGEN_A = os.path.join(directorio, "mono.png")'),
          (11, 'RUTA_SALIDA = os.path.join(directorio, "ejercicio_2_resultado.png")'),
          (14, 'COLOR_FONDO = (243, 245, 250)'),
          (15, 'COLOR_PANEL = (255, 255, 255)'),
          (16, 'COLOR_BORDE = (214, 219, 230)'),
          (17, 'COLOR_TEXTO = (35, 40, 55)'),
          (18, 'COLOR_SECUNDARIO = (110, 118, 135)'),
          (19, 'COLOR_GRILLA = (232, 235, 242)'),
          (20, 'COLORES_CANAL = {'),
          (21, '    "Gris": (70, 75, 90),'),
          (22, '    "R": (226, 61, 74),'),
          (23, '    "G": (46, 168, 96),'),
          (24, '    "B": (52, 110, 230),'),
          (25, '}')],
         [("1", "Importa <code>os</code> para el manejo de rutas."),
          ("3", "Importa los cuatro módulos de Pillow utilizados: <code>Image</code> (carga y lienzo), <code>ImageDraw</code> (dibujo 2D), <code>ImageFont</code> (tipografías) e <code>ImageStat</code> (estadísticas). No se usa Matplotlib: todo el gráfico se construye con PIL."),
          ("5", "Directorio del script, base para las rutas relativas."),
          ("10-11", "Ruta de la imagen de entrada \"a\" (<i>mono.png</i>) y del PNG de salida."),
          ("14-19", "Paleta de colores RGB de la interfaz: fondo general, paneles, bordes, texto principal, texto secundario y líneas de la grilla."),
          ("20-25", "Diccionario con el color asignado a cada histograma: gris oscuro, rojo, verde y azul.")]),

        (2, "Carga de la Imagen y Cálculo de los Histogramas",
         [(31, 'def cargar_imagen(ruta):'),
          (32, '    if not os.path.isfile(ruta):'),
          (33, '        raise FileNotFoundError(f"No se encontró la imagen: {ruta}")'),
          (34, '    return Image.open(ruta).convert("RGB")'),
          (37, 'def calcular_histogramas(img_rgb):'),
          (38, '    hist_gris = img_rgb.convert("L").histogram()'),
          (39, '    hist_rgb = img_rgb.histogram()'),
          (41, '    histogramas = {'),
          (42, '        "Gris": hist_gris,'),
          (43, '        "R": hist_rgb[0:256],'),
          (44, '        "G": hist_rgb[256:512],'),
          (45, '        "B": hist_rgb[512:768],'),
          (46, '    }'),
          (49, '    total = img_rgb.width * img_rgb.height'),
          (50, '    for nombre, hist in histogramas.items():'),
          (51, '        assert sum(hist) == total, f"El histograma {nombre} no suma {total}"'),
          (53, '    return histogramas')],
         [("31-34", "Verifica que el archivo exista y lo abre forzando el modo RGB (así funciona igual con imágenes en paleta, RGBA o escala de grises)."),
          ("38", "Convierte a escala de grises (modo 'L', luminancia ITU-R 601-2) y obtiene su histograma: una lista de 256 frecuencias, una por nivel de intensidad."),
          ("39", "En una imagen RGB, <code>histogram()</code> devuelve una única lista de 768 valores: los 256 niveles de R, seguidos por los de G y luego los de B."),
          ("41-46", "Organiza los cuatro histogramas en un diccionario, separando la lista RGB en tramos [0:256], [256:512] y [512:768]."),
          ("49-51", "Control de calidad: la suma de las frecuencias de cada histograma debe ser exactamente el total de píxeles (ancho x alto); si no, <code>assert</code> detiene el programa."),
          ("53", "Devuelve el diccionario de histogramas.")]),

        (3, "Estadísticas Descriptivas con ImageStat",
         [(56, 'def calcular_estadisticas(img_rgb):'),
          (57, '    est_gris = ImageStat.Stat(img_rgb.convert("L"))'),
          (58, '    est_rgb = ImageStat.Stat(img_rgb)'),
          (60, '    estadisticas = {}'),
          (61, '    for i, canal in enumerate(["Gris", "R", "G", "B"]):'),
          (62, '        est, k = (est_gris, 0) if canal == "Gris" else (est_rgb, i - 1)'),
          (63, '        estadisticas[canal] = {'),
          (64, '            "media": est.mean[k],'),
          (65, '            "desv": est.stddev[k],'),
          (66, '            "mediana": est.median[k],'),
          (67, '            "min": est.extrema[k][0],'),
          (68, '            "max": est.extrema[k][1],'),
          (69, '        }'),
          (70, '    return estadisticas')],
         [("57-58", "<code>ImageStat.Stat</code> calcula estadísticas por banda: una para la imagen en gris (1 banda) y otra para la RGB (3 bandas)."),
          ("61-62", "Recorre los cuatro canales; para 'Gris' usa la banda 0 de <code>est_gris</code> y para R, G, B usa las bandas 0, 1 y 2 de <code>est_rgb</code> (índice <code>i - 1</code>)."),
          ("63-69", "Guarda la media (brillo promedio), la desviación estándar (contraste), la mediana y los valores mínimo y máximo (<code>extrema</code>) de cada canal."),
          ("70", "Devuelve el diccionario de estadísticas, usado en los subtítulos de los paneles y en la tabla de consola.")]),

        (4, "Carga de Fuentes Tipográficas",
         [(76, 'def cargar_fuente(tamano, negrita=False):'),
          (78, '    candidatos = (["arialbd.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"] if negrita'),
          (79, '                  else ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"])'),
          (80, '    for nombre in candidatos:'),
          (81, '        try:'),
          (82, '            return ImageFont.truetype(nombre, tamano)'),
          (83, '        except OSError:'),
          (84, '            continue'),
          (85, '    try:'),
          (86, '        return ImageFont.load_default(size=tamano)'),
          (87, '    except TypeError:'),
          (88, '        return ImageFont.load_default()'),
          (91, 'FUENTE_TITULO = cargar_fuente(28, negrita=True)'),
          (92, 'FUENTE_PANEL = cargar_fuente(17, negrita=True)'),
          (93, 'FUENTE_TEXTO = cargar_fuente(13)'),
          (94, 'FUENTE_TICKS = cargar_fuente(12)')],
         [("76-79", "Lista de fuentes TrueType candidatas (Arial y Segoe UI en Windows, DejaVu en Linux), en versión negrita o normal según el parámetro."),
          ("80-84", "Intenta cargar cada fuente en orden; si no está instalada, <code>truetype</code> lanza <code>OSError</code> y se prueba la siguiente."),
          ("85-88", "Si ninguna existe, usa la fuente por defecto de PIL. Las versiones antiguas de Pillow no aceptan el parámetro <code>size</code> (<code>TypeError</code>), por lo que se carga sin él."),
          ("91-94", "Crea las cuatro fuentes globales: título principal (28 px), títulos de panel (17 px), texto general (13 px) y números de los ejes (12 px).")]),

        (5, "Utilidades: Formato Numérico y Texto Vertical",
         [(97, 'def _formato_numero(valor):'),
          (99, '    if valor >= 1_000_000:'),
          (100, '        return f"{valor / 1_000_000:.1f}M"'),
          (101, '    if valor >= 1_000:'),
          (102, '        return f"{valor / 1_000:.1f}k"'),
          (103, '    return f"{int(valor)}"'),
          (106, 'def _texto_vertical(lienzo, texto, centro, fuente, color):'),
          (108, '    caja = fuente.getbbox(texto)'),
          (109, '    ancho, alto = caja[2] - caja[0] + 4, caja[3] - caja[1] + 6'),
          (110, '    capa = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))'),
          (111, '    ImageDraw.Draw(capa).text((2 - caja[0], 2 - caja[1]), texto, font=fuente, fill=color)'),
          (112, '    capa = capa.rotate(90, expand=True)'),
          (113, '    lienzo.paste(capa, (int(centro[0] - capa.width / 2), int(centro[1] - capa.height / 2)), capa)')],
         [("97-103", "Abrevia las frecuencias grandes del eje Y: por ejemplo, 12500 se muestra como \"12.5k\" y 2300000 como \"2.3M\", para que las etiquetas no ocupen demasiado espacio."),
          ("106-109", "PIL no puede escribir texto rotado directamente; por eso se mide el texto con <code>getbbox</code> para conocer su tamaño exacto."),
          ("110-111", "Crea una capa RGBA transparente del tamaño del texto y escribe el texto en ella."),
          ("112", "Rota la capa 90° en sentido antihorario; <code>expand=True</code> ajusta el tamaño para no recortar el texto."),
          ("113", "Pega la capa centrada en la posición indicada, usando la propia capa como máscara para respetar la transparencia. Se usa para la etiqueta del eje Y.")]),

        (6, "Panel Base con Sombra y Bordes Redondeados",
         [(116, 'def dibujar_panel(lienzo, caja, titulo, subtitulo=None):'),
          (118, '    draw = ImageDraw.Draw(lienzo, "RGBA")'),
          (119, '    x0, y0, x1, _ = caja'),
          (121, '    draw.rounded_rectangle((x0 + 3, y0 + 4, caja[2] + 3, caja[3] + 4), radius=14, fill=(0, 0, 0, 18))'),
          (122, '    draw.rounded_rectangle(caja, radius=14, fill=COLOR_PANEL, outline=COLOR_BORDE, width=1)'),
          (123, '    draw.text((x0 + 20, y0 + 14), titulo, font=FUENTE_PANEL, fill=COLOR_TEXTO)'),
          (124, '    if subtitulo:'),
          (125, '        ancho_sub = draw.textlength(subtitulo, font=FUENTE_TEXTO)'),
          (126, '        draw.text((x1 - 20 - ancho_sub, y0 + 17), subtitulo, font=FUENTE_TEXTO, fill=COLOR_SECUNDARIO)')],
         [("116-119", "Crea un objeto de dibujo en modo RGBA (permite colores semitransparentes) y desempaqueta las coordenadas de la caja del panel."),
          ("121", "Dibuja una <b>sombra</b>: un rectángulo redondeado negro con opacidad 18/255, desplazado 3 px a la derecha y 4 px hacia abajo."),
          ("122", "Dibuja el panel blanco con esquinas redondeadas (radio 14) y un borde gris claro."),
          ("123", "Escribe el título del panel en la esquina superior izquierda."),
          ("124-126", "Si hay subtítulo (las estadísticas del canal), mide su ancho con <code>textlength</code> y lo alinea a la derecha del panel.")]),

        (7, "Dibujo del Histograma (I): Área de Gráfico y Grilla",
         [(129, 'def dibujar_histograma(lienzo, caja, series, titulo, subtitulo=None, modo="barras"):'),
          (130, '    dibujar_panel(lienzo, caja, titulo, subtitulo)'),
          (131, '    draw = ImageDraw.Draw(lienzo, "RGBA")'),
          (133, '    x0, y0, x1, y1 = caja'),
          (134, '    gx0, gy0, gx1, gy1 = x0 + 78, y0 + 52, x1 - 24, y1 - 62'),
          (135, '    ancho, alto = gx1 - gx0, gy1 - gy0'),
          (136, '    max_valor = max(max(h) for h, _ in series) or 1'),
          (139, '    for i in range(5):'),
          (140, '        y = gy1 - alto * i / 4'),
          (141, '        draw.line([(gx0, y), (gx1, y)], fill=COLOR_GRILLA, width=1)'),
          (142, '        etiqueta = _formato_numero(max_valor * i / 4)'),
          (143, '        tw = draw.textlength(etiqueta, font=FUENTE_TICKS)'),
          (144, '        draw.text((gx0 - 10 - tw, y - 7), etiqueta, font=FUENTE_TICKS, fill=COLOR_SECUNDARIO)')],
         [("129-131", "Función principal de graficado. Recibe una lista de <code>series</code> (pares histograma-color) y el <code>modo</code>: 'barras' para un canal o 'linea' para superponer varios. Primero dibuja el panel base."),
          ("133-135", "Define el área útil del gráfico dentro del panel, dejando márgenes para las etiquetas del eje Y (78 px), el título (52 px) y el eje X (62 px)."),
          ("136", "Frecuencia máxima entre todas las series, usada para escalar verticalmente. El <code>or 1</code> evita dividir por cero en una imagen vacía."),
          ("139-141", "Dibuja 5 líneas horizontales de grilla (0%, 25%, 50%, 75% y 100% del máximo). En imagen, el eje Y crece hacia abajo, por eso se resta desde <code>gy1</code>."),
          ("142-144", "Escribe el valor de frecuencia de cada línea, alineado a la derecha del eje Y.")]),

        (8, "Dibujo del Histograma (II): Barras o Curvas Rellenas",
         [(147, '    paso = ancho / 256'),
          (148, '    for hist, color in series:'),
          (149, '        if modo == "barras":'),
          (150, '            for nivel, valor in enumerate(hist):'),
          (151, '                if valor == 0:'),
          (152, '                    continue'),
          (153, '                bx0 = gx0 + nivel * paso'),
          (154, '                by = gy1 - alto * valor / max_valor'),
          (155, '                draw.rectangle([bx0, by, bx0 + max(paso - 0.6, 1), gy1], fill=color + (235,))'),
          (156, '        else:'),
          (157, '            puntos = [(gx0 + ancho * n / 255, gy1 - alto * v / max_valor) for n, v in enumerate(hist)]'),
          (158, '            draw.polygon([(gx0, gy1)] + puntos + [(gx1, gy1)], fill=color + (55,))'),
          (159, '            draw.line(puntos, fill=color + (255,), width=2, joint="curve")')],
         [("147", "Ancho horizontal asignado a cada uno de los 256 niveles de intensidad."),
          ("148-152", "Recorre cada serie. En modo barras, recorre los 256 niveles y omite los que tienen frecuencia 0."),
          ("153-154", "Calcula la posición x de la barra según su nivel y la altura proporcional a su frecuencia respecto del máximo."),
          ("155", "Dibuja la barra como un rectángulo desde la altura calculada hasta la base, dejando una pequeña separación (0.6 px) entre barras y con opacidad 235/255."),
          ("157", "En modo línea, convierte cada par (nivel, frecuencia) en un punto (x, y) del gráfico."),
          ("158", "Cierra la curva con las esquinas inferiores y la rellena con el color del canal muy transparente (55/255), de modo que las tres curvas RGB se vean superpuestas."),
          ("159", "Traza la curva encima con trazo opaco de 2 px y uniones suavizadas (<code>joint='curve'</code>).")]),

        (9, "Dibujo del Histograma (III): Ejes, Gradiente y Etiquetas",
         [(162, '    draw.line([(gx0, gy0), (gx0, gy1), (gx1, gy1)], fill=COLOR_TEXTO, width=2)'),
          (165, '    color_ref = series[0][1] if len(series) == 1 else (255, 255, 255)'),
          (166, '    for i in range(int(ancho) + 1):'),
          (167, '        t = i / ancho'),
          (168, '        c = tuple(int(t * comp) for comp in color_ref)'),
          (169, '        draw.line([(gx0 + i, gy1 + 4), (gx0 + i, gy1 + 12)], fill=c)'),
          (172, '    for nivel in (0, 32, 64, 96, 128, 160, 192, 224, 255):'),
          (173, '        x = gx0 + ancho * nivel / 255'),
          (174, '        draw.line([(x, gy1 + 12), (x, gy1 + 17)], fill=COLOR_TEXTO, width=1)'),
          (175, '        etiqueta = str(nivel)'),
          (176, '        tw = draw.textlength(etiqueta, font=FUENTE_TICKS)'),
          (177, '        draw.text((x - tw / 2, gy1 + 19), etiqueta, font=FUENTE_TICKS, fill=COLOR_SECUNDARIO)'),
          (180, '    etiqueta_x = "Nivel de intensidad"'),
          (181, '    tw = draw.textlength(etiqueta_x, font=FUENTE_TEXTO)'),
          (182, '    draw.text((gx0 + ancho / 2 - tw / 2, gy1 + 38), etiqueta_x, font=FUENTE_TEXTO, fill=COLOR_TEXTO)'),
          (183, '    _texto_vertical(lienzo, "Frecuencia (n.º de píxeles)", (x0 + 20, gy0 + alto / 2),'),
          (184, '                    FUENTE_TEXTO, COLOR_TEXTO)')],
         [("162", "Dibuja los ejes Y y X como una polilínea en forma de 'L'."),
          ("165-169", "Dibuja bajo el eje X una <b>barra de gradiente</b> que va de negro al color del canal (o a blanco si hay varias series), indicando visualmente qué intensidad representa cada posición."),
          ("172-177", "Coloca marcas y etiquetas del eje X cada 32 niveles (0, 32, ..., 224, 255), centradas bajo cada marca."),
          ("180-182", "Escribe el nombre del eje X, centrado."),
          ("183-184", "Escribe el nombre del eje Y rotado 90° usando la función auxiliar <code>_texto_vertical</code>.")]),

        (10, "Panel con la Imagen Original",
         [(187, 'def dibujar_imagen(lienzo, caja, img, titulo, subtitulo=None):'),
          (189, '    dibujar_panel(lienzo, caja, titulo, subtitulo)'),
          (190, '    x0, y0, x1, y1 = caja'),
          (191, '    max_w, max_h = (x1 - x0) - 40, (y1 - y0) - 70'),
          (192, '    factor = min(max_w / img.width, max_h / img.height)'),
          (193, '    miniatura = img.resize((int(img.width * factor), int(img.height * factor)), Image.LANCZOS)'),
          (194, '    px = x0 + ((x1 - x0) - miniatura.width) // 2'),
          (195, '    py = y0 + 52 + (max_h - miniatura.height) // 2'),
          (196, '    lienzo.paste(miniatura, (px, py))'),
          (197, '    ImageDraw.Draw(lienzo).rectangle((px - 1, py - 1, px + miniatura.width, py + miniatura.height),'),
          (198, '                                     outline=COLOR_BORDE)')],
         [("187-190", "Dibuja el panel base y obtiene sus coordenadas."),
          ("191-192", "Calcula el espacio disponible y el factor de escala que permite que la imagen quepa completa <b>sin deformarse</b> (se toma el menor de los dos cocientes)."),
          ("193", "Redimensiona la imagen con el filtro LANCZOS, de alta calidad."),
          ("194-196", "Calcula la posición para centrar la miniatura en el panel y la pega sobre el lienzo."),
          ("197-198", "Dibuja un marco fino alrededor de la imagen.")]),

        (11, "Lienzo General y Encabezado",
         [(201, 'def graficar_histograma(img_rgb, histogramas, estadisticas, ruta_salida=None, mostrar=True):'),
          (202, '    ancho_panel, alto_panel, margen, encabezado = 600, 400, 24, 90'),
          (203, '    ancho_total = 3 * ancho_panel + 4 * margen'),
          (204, '    alto_total = encabezado + 2 * alto_panel + 3 * margen'),
          (205, '    lienzo = Image.new("RGB", (ancho_total, alto_total), COLOR_FONDO)'),
          (207, '    draw = ImageDraw.Draw(lienzo)'),
          (208, '    draw.text((margen, 22), "Ejercicio 2: Histograma de la imagen \\"a\\" (PIL)",'),
          (209, '              font=FUENTE_TITULO, fill=COLOR_TEXTO)'),
          (210, '    draw.text((margen, 60), f"Tamaño: {img_rgb.width} x {img_rgb.height} px  ·  "'),
          (213, '              font=FUENTE_TEXTO, fill=COLOR_SECUNDARIO)'),
          (215, '    def caja(fila, col):'),
          (216, '        x = margen + col * (ancho_panel + margen)'),
          (217, '        y = encabezado + margen + fila * (alto_panel + margen)'),
          (218, '        return (x, y, x + ancho_panel, y + alto_panel)'),
          (220, '    def sub(canal):'),
          (221, '        e = estadisticas[canal]'),
          (222, '        return f"μ={e[\'media\']:.1f}  σ={e[\'desv\']:.1f}  med={e[\'mediana\']}"')],
         [("201-205", "Define una cuadrícula de 3 columnas x 2 filas de paneles de 600x400 px con márgenes de 24 px y un encabezado de 90 px, y crea el lienzo RGB con el color de fondo."),
          ("207-213", "Escribe el título principal y una línea con el tamaño de la imagen, el total de píxeles y el método utilizado."),
          ("215-218", "Función interna que calcula la caja (x0, y0, x1, y1) del panel ubicado en una fila y columna dadas."),
          ("220-222", "Función interna que arma el subtítulo de cada histograma con la media (mu), la desviación estándar (sigma) y la mediana del canal.")]),

        (12, "Distribución de los Seis Paneles y Guardado",
         [(224, '    dibujar_imagen(lienzo, caja(0, 0), img_rgb, "Imagen original \\"a\\"")'),
          (225, '    dibujar_histograma(lienzo, caja(0, 1), [(histogramas["Gris"], COLORES_CANAL["Gris"])],'),
          (226, '                       "Histograma – Escala de grises", sub("Gris"))'),
          (227, '    dibujar_histograma(lienzo, caja(0, 2),'),
          (228, '                       [(histogramas[c], COLORES_CANAL[c]) for c in ("R", "G", "B")],'),
          (229, '                       "Histograma RGB superpuesto", modo="linea")'),
          (230, '    for col, canal in enumerate(("R", "G", "B")):'),
          (231, '        nombre = {"R": "Rojo (R)", "G": "Verde (G)", "B": "Azul (B)"}[canal]'),
          (232, '        dibujar_histograma(lienzo, caja(1, col), [(histogramas[canal], COLORES_CANAL[canal])],'),
          (233, '                           f"Canal {nombre}", sub(canal))'),
          (235, '    if ruta_salida:'),
          (236, '        lienzo.save(ruta_salida)'),
          (237, '        print(f"\\nGráfica guardada como: {os.path.basename(ruta_salida)}")'),
          (238, '    if mostrar:'),
          (239, '        lienzo.show(title="Ejercicio 2 - Histograma (PIL)")'),
          (240, '    return lienzo')],
         [("224", "Panel (0,0): la imagen original \"a\"."),
          ("225-226", "Panel (0,1): histograma en escala de grises, dibujado como barras."),
          ("227-229", "Panel (0,2): las tres curvas R, G y B superpuestas en modo línea, para comparar la distribución de los canales."),
          ("230-233", "Fila inferior: un histograma de barras por cada canal (rojo, verde, azul), cada uno con su color y sus estadísticas."),
          ("235-237", "Guarda el lienzo como PNG si se indicó una ruta."),
          ("238-240", "Abre la imagen con el visor predeterminado del sistema y devuelve el lienzo.")]),

        (13, "Función Integradora y Programa Principal",
         [(246, 'def histograma_pil(ruta, ruta_salida=None, mostrar=True):'),
          (247, '    img = cargar_imagen(ruta)'),
          (248, '    print(f"\\nImagen: {os.path.basename(ruta)}")'),
          (249, '    print(f"  Tamaño: {img.width} x {img.height} píxeles  |  Modo: {img.mode}")'),
          (251, '    histogramas = calcular_histogramas(img)'),
          (252, '    estadisticas = calcular_estadisticas(img)'),
          (256, '    for canal, hist in histogramas.items():'),
          (257, '        e = estadisticas[canal]'),
          (258, '        moda = hist.index(max(hist))'),
          (262, '    lienzo = graficar_histograma(img, histogramas, estadisticas, ruta_salida, mostrar)'),
          (263, '    return histogramas, estadisticas, lienzo'),
          (266, 'if __name__ == "__main__":'),
          (271, '    histograma_pil(RUTA_IMAGEN_A, ruta_salida=RUTA_SALIDA)')],
         [("246-249", "Función que encadena todo el proceso: carga la imagen e imprime su nombre, tamaño y modo."),
          ("251-252", "Calcula los histogramas y las estadísticas."),
          ("254-260", "Imprime una tabla por canal con media, desviación, mediana, mínimo, máximo y la <b>moda</b>: el nivel con mayor frecuencia, obtenido con <code>hist.index(max(hist))</code>."),
          ("262-263", "Genera la gráfica y devuelve todos los resultados."),
          ("266-275", "Punto de entrada: imprime el encabezado, ejecuta el análisis de <i>mono.png</i> guardando el resultado y muestra el mensaje final.")])
    ]
    render_section(2, "Histograma de la Imagen \"a\" con PIL", "ejercicio_2.py", ej2_blocks)
    render_resultados([("ejercicio_2_resultado.png", "Figura 2. Histogramas en escala de grises y por canal R, G, B generados con PIL")])

    # ==================== EJERCICIO 3 DATA ====================
    ej3_blocks = [
        (1, "Importaciones, Rutas y Constantes",
         [(1, 'import os'),
          (3, 'import cv2'),
          (4, 'import numpy as np'),
          (5, 'import matplotlib.pyplot as plt'),
          (7, 'directorio = os.path.dirname(os.path.abspath(__file__))'),
          (12, 'RUTA_IMAGEN_B = os.path.join(directorio, "flores.png")'),
          (13, 'RUTA_SALIDA_CANALES = os.path.join(directorio, "ejercicio_3_canales.png")'),
          (14, 'RUTA_SALIDA_GRIS = os.path.join(directorio, "ejercicio_3_gris.png")'),
          (15, 'RUTA_IMAGEN_GRIS = os.path.join(directorio, "flores_gris.png")'),
          (17, 'NOMBRES_CANALES = ("Rojo (R)", "Verde (G)", "Azul (B)")'),
          (18, 'COLORES_HIST = ("#e23d4a", "#2ea860", "#346ee6")')],
         [("1-5", "Importa <code>os</code>, OpenCV, NumPy y Matplotlib."),
          ("7", "Directorio del script, base para las rutas."),
          ("12", "Ruta de la imagen de entrada \"b\" (<i>flores.png</i>)."),
          ("13-15", "Rutas de salida: figura de canales, figura comparativa de grises y la imagen convertida a gris en sí."),
          ("17-18", "Tuplas con los nombres de los canales y los colores hexadecimales usados en los histogramas, en el orden R, G, B.")]),

        (2, "Carga de la Imagen, Separación de Canales y Canal Teñido",
         [(21, 'def cargar_imagen_rgb(ruta):'),
          (22, '    img_bgr = cv2.imread(ruta, cv2.IMREAD_COLOR)'),
          (23, '    if img_bgr is None:'),
          (24, '        raise FileNotFoundError(f"No se pudo cargar la imagen: {ruta}")'),
          (25, '    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)'),
          (28, 'def separar_canales(img_rgb):'),
          (29, '    r, g, b = cv2.split(img_rgb)'),
          (30, '    return r, g, b'),
          (33, 'def canal_coloreado(canal, indice):'),
          (34, '    img = np.zeros((*canal.shape, 3), dtype=np.uint8)'),
          (35, '    img[:, :, indice] = canal'),
          (36, '    return img')],
         [("21-24", "Lee la imagen en color y verifica que se haya cargado correctamente."),
          ("25", "OpenCV almacena los canales en orden <b>BGR</b>; se convierten a <b>RGB</b> para que la separación y la visualización con Matplotlib sean correctas."),
          ("28-30", "<code>cv2.split</code> divide la matriz (alto x ancho x 3) en tres matrices 2D independientes, una por canal, con valores de 0 a 255."),
          ("33-34", "Crea una imagen RGB completamente negra del mismo tamaño que el canal (<code>*canal.shape</code> desempaqueta alto y ancho)."),
          ("35-36", "Copia el canal solo en su posición (0 = R, 1 = G, 2 = B), dejando los otros dos en 0. Así se visualiza el canal 'teñido' con su color puro.")]),

        (3, "Conversión a Escala de Grises (OpenCV y Manual)",
         [(39, 'def convertir_a_gris(img_rgb):'),
          (40, '    gris_opencv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)'),
          (42, '    r, g, b = [c.astype(np.float64) for c in separar_canales(img_rgb)]'),
          (43, '    gris_manual = np.clip(np.round(0.299 * r + 0.587 * g + 0.114 * b), 0, 255).astype(np.uint8)'),
          (45, '    return gris_opencv, gris_manual')],
         [("40", "Método 1: conversión nativa de OpenCV con <code>COLOR_RGB2GRAY</code>."),
          ("42", "Método 2 (manual): separa los canales y los convierte a coma flotante para evitar el desbordamiento de <code>uint8</code> al multiplicar y sumar."),
          ("43", "Aplica la fórmula de luminancia ITU-R BT.601: <b>Y = 0.299R + 0.587G + 0.114B</b>. Los pesos reflejan la sensibilidad del ojo humano (mayor al verde, menor al azul). El resultado se redondea, se limita a [0, 255] con <code>np.clip</code> y se convierte a <code>uint8</code>."),
          ("45", "Devuelve ambas versiones para compararlas.")]),

        (4, "Figura de Canales (I): Imagen Original e Histogramas",
         [(48, 'def graficar_canales(img_rgb, canales, ruta_salida=None):'),
          (49, '    fig, axes = plt.subplots(2, 4, figsize=(20, 9))'),
          (50, '    fig.suptitle("Ejercicio 3: Separación de los planos de color R, G, B",'),
          (51, '                 fontsize=16, fontweight="bold")'),
          (54, '    axes[0, 0].imshow(img_rgb)'),
          (55, '    axes[0, 0].set_title("Imagen original \\"b\\" (RGB)", fontsize=12, fontweight="bold")'),
          (56, '    axes[0, 0].axis("off")'),
          (59, '    max_interno = 0'),
          (60, '    for canal, nombre, color in zip(canales, NOMBRES_CANALES, COLORES_HIST):'),
          (61, '        hist = cv2.calcHist([canal], [0], None, [256], [0, 256]).ravel()'),
          (62, '        max_interno = max(max_interno, hist[1:255].max())'),
          (63, '        axes[1, 0].plot(hist, color=color, label=nombre, linewidth=1.4)'),
          (64, '        axes[1, 0].fill_between(range(256), hist, color=color, alpha=0.15)'),
          (65, '    axes[1, 0].set_title("Histograma por canal", fontsize=12, fontweight="bold")'),
          (66, '    axes[1, 0].set_xlim(0, 255)'),
          (69, '    axes[1, 0].set_ylim(0, max_interno * 1.15)'),
          (70, '    axes[1, 0].set_xlabel("Nivel de intensidad")'),
          (71, '    axes[1, 0].set_ylabel("Frecuencia")'),
          (72, '    axes[1, 0].legend()'),
          (73, '    axes[1, 0].grid(alpha=0.3)')],
         [("48-51", "Crea una figura de 2 filas x 4 columnas con su título general."),
          ("54-56", "Panel (0,0): imagen original sin ejes."),
          ("59-61", "Para cada canal calcula su histograma con <code>cv2.calcHist</code> (256 bins en el rango [0, 256)); <code>ravel()</code> lo convierte de (256, 1) a un vector 1D."),
          ("62", "Guarda el máximo de frecuencia <b>excluyendo los niveles 0 y 255</b>. Esos extremos suelen tener picos enormes por zonas saturadas o muy oscuras, que aplastarían el resto del histograma."),
          ("63-64", "Dibuja la curva de cada canal con su color y un relleno semitransparente (alpha = 0.15)."),
          ("65-66", "Título del panel y rango del eje X de 0 a 255."),
          ("69", "Limita el eje Y al máximo interno + 15%, de modo que la forma de la distribución se aprecie con claridad."),
          ("70-73", "Etiquetas de los ejes, leyenda con los nombres de los canales y grilla tenue.")]),

        (5, "Figura de Canales (II): Planos en Intensidad y Teñidos",
         [(76, '    for i, (canal, nombre) in enumerate(zip(canales, NOMBRES_CANALES)):'),
          (78, '        axes[0, i + 1].imshow(canal, cmap="gray", vmin=0, vmax=255)'),
          (79, '        axes[0, i + 1].set_title(f"Canal {nombre} – intensidad\\n"'),
          (80, '                                 f"media = {canal.mean():.1f}", fontsize=11)'),
          (81, '        axes[0, i + 1].axis("off")'),
          (84, '        axes[1, i + 1].imshow(canal_coloreado(canal, i))'),
          (85, '        axes[1, i + 1].set_title(f"Canal {nombre} – teñido", fontsize=11)'),
          (86, '        axes[1, i + 1].axis("off")'),
          (88, '    plt.tight_layout(rect=[0, 0, 1, 0.95])'),
          (89, '    if ruta_salida:'),
          (90, '        fig.savefig(ruta_salida, dpi=150, bbox_inches="tight")'),
          (91, '        print(f"  Figura de canales guardada como: {os.path.basename(ruta_salida)}")'),
          (92, '    return fig')],
         [("76", "Recorre los tres canales con su índice (0, 1, 2) para ubicarlos en las columnas 1 a 3."),
          ("78-81", "Fila superior: cada canal como imagen en escala de grises. Se fija <code>vmin=0, vmax=255</code> para que el brillo sea absoluto y comparable entre canales (sin autoescalado). El título incluye la intensidad media."),
          ("84-86", "Fila inferior: cada canal 'teñido' con su color puro mediante <code>canal_coloreado</code>."),
          ("88-92", "Ajusta el diseño, guarda la figura a 150 DPI y la devuelve.")]),

        (6, "Figura Comparativa de la Conversión a Gris",
         [(95, 'def graficar_gris(img_rgb, gris_opencv, gris_manual, ruta_salida=None):'),
          (96, '    diferencia = cv2.absdiff(gris_opencv, gris_manual)'),
          (98, '    fig, axes = plt.subplots(1, 4, figsize=(20, 5))'),
          (99, '    fig.suptitle("Ejercicio 3: Conversión a escala de grises", fontsize=16, fontweight="bold")'),
          (101, '    axes[0].imshow(img_rgb)'),
          (104, '    axes[1].imshow(gris_opencv, cmap="gray", vmin=0, vmax=255)'),
          (107, '    axes[2].imshow(gris_manual, cmap="gray", vmin=0, vmax=255)'),
          (110, '    im = axes[3].imshow(diferencia, cmap="magma", vmin=0, vmax=max(1, int(diferencia.max())))'),
          (111, '    axes[3].set_title(f"|OpenCV − Manual|  (máx = {diferencia.max()})", fontsize=12)'),
          (112, '    fig.colorbar(im, ax=axes[3], fraction=0.035, pad=0.02)'),
          (114, '    for ax in axes:'),
          (115, '        ax.axis("off")'),
          (117, '    plt.tight_layout(rect=[0, 0, 1, 0.92])'),
          (118, '    if ruta_salida:'),
          (119, '        fig.savefig(ruta_salida, dpi=150, bbox_inches="tight")'),
          (121, '    return fig')],
         [("95-96", "Calcula la diferencia absoluta píxel a píxel entre ambos métodos con <code>cv2.absdiff</code> (evita valores negativos en <code>uint8</code>)."),
          ("98-99", "Crea una figura de 1 fila x 4 paneles."),
          ("101-108", "Muestra la imagen original, el gris de OpenCV y el gris manual, ambos con la escala fija 0-255."),
          ("110-112", "Muestra el mapa de diferencias con el colormap 'magma' y una barra de color. El <code>max(1, ...)</code> evita un rango nulo si ambas imágenes son idénticas. Las diferencias esperadas son de 0 o 1 nivel, debidas solo al redondeo interno de OpenCV."),
          ("114-115", "Oculta los ejes de todos los paneles."),
          ("117-121", "Ajusta el diseño, guarda la figura y la devuelve.")]),

        (7, "Función Integradora y Programa Principal",
         [(124, 'def procesar_imagen_b(ruta, mostrar=True):'),
          (125, '    img_rgb = cargar_imagen_rgb(ruta)'),
          (126, '    alto, ancho, _ = img_rgb.shape'),
          (132, '    canales = separar_canales(img_rgb)'),
          (133, '    for canal, nombre in zip(canales, NOMBRES_CANALES):'),
          (134, '        print(f"  {nombre:<10} forma={canal.shape}  media={canal.mean():7.2f}  "'),
          (135, '              f"mín={canal.min():3d}  máx={canal.max():3d}")'),
          (136, '    graficar_canales(img_rgb, canales, RUTA_SALIDA_CANALES)'),
          (140, '    gris_opencv, gris_manual = convertir_a_gris(img_rgb)'),
          (143, '    print(f"  Diferencia máxima entre métodos: {cv2.absdiff(gris_opencv, gris_manual).max()}")'),
          (144, '    cv2.imwrite(RUTA_IMAGEN_GRIS, gris_opencv)'),
          (146, '    graficar_gris(img_rgb, gris_opencv, gris_manual, RUTA_SALIDA_GRIS)'),
          (148, '    if mostrar:'),
          (149, '        plt.show()'),
          (151, '    return {"canales": canales, "gris_opencv": gris_opencv, "gris_manual": gris_manual}'),
          (154, 'if __name__ == "__main__":'),
          (159, '    procesar_imagen_b(RUTA_IMAGEN_B)')],
         [("124-128", "Carga la imagen \"b\", obtiene sus dimensiones desde <code>shape</code> (alto, ancho, canales) y las imprime."),
          ("131-135", "Separa los canales e imprime, para cada uno, su forma, intensidad media, mínimo y máximo."),
          ("136", "Genera y guarda la figura de separación de canales."),
          ("139-143", "Convierte la imagen a gris por ambos métodos e imprime la media de cada resultado y la diferencia máxima entre ellos."),
          ("144-145", "Guarda la imagen en escala de grises como <i>flores_gris.png</i>; <code>imwrite</code> acepta directamente una matriz de un solo canal."),
          ("146", "Genera la figura comparativa de la conversión."),
          ("148-151", "Muestra las ventanas de Matplotlib y devuelve los resultados."),
          ("154-163", "Punto de entrada: imprime el encabezado, procesa <i>flores.png</i> y muestra el mensaje final.")])
    ]
    render_section(3, "Separación de Planos R, G, B y Conversión a Gris", "ejercicio_3.py", ej3_blocks)
    render_resultados([
        ("ejercicio_3_canales.png", "Figura 3. Separación de los planos de color R, G, B e histogramas por canal"),
        ("ejercicio_3_gris.png", "Figura 4. Conversión a escala de grises: OpenCV vs. fórmula manual y mapa de diferencias"),
    ])

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {ruta_pdf}")
    print(f"Tamaño del archivo: {os.path.getsize(ruta_pdf):,} bytes")


if __name__ == "__main__":
    build_pdf()
