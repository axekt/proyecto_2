from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import os

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(directorio, "sea.jpg") 

print("=" * 60)
print("  EJERCICIO 7: Colorización de Imagen en Escala de Grises")
print("=" * 60)

img_gris = Image.open(ruta_imagen).convert("L")
print(f"\nImagen original: sea.jpg (olas en escala de grises)")
print(f"  Tamaño: {img_gris.size[0]} x {img_gris.size[1]} píxeles")
print(f"  Modo: {img_gris.mode}")

arr_gris = np.array(img_gris, dtype=np.float64)

print(f"\n--- Método 1: Mapa de Colores Personalizado (Oceánico) ---")

arr_normalizado = arr_gris / 255.0

canal_R = np.clip(arr_normalizado * 0.3 + np.power(arr_normalizado, 3) * 0.7, 0, 1)

canal_G = np.clip(arr_normalizado * 0.5 + np.power(arr_normalizado, 2) * 0.5, 0, 1)

canal_B = np.clip(0.15 + arr_normalizado * 0.85, 0, 1)

arr_color_oceano = np.stack([
    (canal_R * 255).astype(np.uint8),
    (canal_G * 255).astype(np.uint8),
    (canal_B * 255).astype(np.uint8)
], axis=-1)

img_oceano = Image.fromarray(arr_color_oceano, mode="RGB")
img_oceano.save(os.path.join(directorio, "sea_color_oceano.jpg"), quality=95)
print("  Guardado como: sea_color_oceano.jpg")

print(f"\n--- Método 2: LUT de Atardecer ---")

lut_R = []
lut_G = []
lut_B = []

for i in range(256):
    t = i / 255.0  
    r = int(min(255, 30 + t * 200 + (t ** 2) * 25))
    g = int(min(255, 10 + t * 100 + (t ** 3) * 145))
    b = int(min(255, 60 + t * 80 - (t ** 2) * 40 + (t ** 4) * 155))

    lut_R.append(r)
    lut_G.append(g)
    lut_B.append(b)

img_R_atardecer = img_gris.point(lut_R)
img_G_atardecer = img_gris.point(lut_G)
img_B_atardecer = img_gris.point(lut_B)

img_atardecer = Image.merge("RGB", (img_R_atardecer, img_G_atardecer, img_B_atardecer))
img_atardecer.save(os.path.join(directorio, "sea_color_atardecer.jpg"), quality=95)
print("  Guardado como: sea_color_atardecer.jpg")

print(f"\n--- Método 3: Colormap de Matplotlib (Turquesa Tropical) ---")

cmap = plt.colormaps.get_cmap('ocean')
arr_mapeado = cmap(arr_normalizado)

arr_color_cmap = (arr_mapeado[:, :, :3] * 255).astype(np.uint8)
img_cmap = Image.fromarray(arr_color_cmap, mode="RGB")
img_cmap.save(os.path.join(directorio, "sea_color_tropical.jpg"), quality=95)
print("  Guardado como: sea_color_tropical.jpg")

print(f"\n--- Método 4: ImageOps.colorize (Azul Realista) ---")

img_colorize = ImageOps.colorize(
    img_gris,
    black=(5, 15, 45),        
    white=(220, 240, 255),    
    mid=(20, 90, 160),       
    blackpoint=0,
    whitepoint=255,
    midpoint=120
)

img_colorize = img_colorize.filter(ImageFilter.SMOOTH)

enhancer_sat = ImageEnhance.Color(img_colorize)
img_colorize = enhancer_sat.enhance(1.3)

img_colorize.save(os.path.join(directorio, "sea_color_realista.jpg"), quality=95)
print("  Guardado como: sea_color_realista.jpg")

print(f"\n{'-' * 55}")
print(f"  Resumen de Colorizaciones Aplicadas")
print(f"{'-' * 55}")
print(f"  Método 1 - Oceánico:   Mapa personalizado con NumPy")
print(f"  Método 2 - Atardecer:  LUT (Look-Up Table) con Image.point()")
print(f"  Método 3 - Tropical:   Colormap 'ocean' de Matplotlib")
print(f"  Método 4 - Realista:   ImageOps.colorize() de Pillow")
print(f"{'-' * 55}")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle("Ejercicio 7: Colorización de Imagen de Olas en Escala de Grises",
             fontsize=16, fontweight='bold', y=0.99)

axes[0, 0].imshow(arr_gris, cmap='gray')
axes[0, 0].set_title("Original (Escala de Grises)", fontsize=12, fontweight='bold')
axes[0, 0].axis('off')

axes[0, 1].imshow(img_oceano)
axes[0, 1].set_title("Método 1: Oceánico\n(Mapa personalizado con NumPy)", fontsize=11)
axes[0, 1].axis('off')

axes[0, 2].imshow(img_atardecer)
axes[0, 2].set_title("Método 2: Atardecer\n(LUT con Image.point())", fontsize=11)
axes[0, 2].axis('off')

axes[1, 0].imshow(img_cmap)
axes[1, 0].set_title("Método 3: Tropical\n(Colormap 'ocean' de Matplotlib)", fontsize=11)
axes[1, 0].axis('off')

axes[1, 1].imshow(img_colorize)
axes[1, 1].set_title("Método 4: Realista\n(ImageOps.colorize de Pillow)", fontsize=11)
axes[1, 1].axis('off')

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

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(directorio, "ejercicio_7_resultado.png"), dpi=150, bbox_inches='tight')
print(f"\nFigura completa guardada como: ejercicio_7_resultado.png")
plt.show()

print("\n" + "=" * 60)
print("  Ejercicio 7 completado exitosamente.")
print("=" * 60)
