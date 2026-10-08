# ==============================================================================
# Ejercicio 7: Colorización de Imagen en Escala de Grises
# ==============================================================================
# Este script toma la imagen de olas del mar en escala de grises (sea.jpg)
# y le aplica color para convertirla en una imagen coloreada.
#
# Técnica: Se utiliza un mapeo de colores basado en la intensidad de los
# píxeles en la imagen gris. Se asignan colores realistas del mar:
#   - Tonos oscuros → Azul profundo/oscuro (agua profunda)
#   - Tonos medios → Azul-verde/turquesa (agua media)
#   - Tonos claros → Blanco/celeste (espuma de las olas)
#
# Se utilizan múltiples métodos para demostrar diferentes técnicas de
# colorización.
# ==============================================================================

from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configuración de rutas ---
directorio = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(directorio, "sea.jpg")  # Imagen de olas en gris

# --- Carga de la imagen ---
print("=" * 60)
print("  EJERCICIO 7: Colorización de Imagen en Escala de Grises")
print("=" * 60)

img_gris = Image.open(ruta_imagen).convert("L")
print(f"\nImagen original: sea.jpg (olas en escala de grises)")
print(f"  Tamaño: {img_gris.size[0]} x {img_gris.size[1]} píxeles")
print(f"  Modo: {img_gris.mode}")

# Convertir a array NumPy
arr_gris = np.array(img_gris, dtype=np.float64)

# =====================================================================
# MÉTODO 1: Colorización con Mapa de Colores Personalizado (Oceánico)
# =====================================================================
print(f"\n--- Método 1: Mapa de Colores Personalizado (Oceánico) ---")

# Normalizar la imagen gris al rango [0, 1]
arr_normalizado = arr_gris / 255.0

# Crear canales R, G, B basados en la intensidad
# Esquema de color oceánico realista:
#   - Tonos oscuros: Azul oscuro profundo (agua profunda)
#   - Tonos medios: Azul-verdoso (agua media)
#   - Tonos claros: Blanco azulado (espuma)

# Canal Rojo: bajo en agua profunda, aumenta en la espuma
canal_R = np.clip(arr_normalizado * 0.3 + np.power(arr_normalizado, 3) * 0.7, 0, 1)

# Canal Verde: moderado en tonos medios (efecto verdoso del agua), alto en espuma
canal_G = np.clip(arr_normalizado * 0.5 + np.power(arr_normalizado, 2) * 0.5, 0, 1)

# Canal Azul: alto en todo el rango (dominancia azul), más intenso en tonos medios
canal_B = np.clip(0.15 + arr_normalizado * 0.85, 0, 1)

# Combinar canales en una imagen RGB
arr_color_oceano = np.stack([
    (canal_R * 255).astype(np.uint8),
    (canal_G * 255).astype(np.uint8),
    (canal_B * 255).astype(np.uint8)
], axis=-1)

img_oceano = Image.fromarray(arr_color_oceano, mode="RGB")
img_oceano.save(os.path.join(directorio, "sea_color_oceano.jpg"), quality=95)
print("  Guardado como: sea_color_oceano.jpg")

# =====================================================================
# MÉTODO 2: Colorización con LUT (Look-Up Table) - Atardecer
# =====================================================================
print(f"\n--- Método 2: LUT de Atardecer ---")

# Crear tablas de mapeo para cada canal (256 valores)
lut_R = []
lut_G = []
lut_B = []

for i in range(256):
    t = i / 255.0  # Normalizado [0, 1]

    # Tonos de atardecer sobre el mar:
    # Oscuros: morado oscuro → Medios: naranja cálido → Claros: amarillo dorado
    r = int(min(255, 30 + t * 200 + (t ** 2) * 25))
    g = int(min(255, 10 + t * 100 + (t ** 3) * 145))
    b = int(min(255, 60 + t * 80 - (t ** 2) * 40 + (t ** 4) * 155))

    lut_R.append(r)
    lut_G.append(g)
    lut_B.append(b)

# Aplicar las LUTs a la imagen gris
img_R_atardecer = img_gris.point(lut_R)
img_G_atardecer = img_gris.point(lut_G)
img_B_atardecer = img_gris.point(lut_B)

# Combinar los canales
img_atardecer = Image.merge("RGB", (img_R_atardecer, img_G_atardecer, img_B_atardecer))
img_atardecer.save(os.path.join(directorio, "sea_color_atardecer.jpg"), quality=95)
print("  Guardado como: sea_color_atardecer.jpg")

# =====================================================================
# MÉTODO 3: Colorización con Matplotlib Colormap (Turquesa Tropical)
# =====================================================================
print(f"\n--- Método 3: Colormap de Matplotlib (Turquesa Tropical) ---")

# Usar un colormap de matplotlib para mapear los valores de gris a colores
# 'ocean' colormap simula colores del océano
cmap = plt.colormaps.get_cmap('ocean')
arr_mapeado = cmap(arr_normalizado)  # Retorna array RGBA

# Convertir de RGBA a RGB (uint8)
arr_color_cmap = (arr_mapeado[:, :, :3] * 255).astype(np.uint8)
img_cmap = Image.fromarray(arr_color_cmap, mode="RGB")
img_cmap.save(os.path.join(directorio, "sea_color_tropical.jpg"), quality=95)
print("  Guardado como: sea_color_tropical.jpg")

# =====================================================================
# MÉTODO 4: Colorización con ImageOps.colorize (Azul Realista)
# =====================================================================
print(f"\n--- Método 4: ImageOps.colorize (Azul Realista) ---")

# ImageOps.colorize mapea los tonos oscuros a un color y los claros a otro
# con un color intermedio opcional
img_colorize = ImageOps.colorize(
    img_gris,
    black=(5, 15, 45),        # Azul muy oscuro para las partes oscuras (profundidad)
    white=(220, 240, 255),    # Blanco azulado para las partes claras (espuma)
    mid=(20, 90, 160),        # Azul medio para los tonos intermedios (agua)
    blackpoint=0,
    whitepoint=255,
    midpoint=120
)

# Aplicar un leve suavizado para naturalidad
img_colorize = img_colorize.filter(ImageFilter.SMOOTH)

# Aumentar saturación ligeramente
enhancer_sat = ImageEnhance.Color(img_colorize)
img_colorize = enhancer_sat.enhance(1.3)

img_colorize.save(os.path.join(directorio, "sea_color_realista.jpg"), quality=95)
print("  Guardado como: sea_color_realista.jpg")

# --- Información de resultados ---
print(f"\n{'-' * 55}")
print(f"  Resumen de Colorizaciones Aplicadas")
print(f"{'-' * 55}")
print(f"  Método 1 - Oceánico:   Mapa personalizado con NumPy")
print(f"  Método 2 - Atardecer:  LUT (Look-Up Table) con Image.point()")
print(f"  Método 3 - Tropical:   Colormap 'ocean' de Matplotlib")
print(f"  Método 4 - Realista:   ImageOps.colorize() de Pillow")
print(f"{'-' * 55}")

# --- Visualización ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle("Ejercicio 7: Colorización de Imagen de Olas en Escala de Grises",
             fontsize=16, fontweight='bold', y=0.99)

# Imagen original en grises
axes[0, 0].imshow(arr_gris, cmap='gray')
axes[0, 0].set_title("Original (Escala de Grises)", fontsize=12, fontweight='bold')
axes[0, 0].axis('off')

# Método 1: Oceánico
axes[0, 1].imshow(img_oceano)
axes[0, 1].set_title("Método 1: Oceánico\n(Mapa personalizado con NumPy)", fontsize=11)
axes[0, 1].axis('off')

# Método 2: Atardecer
axes[0, 2].imshow(img_atardecer)
axes[0, 2].set_title("Método 2: Atardecer\n(LUT con Image.point())", fontsize=11)
axes[0, 2].axis('off')

# Método 3: Tropical
axes[1, 0].imshow(img_cmap)
axes[1, 0].set_title("Método 3: Tropical\n(Colormap 'ocean' de Matplotlib)", fontsize=11)
axes[1, 0].axis('off')

# Método 4: Realista
axes[1, 1].imshow(img_colorize)
axes[1, 1].set_title("Método 4: Realista\n(ImageOps.colorize de Pillow)", fontsize=11)
axes[1, 1].axis('off')

# Comparación lado a lado (gris vs mejor resultado)
# Crear una imagen dividida: mitad gris, mitad color
ancho, alto = img_gris.size
mitad = ancho // 2
img_gris_rgb = img_gris.convert("RGB")

img_comparacion = Image.new("RGB", (ancho, alto))
img_comparacion.paste(img_gris_rgb.crop((0, 0, mitad, alto)), (0, 0))
img_comparacion.paste(img_colorize.crop((mitad, 0, ancho, alto)), (mitad, 0))

axes[1, 2].imshow(img_comparacion)
axes[1, 2].axvline(x=mitad, color='white', linestyle='-', linewidth=2)
axes[1, 2].text(mitad / 2, alto * 0.05, "Original", ha='center', va='top',
                fontsize=11, color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.5))
axes[1, 2].text(mitad + mitad / 2, alto * 0.05, "Coloreada", ha='center', va='top',
                fontsize=11, color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.5))
axes[1, 2].set_title("Comparación: Original vs Coloreada", fontsize=12, fontweight='bold')
axes[1, 2].axis('off')

# Ajustar espaciado
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(directorio, "ejercicio_7_resultado.png"), dpi=150, bbox_inches='tight')
print(f"\nFigura completa guardada como: ejercicio_7_resultado.png")
plt.show()

print("\n" + "=" * 60)
print("  Ejercicio 7 completado exitosamente.")
print("=" * 60)
