import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

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
            self.drawString(54, 755, "Proyecto #2 — Procesamiento de Imágenes (Ejercicios 4 al 7)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 750, 612 - 54, 750)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Documento Técnico Explicativo — Python, PIL, NumPy, Matplotlib")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()

def build_pdf():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_pdf = os.path.join(directorio_actual, "Resumen_Ejercicios_4_al_7.pdf")
    
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
        alignment=1, # Center
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=muted_text,
        alignment=1,
        spaceAfter=20
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
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
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
        [[Paragraph("<b>PROYECTO ACADÉMICO — PROCESAMIENTO DE IMÁGENES</b><br/><font size=11 color='#4A5568'>Resumen General, Justificación de Librerías y Análisis Línea por Línea (Ejercicios 4 al 7)</font>", title_style)]],
        colWidths=[504]
    )
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 14))

    # SECTION 1: Resumen General
    story.append(Paragraph("1. Resumen General de Cada Ejercicio", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
    
    resumenes = [
        ("Ejercicio 4: Composición con Plantillas Geométricas",
         "<b>Objetivo:</b> Superponer la imagen de Lena (<i>fig_00.jpg</i>) sobre 4 imágenes de fondo distintas (<i>fig_01.jpg</i> a <i>fig_04.jpg</i>) utilizando plantillas geométricas (círculo, rectángulo, pentágono y corazón; <i>pla_01.jpg</i> a <i>pla_04.jpg</i>) como máscaras de composición.<br/>"
         "<b>Mecanismo:</b> Se redimensiona la imagen a superponer y la máscara al tamaño exacto de cada fondo. Mediante <code>Image.composite(sup, fondo, mascara)</code>, los píxeles blancos (255) de la plantilla dejan ver a Lena, los negros (0) dejan ver el fondo, y los bordes grises se difuminan suavemente sin distorsión."),
        
        ("Ejercicio 5: Separación de Planos R, G, B y Cálculo de Área",
         "<b>Objetivo:</b> Descomponer la imagen de fluorescencia de neuronas (<i>fig_05.jpg</i>) en sus tres canales fundamentales Rojo, Verde y Azul, calculando el área física ocupada por cada componente de color.<br/>"
         "<b>Mecanismo:</b> Con <code>img.split()</code> se extraen las bandas individuales. Se transforman en matrices NumPy y se aplica un umbral de corte (intensidad > 30) para aislar la emisión biológica del ruido de fondo. Se cuantifican los píxeles activos y su porcentaje respecto al área total, identificando el canal cromático predominante."),
        
        ("Ejercicio 6: Histograma RGB y Escala de Grises",
         "<b>Objetivo:</b> Analizar la distribución estadística de intensidades lumínicas y cromáticas en la imagen de Lena (<i>fig_00.jpg</i>), extrayendo la tonalidad modal (más repetida) en cada canal y comparando el histograma en escala de grises.<br/>"
         "<b>Mecanismo:</b> Se extrae el histograma de 768 posiciones con <code>img.histogram()</code>, dividiéndolo en tramos de 256 niveles para R, G y B. Con <code>np.argmax()</code> se localiza la moda exacta de cada canal. La imagen se convierte a escala de grises ('L') mediante la fórmula estándar de luminancia ITU-R 601-2, visualizando subplots con curvas individuales y acumulativas."),
        
        ("Ejercicio 7: Colorización de Imagen en Escala de Grises",
         "<b>Objetivo:</b> Transformar una imagen monocromática de olas del mar (<i>sea.jpg</i>) en una imagen cromática vívida utilizando cuatro técnicas de colorización avanzadas.<br/>"
         "<b>Mecanismo:</b> Se implementan cuatro algoritmos: 1) <i>Mapeo oceánico no lineal</i> en NumPy combinando funciones polinómicas y cúbicas; 2) <i>Tabla de búsqueda (LUT)</i> para efecto atardecer cálido con <code>Image.point()</code>; 3) <i>Paleta predefinida</i> mediante mapas de color colormap de Matplotlib (<code>'ocean'</code>); y 4) <i>Colorización tricromática</i> con <code>ImageOps.colorize()</code> complementada con realce de saturación y filtro de suavizado.")
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
        
        [Paragraph("<b>PIL / Pillow</b><br/>(<code>Image</code>)", table_cell_style),
         Paragraph("<code>open()</code>, <code>resize()</code>, <code>convert()</code>, <code>split()</code>, <code>merge()</code>, <code>composite()</code>, <code>point()</code>, <code>save()</code>", table_cell_style),
         Paragraph("Librería estándar para I/O y procesamiento de imágenes en Python. Permite manipular formatos JPG/PNG, transformar espacios de color (RGB, L), recomponer imágenes con máscaras alfa y redimensionar con filtros de alta calidad como LANCZOS.", table_cell_style)],
        
        [Paragraph("<b>PIL / Pillow</b><br/>(<code>ImageOps, ImageFilter, ImageEnhance</code>)", table_cell_style),
         Paragraph("<code>ImageOps.colorize()</code>,<br/><code>ImageFilter.SMOOTH</code>,<br/><code>ImageEnhance.Color()</code>", table_cell_style),
         Paragraph("Módulos avanzados de postprocesamiento en el Ejercicio 7. <code>colorize</code> asigna gradientes tricromáticos (sombras/medios tonos/luces), <code>SMOOTH</code> elimina el banding/ruido del mar y <code>Color</code> amplifica la saturación un 30%.", table_cell_style)],
         
        [Paragraph("<b>NumPy</b><br/>(<code>numpy</code>)", table_cell_style),
         Paragraph("<code>array()</code>, <code>sum()</code>, <code>mean()</code>, <code>std()</code>, <code>argmax()</code>, <code>clip()</code>, <code>power()</code>, <code>stack()</code>", table_cell_style),
         Paragraph("Motor de cálculo matricial ultrarrápido en C. Permite tratar imágenes como tensores numéricos, vectorizar cálculos sobre millones de píxeles, segmentar áreas por umbralización booleana y diseñar curvas de transferencia de color matemáticas.", table_cell_style)],
        
        [Paragraph("<b>Matplotlib</b><br/>(<code>pyplot</code>)", table_cell_style),
         Paragraph("<code>subplots()</code>, <code>imshow()</code>, <code>bar()</code>, <code>plot()</code>, <code>axvline()</code>, <code>savefig()</code>", table_cell_style),
         Paragraph("Generación de visualizaciones comparativas, subplots estructurados, histogramas de frecuencia, gráficos de barras de áreas y mapas de falso color (colormaps científicos). Permite exportar resultados en alta resolución (DPI=150).", table_cell_style)],
        
        [Paragraph("<b>os</b>", table_cell_style),
         Paragraph("<code>path.dirname()</code>, <code>path.abspath()</code>, <code>path.join()</code>", table_cell_style),
         Paragraph("Garantiza portabilidad multiplataforma (Windows/Linux/macOS) resolviendo rutas relativas al script en ejecución sin depender del directorio de trabajo actual.", table_cell_style)]
    ]
    
    lib_table = Table(lib_data, colWidths=[100, 160, 244])
    lib_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(lib_table)
    story.append(Spacer(1, 14))

    # Helper function to render Code Blocks & Line explanations
    def render_section(exercise_num, exercise_title, script_name, blocks_data):
        story.append(PageBreak())
        story.append(Paragraph(f"3.{exercise_num - 3} Ejercicio {exercise_num} — {exercise_title}", h1_style))
        story.append(Paragraph(f"<b>Archivo fuente:</b> <code>{script_name}</code> (Código limpio sin comentarios)", h3_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))
        
        for block_num, b_title, b_code, b_lines in blocks_data:
            block_flowables = []
            block_flowables.append(Paragraph(f"Bloque {block_num}: {b_title}", h2_style))
            
            # Code box
            code_paragraphs = [Paragraph(f"<font color='#718096'>{ln:2d} | </font>{code_line.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')}", code_style) for ln, code_line in b_code]
            code_table = Table([[code_paragraphs]], colWidths=[504])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), code_bg),
                ('BOX', (0,0), (-1,-1), 0.8, code_border),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
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

    # ==================== EJERCICIO 4 DATA ====================
    ej4_blocks = [
        (1, "Importación de Librerías", 
         [(1, "from PIL import Image"),
          (2, "import matplotlib.pyplot as plt"),
          (3, "import os")],
         [("1", "Importa el módulo central <code>Image</code> de Pillow para manipular, convertir y componer imágenes."),
          ("2", "Importa la interfaz <code>pyplot</code> de Matplotlib para la visualización tabular de resultados."),
          ("3", "Importa el módulo <code>os</code> para la gestión dinámica y segura de rutas de archivos en el sistema operativo.")]),
         
        (2, "Definición y Configuración de Rutas",
         [(5, "directorio = os.path.dirname(os.path.abspath(__file__))"),
          (7, "ruta_superponer = os.path.join(directorio, \"fig_00.jpg\")"),
          (9, "rutas_fondo = ["),
          (10, "    os.path.join(directorio, \"fig_01.jpg\"),"),
          (11, "    os.path.join(directorio, \"fig_02.jpg\"),"),
          (12, "    os.path.join(directorio, \"fig_03.jpg\"),"),
          (13, "    os.path.join(directorio, \"fig_04.jpg\"),"),
          (14, "]"),
          (16, "rutas_plantillas = ["),
          (17, "    os.path.join(directorio, \"pla_01.jpg\"),"),
          (18, "    os.path.join(directorio, \"pla_02.jpg\"),"),
          (19, "    os.path.join(directorio, \"pla_03.jpg\"),"),
          (20, "    os.path.join(directorio, \"pla_04.jpg\"),"),
          (21, "]"),
          (23, "nombres_plantillas = [\"Círculo\", \"Rectángulo\", \"Pentágono\", \"Corazón\"]"),
          (25, "nombres_fondo = [\"Libros con planta\", \"Universidad\", \"Libro en pasto\", \"Libro fantástico\"]")],
         [("5", "Obtiene la ruta absoluta del directorio que contiene el script para garantizar portabilidad."),
          ("7", "Define la ruta de la imagen que será superpuesta (Lena: <i>fig_00.jpg</i>)."),
          ("9-14", "Lista con las 4 rutas absolutas de los fondos sobre los cuales se proyectará Lena."),
          ("16-21", "Lista con las 4 rutas de las plantillas en blanco y negro (máscaras de recorte)."),
          ("23, 25", "Listas de cadenas de texto descriptivas para las figuras geométricas y fondos, empleadas en títulos y nombres de archivo.")]),
         
        (3, "Carga de Imagen a Superponer y Preparación de la Figura",
         [(27, "print(\"=\" * 60)"),
          (28, "print(\"  EJERCICIO 4: Composición con Plantillas Geométricas\")"),
          (29, "print(\"=\" * 60)"),
          (31, "img_superponer = Image.open(ruta_superponer).convert(\"RGB\")"),
          (32, "print(f\"\\nImagen a superponer: fig_00.jpg\")"),
          (33, "print(f\"  Tamaño: {img_superponer.size}\")"),
          (34, "print(f\"  Modo: {img_superponer.mode}\")"),
          (36, "fig, axes = plt.subplots(4, 4, figsize=(18, 18))"),
          (37, "fig.suptitle(\"Ejercicio 4: Composición de Imágenes con Plantillas Geométricas\","),
          (38, "             fontsize=16, fontweight='bold', y=0.98)")],
         [("27-29", "Imprime en consola un encabezado formateado delimitado por líneas de 60 caracteres."),
          ("31", "Abre la imagen <i>fig_00.jpg</i> y asegura su representación en espacio de color de 3 canales RGB."),
          ("32-34", "Imprime información de control técnico: nombre, dimensiones en píxeles (ancho x alto) y modo de color."),
          ("36-38", "Inicializa una cuadrícula de 4x4 subplots (16 gráficos) en Matplotlib con tamaño 18x18 pulgadas y título principal negrita.")]),
         
        (4, "Bucle Principal de Composición y Redimensionamiento",
         [(40, "for i in range(4):"),
          (41, "    img_fondo = Image.open(rutas_fondo[i]).convert(\"RGB\")"),
          (42, "    img_plantilla = Image.open(rutas_plantillas[i]).convert(\"L\")"),
          (43, "    tamaño = img_fondo.size"),
          (44, "    img_sup_resized = img_superponer.resize(tamaño, Image.LANCZOS)"),
          (45, "    mascara_resized = img_plantilla.resize(tamaño, Image.LANCZOS)"),
          (46, "    resultado = Image.composite(img_sup_resized, img_fondo, mascara_resized)")],
         [("40", "Itera sobre los 4 casos de composición (índices 0 a 3)."),
          ("41", "Carga el fondo correspondiente y lo convierte a modo RGB."),
          ("42", "Carga la plantilla geométrica y la convierte a escala de grises ('L'), modo requerido para operar como máscara alfa."),
          ("43", "Extrae la tupla <code>(ancho, alto)</code> del fondo como resolución maestra de destino."),
          ("44-45", "Redimensiona la imagen de Lena y la plantilla geométrica al tamaño exacto del fondo usando el filtro <code>Image.LANCZOS</code> para máxima nitidez sin pixelado."),
          ("46", "Aplica el algoritmo <code>Image.composite</code>: los píxeles donde la máscara es 255 (blanco) provienen de Lena; donde es 0 (negro), provienen del fondo.")]),
         
        (5, "Guardado en Disco y Presentación Gráfica",
         [(48, "    print(f\"\\n--- Composición {i+1}: Plantilla {nombres_plantillas[i]} ---\")"),
          (53, "    nombre_salida = f\"resultado_ej4_{nombres_plantillas[i].lower()}.jpg\""),
          (54, "    ruta_salida = os.path.join(directorio, nombre_salida)"),
          (55, "    resultado.save(ruta_salida, quality=95)"),
          (58, "    axes[i, 0].imshow(img_fondo); axes[i, 0].set_title(f\"Fondo: {nombres_fondo[i]}\"); axes[i, 0].axis('off')"),
          (61, "    axes[i, 1].imshow(img_plantilla, cmap='gray'); axes[i, 1].set_title(f\"Plantilla: {nombres_plantillas[i]}\"); axes[i, 1].axis('off')"),
          (64, "    axes[i, 2].imshow(img_sup_resized); axes[i, 2].set_title(\"Superponer: Lena\"); axes[i, 2].axis('off')"),
          (67, "    axes[i, 3].imshow(resultado); axes[i, 3].set_title(f\"Resultado: {nombres_plantillas[i]}\"); axes[i, 3].axis('off')"),
          (72, "plt.tight_layout(rect=[0, 0.03, 1, 0.95])"),
          (74, "ruta_figura = os.path.join(directorio, \"ejercicio_4_resultado.png\")"),
          (75, "plt.savefig(ruta_figura, dpi=150, bbox_inches='tight')"),
          (77, "plt.show()")],
         [("48-52", "Muestra en consola las dimensiones de cada componente del proceso."),
          ("53-56", "Genera el nombre de archivo de salida (ej. <i>resultado_ej4_círculo.jpg</i>) y guarda la imagen con calidad JPG 95%."),
          ("58-69", "Asigna en la fila <code>i</code> de la matriz de gráficos: Columna 0 (Fondo), Columna 1 (Máscara con mapa gris), Columna 2 (Lena redimensionada) y Columna 3 (Composición final). Oculta ejes con <code>axis('off')</code>."),
          ("72-77", "Ajusta márgenes evitando superposiciones, guarda la figura completa de 16 paneles a 150 DPI y despliega la ventana interactiva.")])
    ]
    render_section(4, "Composición con Plantillas Geométricas", "ejercicio_4.py", ej4_blocks)

    # ==================== EJERCICIO 5 DATA ====================
    ej5_blocks = [
        (1, "Importaciones y Carga de la Imagen de Neuronas",
         [(1, "from PIL import Image"),
          (2, "import numpy as np"),
          (3, "import matplotlib.pyplot as plt"),
          (4, "import os"),
          (6, "directorio = os.path.dirname(os.path.abspath(__file__))"),
          (7, "ruta_imagen = os.path.join(directorio, \"fig_05.jpg\")"),
          (13, "img = Image.open(ruta_imagen).convert(\"RGB\")")],
         [("1-4", "Importa Pillow, NumPy (cálculo matricial), Matplotlib y os."),
          ("6-7", "Construye la ruta a la imagen de fluorescencia confocal <i>fig_05.jpg</i>."),
          ("13-17", "Abre la imagen, fuerza formato RGB y reporta en consola resolución y número total de píxeles.")]),
         
        (2, "Separación de Planos Cromáticos R, G, B",
         [(19, "plano_R, plano_G, plano_B = img.split()"),
          (21, "arr_R = np.array(plano_R)"),
          (22, "arr_G = np.array(plano_G)"),
          (23, "arr_B = np.array(plano_B)"),
          (25, "total_pixeles = arr_R.size")],
         [("19", "Utiliza el método nativo <code>img.split()</code> para descomponer la imagen en tres objetos Image monocromáticos."),
          ("21-23", "Convierte cada plano de Pillow en matrices NumPy 2D de enteros no signados de 8 bits (uint8) con valores entre 0 y 255."),
          ("25", "Almacena el total de píxeles de la imagen (ancho x alto) mediante el atributo <code>.size</code> del array.")]),
         
        (3, "Segmentación por Umbralización y Cálculo de Área",
         [(27, "umbral = 30"),
          (29, "pixeles_R = np.sum(arr_R > umbral)"),
          (30, "pixeles_G = np.sum(arr_G > umbral)"),
          (31, "pixeles_B = np.sum(arr_B > umbral)"),
          (33, "porcentaje_R = (pixeles_R / total_pixeles) * 100"),
          (34, "porcentaje_G = (pixeles_G / total_pixeles) * 100"),
          (35, "porcentaje_B = (pixeles_B / total_pixeles) * 100")],
         [("27", "Establece un umbral de corte de 30 para discriminar la fluorescencia biológica del ruido térmico y fondo oscuro."),
          ("29-31", "Crea una máscara booleana por canal (<code>arr > umbral</code>) y suma los valores verdaderos (True=1), contando píxeles biológicamente activos."),
          ("33-35", "Calcula la proporción porcentual del área cubierta por cada fluoróforo respecto a la superficie completa del sensor.")]),
         
        (4, "Reporte Tabular de Estadísticas de Intensidad",
         [(37, "print(f\"\\n{'=' * 55}\\n  Análisis de Área por Plano (umbral = {umbral})\\n{'=' * 55}\")"),
          (42, "print(f\"  {'Rojo (R)':<12} {pixeles_R:>18,} {porcentaje_R:>11.2f}%\")"),
          (52, "for nombre, arr, color in [(\"Rojo (R)\", arr_R, \"R\"), (\"Verde (G)\", arr_G, \"G\"), (\"Azul (B)\", arr_B, \"B\")]:"),
          (56, "    print(f\"    Mínimo:    {arr.min()}\")"),
          (57, "    print(f\"    Máximo:    {arr.max()}\")"),
          (58, "    print(f\"    Media:     {arr.mean():.2f}\")"),
          (59, "    print(f\"    Desv.Std:  {arr.std():.2f}\")")],
         [("37-47", "Imprime en consola una tabla formateada con alineación de columnas que detalla conteo de píxeles y porcentajes por color."),
          ("52-60", "Itera sobre los arrays de cada canal calculando mínimo, máximo, media aritmética (brillo global) y desviación estándar (dispersión de contraste).")]),
         
        (5, "Reconstrucción Tricromática y Visualización Multicanal",
         [(62, "canal_cero = Image.new(\"L\", img.size, 0)"),
          (63, "img_solo_R = Image.merge(\"RGB\", (plano_R, canal_cero, canal_cero))"),
          (64, "img_solo_G = Image.merge(\"RGB\", (canal_cero, plano_G, canal_cero))"),
          (65, "img_solo_B = Image.merge(\"RGB\", (canal_cero, canal_cero, plano_B))"),
          (67, "fig, axes = plt.subplots(2, 4, figsize=(20, 10))"),
          (73, "axes[0, 1].imshow(arr_R, cmap='gray')"),
          (82, "axes[1, 1].imshow(img_solo_R)"),
          (94, "barras = axes[1, 0].bar(canales_nombres, porcentajes, color=['#FF4444', '#44BB44', '#4444FF'])")],
         [("62", "Crea una imagen auxiliar 'L' de ceros (negro absoluto) con las mismas dimensiones que la imagen original."),
          ("63-65", "Reconstruye imágenes en color puro aislando cada canal mediante <code>Image.merge('RGB', ...)</code> y rellenando los otros dos canales con negro."),
          ("67-71", "Crea una figura de 2 filas x 4 columnas en Matplotlib."),
          ("73-80", "Fila 1: Presenta la imagen original combinada y los tres planos en escala de grises."),
          ("82-90", "Fila 2: Presenta las imágenes en color aislado (rojo puro, verde puro, azul puro)."),
          ("94-110", "Subplot [1, 0]: Genera un gráfico de barras comparativo con el porcentaje de área de cada plano, etiquetando los valores sobre las columnas y guardando la figura.")])
    ]
    render_section(5, "Separación de Planos R, G, B y Cálculo de Área", "ejercicio_5.py", ej5_blocks)

    # ==================== EJERCICIO 6 DATA ====================
    ej6_blocks = [
        (1, "Extracción y Segmentación del Histograma de Color",
         [(1, "from PIL import Image"),
          (2, "import numpy as np"),
          (3, "import matplotlib.pyplot as plt"),
          (4, "import os"),
          (13, "img = Image.open(ruta_imagen).convert(\"RGB\")"),
          (18, "plano_R, plano_G, plano_B = img.split()"),
          (24, "histograma_pil = img.histogram()"),
          (26, "hist_R_pil = histograma_pil[0:256]"),
          (27, "hist_G_pil = histograma_pil[256:512]"),
          (28, "hist_B_pil = histograma_pil[512:768]")],
         [("1-4", "Importa librerías requeridas."),
          ("13-23", "Carga la imagen de Lena (<i>fig_00.jpg</i>), divide sus bandas cromáticas y extrae los arrays NumPy."),
          ("24", "Invoca <code>img.histogram()</code>: genera una lista contigua de 768 enteros con el conteo de píxeles."),
          ("26-28", "Segmenta la lista en tres sublistas de 256 elementos: [0:256] para R, [256:512] para G y [512:768] para B.")]),
         
        (2, "Cálculo de la Moda (Tonalidad Más Frecuente)",
         [(30, "moda_R = np.argmax(hist_R_pil)"),
          (31, "moda_G = np.argmax(hist_G_pil)"),
          (32, "moda_B = np.argmax(hist_B_pil)"),
          (34, "frecuencia_R = hist_R_pil[moda_R]"),
          (35, "frecuencia_G = hist_G_pil[moda_G]"),
          (36, "frecuencia_B = hist_B_pil[moda_B]")],
         [("30-32", "Aplica <code>np.argmax()</code> sobre cada segmento de 256 posiciones: obtiene el índice exacto (0-255) donde la frecuencia es máxima."),
          ("34-36", "Accede a dicho índice para obtener el conteo absoluto de píxeles que poseen esa intensidad dominante.")]),
         
        (3, "Conversión a Escala de Grises y Análisis Estadístico",
         [(52, "img_gris = img.convert(\"L\")"),
          (54, "arr_gris = np.array(img_gris)"),
          (56, "hist_gris = img_gris.histogram()"),
          (58, "moda_gris = np.argmax(hist_gris)"),
          (59, "frecuencia_gris = hist_gris[moda_gris]"),
          (61, "media_gris = arr_gris.mean()"),
          (62, "std_gris = arr_gris.std()"),
          (63, "mediana_gris = np.median(arr_gris)")],
         [("52", "Convierte la imagen a escala de grises monocromática usando coeficientes de ponderación fisiológica humana (L = 0.299R + 0.587G + 0.114B)."),
          ("54-56", "Convierte a matriz numérica y obtiene su histograma de 256 niveles."),
          ("58-59", "Calcula la moda y el pico de frecuencia del canal de luminancia."),
          ("61-63", "Calcula métricas estadísticas descriptivas: media (brillo global), desviación estándar (contraste dinámico) y mediana.")]),
         
        (4, "Generación Automática de Conclusiones Analíticas",
         [(65, "print(f\"\\n{'=' * 60}\\n  CONCLUSIONES DEL ANÁLISIS DE HISTOGRAMAS\\n{'=' * 60}\")"),
          (71, "if moda_R > moda_B: print(\"  -> La imagen tiene predominancia de tonos CÁLIDOS\")"),
          (76, "brillo_desc = \"brillante\" if media_gris > 140 else \"oscura\" if media_gris < 100 else \"equilibrada\""),
          (81, "contraste_desc = \"alto\" if std_gris > 60 else \"bajo\" if std_gris < 35 else \"medio/bueno\"")],
         [("65-70", "Imprime sección de conclusiones calculadas en tiempo de ejecución."),
          ("71-75", "Evalúa si la moda roja supera a la azul para clasificar la temperatura de color de la escena (cálida vs fría)."),
          ("76-80", "Evalúa la media de luminancia para tipificar la exposición fotográfica (sobreexpuesta/subexpuesta/equilibrada)."),
          ("81-85", "Evalúa la desviación estándar para determinar el aprovechamiento del rango dinámico (contraste alto/medio/bajo).")]),
         
        (5, "Visualización de 9 Paneles y Guardado",
         [(87, "fig, axes = plt.subplots(3, 3, figsize=(18, 16))"),
          (93, "axes[0, 2].barh([\"Rojo\", \"Verde\", \"Azul\", \"Grises\"], [moda_R, moda_G, moda_B, moda_gris])"),
          (102, "axes[1, 0].bar(range(256), hist_R_pil, color='red', alpha=0.7); axes[1, 0].axvline(x=moda_R, color='darkred', linestyle='--')"),
          (129, "axes[2, 0].plot(range(256), hist_R_pil, 'r-', label='R'); axes[2, 0].plot(range(256), hist_G_pil, 'g-', label='G'); axes[2, 0].plot(range(256), hist_B_pil, 'b-', label='B')"),
          (142, "hist_acumulado = np.cumsum(hist_gris) / total_pixeles"),
          (143, "axes[2, 2].plot(range(256), hist_acumulado, 'k-', linewidth=2)"),
          (153, "plt.savefig(os.path.join(directorio, \"ejercicio_6_resultado.png\"), dpi=150, bbox_inches='tight')")],
         [("87-90", "Crea una cuadrícula de 3x3 paneles altamente estructurada."),
          ("93-100", "Panel [0,2]: Gráfico de barras horizontal comparando las modas de los tres canales y de la escala de grises."),
          ("102-126", "Fila 1: Histogramas individuales de R, G y B con barras coloreadas y líneas verticales discontinuas marcando la moda exacta."),
          ("129-140", "Panel [2,0]: Histograma RGB superpuesto mostrando las 3 curvas continuas."),
          ("142-150", "Panel [2,2]: Curva del histograma acumulado normalizado con <code>np.cumsum()</code>, útil para análisis de ecualización."),
          ("153-155", "Exporta la figura completa en alta definición y despliega el renderizador.")])
    ]
    render_section(6, "Histograma RGB y Escala de Grises", "ejercicio_6.py", ej6_blocks)

    # ==================== EJERCICIO 7 DATA ====================
    ej7_blocks = [
        (1, "Configuración y Carga de la Imagen Marina Monocromática",
         [(1, "from PIL import Image, ImageOps, ImageFilter, ImageEnhance"),
          (2, "import numpy as np"),
          (3, "import matplotlib.pyplot as plt"),
          (4, "import os"),
          (6, "directorio = os.path.dirname(os.path.abspath(__file__))"),
          (7, "ruta_imagen = os.path.join(directorio, \"sea.jpg\")"),
          (13, "img_gris = Image.open(ruta_imagen).convert(\"L\")"),
          (18, "arr_gris = np.array(img_gris, dtype=np.float64)")],
         [("1-4", "Importa módulos de Pillow (incluyendo <code>ImageOps, ImageFilter, ImageEnhance</code>), NumPy y Matplotlib."),
          ("6-7", "Localiza la imagen marina en escala de grises <i>sea.jpg</i>."),
          ("13-16", "Carga y asegura conversión a modo 'L' de un solo canal."),
          ("18", "Convierte los píxeles a array NumPy en coma flotante de 64 bits (<code>np.float64</code>) para cálculos de precisión continua sin desbordamiento.")]),
         
        (2, "Método 1: Mapa de Colores Matemático Personalizado (Océano)",
         [(22, "arr_normalizado = arr_gris / 255.0"),
          (24, "canal_R = np.clip(arr_normalizado * 0.3 + np.power(arr_normalizado, 3) * 0.7, 0, 1)"),
          (26, "canal_G = np.clip(arr_normalizado * 0.5 + np.power(arr_normalizado, 2) * 0.5, 0, 1)"),
          (28, "canal_B = np.clip(0.15 + arr_normalizado * 0.85, 0, 1)"),
          (30, "arr_color_oceano = np.stack(["),
          (31, "    (canal_R * 255).astype(np.uint8),"),
          (32, "    (canal_G * 255).astype(np.uint8),"),
          (33, "    (canal_B * 255).astype(np.uint8)"),
          (34, "], axis=-1)"),
          (36, "img_oceano = Image.fromarray(arr_color_oceano, mode=\"RGB\")")],
         [("22", "Normaliza las intensidades al rango unitario [0.0, 1.0]."),
          ("24", "Canal Rojo: Curva fuertemente comprimida mediante potencia cúbica (conserva el rojo solo en la espuma más brillante)."),
          ("26", "Canal Verde: Curva cuadrática intermedia para tonalidades turquesa y esmeralda."),
          ("28", "Canal Azul: Elevación de base (bias = 0.15) asegurando presencia de azul profundo incluso en las sombras más oscuras."),
          ("30-34", "Multiplica por 255, castea a <code>uint8</code> y apila los tres canales a lo largo del último eje (eje z de color)."),
          ("36", "Convierte el tensor NumPy resultante de vuelta a objeto Pillow RGB.")]),
         
        (3, "Método 2: Tabla de Búsqueda LUT (Efecto Atardecer Cálido)",
         [(39, "lut_R = [min(255, int(i * 1.3 + 20)) for i in range(256)]"),
          (40, "lut_G = [min(255, int(i * 0.85)) for i in range(256)]"),
          (41, "lut_B = [min(255, int(i * 0.55)) for i in range(256)]"),
          (43, "lut_total = lut_R + lut_G + lut_B"),
          (45, "img_gris_rgb = img_gris.convert(\"RGB\")"),
          (46, "img_atardecer = img_gris_rgb.point(lut_total)")],
         [("39-41", "Genera tres tablas de búsqueda (LUT) de 256 elementos: Rojo potenciado (+30% más base de 20), Verde atenuado (-15%) y Azul fuertemente filtrado (-45%)."),
          ("43", "Concatena las 3 listas en una única LUT de 768 enteros."),
          ("45", "Replica el canal gris en tres canales idénticos RGB."),
          ("46", "Aplica <code>img.point(lut_total)</code>: transforma cada píxel instantáneamente mediante mapeo directo por tabla en C, logrando un atardecer dorado cálido.")]),
         
        (4, "Método 3: Paleta Científica de Matplotlib ('ocean')",
         [(48, "cmap_ocean = plt.colormaps.get_cmap('ocean')"),
          (50, "arr_normalizado_2 = np.array(img_gris, dtype=np.float64) / 255.0"),
          (52, "arr_rgba = cmap_ocean(arr_normalizado_2)"),
          (54, "arr_rgb = (arr_rgba[:, :, :3] * 255).astype(np.uint8)"),
          (56, "img_tropical = Image.fromarray(arr_rgb, mode=\"RGB\")")],
         [("48", "Obtiene el colormap científico predefinido <code>'ocean'</code> de Matplotlib."),
          ("50", "Normaliza los valores de la imagen en escala de grises a float entre 0.0 y 1.0."),
          ("52", "Aplica el colormap sobre la matriz: devuelve un array RGBA de 4 canales flotantes."),
          ("54-56", "Descarta el canal alfa (<code>[:, :, :3]</code>), escala a 255, convierte a <code>uint8</code> y crea la imagen RGB final.")]),
         
        (5, "Método 4: Mapeo Tricromático con Postprocesamiento (Realista)",
         [(58, "color_sombras = (5, 25, 60)"),
          (59, "color_medios = (20, 120, 160)"),
          (60, "color_luces = (220, 240, 255)"),
          (62, "img_realista = ImageOps.colorize(img_gris, black=color_sombras, white=color_luces, mid=color_medios)"),
          (64, "img_realista = img_realista.filter(ImageFilter.SMOOTH)"),
          (66, "realzador = ImageEnhance.Color(img_realista)"),
          (67, "img_realista = realzador.enhance(1.3)")],
         [("58-60", "Define la triada de color cromática: azul marino profundo en sombras, verde azulado marino en medios tonos y blanco espumoso con tinte celeste en luces."),
          ("62", "Ejecuta <code>ImageOps.colorize</code> para interpolar linealmente los niveles de gris entre las tres tonalidades objetivo."),
          ("64", "Aplica <code>ImageFilter.SMOOTH</code> para homogenizar transiciones tonales en el oleaje."),
          ("66-67", "Aumenta la viveza y saturación cromática en un 30% mediante <code>ImageEnhance.Color.enhance(1.3)</code>.")]),
         
        (6, "Comparación Multipanel y Exportación Final",
         [(70, "fig, axes = plt.subplots(2, 3, figsize=(18, 12))"),
          (76, "axes[0, 0].imshow(img_gris, cmap='gray'); axes[0, 0].set_title(\"Original: sea.jpg (Grises)\")"),
          (80, "axes[0, 1].imshow(img_oceano); axes[0, 1].set_title(\"Método 1: Océano (NumPy)\")"),
          (84, "axes[0, 2].imshow(img_atardecer); axes[0, 2].set_title(\"Método 2: Atardecer (LUT)\")"),
          (88, "axes[1, 0].imshow(img_tropical); axes[1, 0].set_title(\"Método 3: Tropical (Colormap)\")"),
          (92, "axes[1, 1].imshow(img_realista); axes[1, 1].set_title(\"Método 4: Realista (ImageOps)\")"),
          (96, "im_h = img_gris.size[1]; ancho_seccion = img_gris.size[0] // 3"),
          (97, "arr_comp = np.zeros((im_h, ancho_seccion * 3, 3), dtype=np.uint8)"),
          (98, "arr_comp[:, :ancho_seccion] = np.array(img_gris.convert('RGB'))[:, :ancho_seccion]"),
          (99, "arr_comp[:, ancho_seccion:2*ancho_seccion] = np.array(img_oceano)[:, ancho_seccion:2*ancho_seccion]"),
          (100, "arr_comp[:, 2*ancho_seccion:] = np.array(img_realista)[:, 2*ancho_seccion:]"),
          (101, "axes[1, 2].imshow(arr_comp); axes[1, 2].set_title(\"Comparación: Grises | Océano | Realista\")"),
          (111, "plt.savefig(os.path.join(directorio, \"ejercicio_7_resultado.png\"), dpi=150, bbox_inches='tight')")],
         [("70-75", "Configura una cuadrícula de 2 filas x 3 columnas con títulos estilizados."),
          ("76-95", "Representa la imagen original en escala de grises y cada una de las cuatro interpretaciones cromáticas."),
          ("96-105", "Construye una composición trifásica lado a lado (Original en grises, Océano matemático y Realista) en un solo panel para comparación directa de fidelidad."),
          ("111-115", "Exporta la figura final a resolución completa y despliega el visualizador.")])
    ]
    render_section(7, "Colorización de Imagen en Escala de Grises", "ejercicio_7.py", ej7_blocks)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {ruta_pdf}")
    print(f"Tamaño del archivo: {os.path.getsize(ruta_pdf):,} bytes")

if __name__ == "__main__":
    build_pdf()
