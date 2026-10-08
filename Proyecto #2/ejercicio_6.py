# ==============================================================================
# Ejercicio 6: Histograma RGB y Escala de Grises
# ==============================================================================
# Este script obtiene el histograma de la imagen de Lena (fig_00.jpg) para
# cada plano R, G, B. Identifica la tonalidad más repetida en cada canal.
# Además, convierte la imagen a escala de grises, obtiene su histograma
# e imprime conclusiones sobre los resultados.
# ==============================================================================

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configuración de rutas ---
directorio = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(directorio, "fig_00.jpg")  # Imagen de Lena

# --- Carga de la imagen ---
print("=" * 60)
print("  EJERCICIO 6: Histograma RGB y Escala de Grises")
print("=" * 60)

img = Image.open(ruta_imagen).convert("RGB")
print(f"\nImagen original: fig_00.jpg (Lena)")
print(f"  Tamaño: {img.size[0]} x {img.size[1]} píxeles")
print(f"  Modo: {img.mode}")

# --- Separar canales R, G, B ---
plano_R, plano_G, plano_B = img.split()

# Convertir a arrays NumPy
arr_R = np.array(plano_R)
arr_G = np.array(plano_G)
arr_B = np.array(plano_B)

# --- Obtener histogramas usando el método histogram() de PIL ---
# PIL devuelve una lista de 256 valores por canal (768 en total para RGB)
histograma_pil = img.histogram()

# Separar histogramas por canal
hist_R_pil = histograma_pil[0:256]     # Canal Rojo: posiciones 0-255
hist_G_pil = histograma_pil[256:512]   # Canal Verde: posiciones 256-511
hist_B_pil = histograma_pil[512:768]   # Canal Azul: posiciones 512-767

# --- Identificar tonalidad más repetida (moda) de cada canal ---
moda_R = np.argmax(hist_R_pil)
moda_G = np.argmax(hist_G_pil)
moda_B = np.argmax(hist_B_pil)

frecuencia_R = hist_R_pil[moda_R]
frecuencia_G = hist_G_pil[moda_G]
frecuencia_B = hist_B_pil[moda_B]

print(f"\n{'-' * 60}")
print(f"  Tonalidad Más Repetida por Canal (Moda)")
print(f"{'-' * 60}")
print(f"  {'Canal':<15} {'Tonalidad':>12} {'Frecuencia':>15} {'Descripción':<20}")
print(f"{'-' * 60}")
print(f"  {'Rojo (R)':<15} {moda_R:>12} {frecuencia_R:>15,} {'Intensidad ' + str(moda_R)}")
print(f"  {'Verde (G)':<15} {moda_G:>12} {frecuencia_G:>15,} {'Intensidad ' + str(moda_G)}")
print(f"  {'Azul (B)':<15} {moda_B:>12} {frecuencia_B:>15,} {'Intensidad ' + str(moda_B)}")
print(f"{'-' * 60}")

# --- Estadísticas por canal ---
print(f"\n{'-' * 60}")
print(f"  Estadísticas de Intensidad por Canal")
print(f"{'-' * 60}")
for nombre, arr in [("Rojo (R)", arr_R), ("Verde (G)", arr_G), ("Azul (B)", arr_B)]:
    print(f"  {nombre}: Media={arr.mean():.2f}, Mediana={np.median(arr):.2f}, "
          f"Min={arr.min()}, Max={arr.max()}, DesvStd={arr.std():.2f}")

# --- Conversión a Escala de Grises ---
print(f"\n{'-' * 60}")
print(f"  Conversión a Escala de Grises")
print(f"{'-' * 60}")

img_gris = img.convert("L")  # Conversión usando fórmula estándar ITU-R 601-2
arr_gris = np.array(img_gris)

# Histograma en escala de grises
hist_gris = img_gris.histogram()
moda_gris = np.argmax(hist_gris)
frecuencia_gris = hist_gris[moda_gris]

print(f"\n  Imagen en escala de grises:")
print(f"    Tonalidad más repetida: {moda_gris} (frecuencia: {frecuencia_gris:,})")
print(f"    Media de intensidad:    {arr_gris.mean():.2f}")
print(f"    Mediana:                {np.median(arr_gris):.2f}")
print(f"    Desviación estándar:    {arr_gris.std():.2f}")
print(f"    Rango dinámico:         [{arr_gris.min()}, {arr_gris.max()}]")

# --- Conclusiones ---
print(f"\n{'=' * 60}")
print(f"  CONCLUSIONES")
print(f"{'=' * 60}")

# Determinar el canal dominante
canal_dominante = ""
media_canales = {"Rojo": arr_R.mean(), "Verde": arr_G.mean(), "Azul": arr_B.mean()}
canal_max = max(media_canales, key=media_canales.get)
canal_min = min(media_canales, key=media_canales.get)

print(f"""
  1. DISTRIBUCIÓN DE COLOR:
     - El canal con mayor intensidad promedio es el {canal_max}
       (media = {media_canales[canal_max]:.2f}), lo que indica que la imagen
       tiene una dominancia de tonos {canal_max.lower()}s.
     - El canal con menor intensidad es el {canal_min}
       (media = {media_canales[canal_min]:.2f}).

  2. TONALIDADES MÁS FRECUENTES:
     - Rojo: La tonalidad {moda_R} es la más frecuente ({frecuencia_R:,} píxeles).
     - Verde: La tonalidad {moda_G} es la más frecuente ({frecuencia_G:,} píxeles).
     - Azul: La tonalidad {moda_B} es la más frecuente ({frecuencia_B:,} píxeles).

  3. ESCALA DE GRISES:
     - Al convertir a gris, la tonalidad más repetida es {moda_gris}
       (frecuencia: {frecuencia_gris:,}).
     - La media de {arr_gris.mean():.2f} indica que la imagen es
       {'relativamente clara' if arr_gris.mean() > 128 else 'relativamente oscura'}.
     - La desviación estándar de {arr_gris.std():.2f} indica una
       {'alta' if arr_gris.std() > 60 else 'moderada' if arr_gris.std() > 30 else 'baja'}
       variabilidad en las tonalidades, es decir,
       {'buen contraste' if arr_gris.std() > 50 else 'contraste medio' if arr_gris.std() > 30 else 'bajo contraste'}.

  4. COMPARACIÓN RGB vs GRIS:
     - La conversión a gris combina la información de los tres canales,
       produciendo un histograma que refleja la luminosidad general.
     - La imagen de Lena es conocida por tener una distribución equilibrada
       de colores, con predominancia en tonos cálidos (rojos y verdes).
""")

# --- Visualización ---
fig, axes = plt.subplots(3, 3, figsize=(18, 14))
fig.suptitle("Ejercicio 6: Histograma RGB y Escala de Grises - Imagen de Lena",
             fontsize=16, fontweight='bold', y=0.99)

# --- Fila 1: Imagen original y canales separados ---
axes[0, 0].imshow(img)
axes[0, 0].set_title("Imagen Original (RGB)", fontsize=12, fontweight='bold')
axes[0, 0].axis('off')

# Crear imágenes coloreadas de cada plano
img_solo_R = Image.merge("RGB", (plano_R, Image.new("L", img.size, 0), Image.new("L", img.size, 0)))
img_solo_G = Image.merge("RGB", (Image.new("L", img.size, 0), plano_G, Image.new("L", img.size, 0)))
img_solo_B = Image.merge("RGB", (Image.new("L", img.size, 0), Image.new("L", img.size, 0), plano_B))

axes[0, 1].imshow(img_gris, cmap='gray')
axes[0, 1].set_title("Imagen en Escala de Grises", fontsize=12, fontweight='bold')
axes[0, 1].axis('off')

# Imagen compuesta mostrando los tres canales
axes[0, 2].axis('off')
axes[0, 2].text(0.5, 0.7, "Tonalidad más repetida:", ha='center', va='center',
                fontsize=13, fontweight='bold', transform=axes[0, 2].transAxes)
axes[0, 2].text(0.5, 0.55, f"R = {moda_R}  (freq: {frecuencia_R:,})",
                ha='center', va='center', fontsize=12, color='red',
                transform=axes[0, 2].transAxes)
axes[0, 2].text(0.5, 0.40, f"G = {moda_G}  (freq: {frecuencia_G:,})",
                ha='center', va='center', fontsize=12, color='green',
                transform=axes[0, 2].transAxes)
axes[0, 2].text(0.5, 0.25, f"B = {moda_B}  (freq: {frecuencia_B:,})",
                ha='center', va='center', fontsize=12, color='blue',
                transform=axes[0, 2].transAxes)
axes[0, 2].text(0.5, 0.10, f"Gris = {moda_gris}  (freq: {frecuencia_gris:,})",
                ha='center', va='center', fontsize=12, color='gray',
                transform=axes[0, 2].transAxes)
axes[0, 2].set_title("Resumen de Modas", fontsize=12, fontweight='bold')

# --- Fila 2: Histogramas individuales R, G, B ---
rango = range(256)

axes[1, 0].bar(rango, hist_R_pil, color='red', alpha=0.7, width=1.0)
axes[1, 0].axvline(x=moda_R, color='darkred', linestyle='--', linewidth=2,
                   label=f'Moda={moda_R}')
axes[1, 0].set_title(f"Histograma Canal Rojo (R)\nModa: {moda_R}", fontsize=11, color='red')
axes[1, 0].set_xlabel("Intensidad (0-255)")
axes[1, 0].set_ylabel("Frecuencia")
axes[1, 0].legend(fontsize=9)
axes[1, 0].set_xlim([0, 255])

axes[1, 1].bar(rango, hist_G_pil, color='green', alpha=0.7, width=1.0)
axes[1, 1].axvline(x=moda_G, color='darkgreen', linestyle='--', linewidth=2,
                   label=f'Moda={moda_G}')
axes[1, 1].set_title(f"Histograma Canal Verde (G)\nModa: {moda_G}", fontsize=11, color='green')
axes[1, 1].set_xlabel("Intensidad (0-255)")
axes[1, 1].set_ylabel("Frecuencia")
axes[1, 1].legend(fontsize=9)
axes[1, 1].set_xlim([0, 255])

axes[1, 2].bar(rango, hist_B_pil, color='blue', alpha=0.7, width=1.0)
axes[1, 2].axvline(x=moda_B, color='darkblue', linestyle='--', linewidth=2,
                   label=f'Moda={moda_B}')
axes[1, 2].set_title(f"Histograma Canal Azul (B)\nModa: {moda_B}", fontsize=11, color='blue')
axes[1, 2].set_xlabel("Intensidad (0-255)")
axes[1, 2].set_ylabel("Frecuencia")
axes[1, 2].legend(fontsize=9)
axes[1, 2].set_xlim([0, 255])

# --- Fila 3: Histograma combinado RGB y Histograma de Grises ---
# Histograma combinado RGB (superpuesto)
axes[2, 0].bar(rango, hist_R_pil, color='red', alpha=0.4, width=1.0, label='Rojo')
axes[2, 0].bar(rango, hist_G_pil, color='green', alpha=0.4, width=1.0, label='Verde')
axes[2, 0].bar(rango, hist_B_pil, color='blue', alpha=0.4, width=1.0, label='Azul')
axes[2, 0].set_title("Histograma RGB Combinado", fontsize=11, fontweight='bold')
axes[2, 0].set_xlabel("Intensidad (0-255)")
axes[2, 0].set_ylabel("Frecuencia")
axes[2, 0].legend(fontsize=9)
axes[2, 0].set_xlim([0, 255])

# Histograma en escala de grises
axes[2, 1].bar(rango, hist_gris, color='gray', alpha=0.7, width=1.0)
axes[2, 1].axvline(x=moda_gris, color='black', linestyle='--', linewidth=2,
                   label=f'Moda={moda_gris}')
axes[2, 1].set_title(f"Histograma Escala de Grises\nModa: {moda_gris}", fontsize=11,
                     fontweight='bold')
axes[2, 1].set_xlabel("Intensidad (0-255)")
axes[2, 1].set_ylabel("Frecuencia")
axes[2, 1].legend(fontsize=9)
axes[2, 1].set_xlim([0, 255])

# Histograma acumulado
hist_R_acum = np.cumsum(hist_R_pil)
hist_G_acum = np.cumsum(hist_G_pil)
hist_B_acum = np.cumsum(hist_B_pil)

axes[2, 2].plot(rango, hist_R_acum, color='red', linewidth=2, label='Rojo')
axes[2, 2].plot(rango, hist_G_acum, color='green', linewidth=2, label='Verde')
axes[2, 2].plot(rango, hist_B_acum, color='blue', linewidth=2, label='Azul')
axes[2, 2].set_title("Histograma Acumulado RGB", fontsize=11, fontweight='bold')
axes[2, 2].set_xlabel("Intensidad (0-255)")
axes[2, 2].set_ylabel("Frecuencia Acumulada")
axes[2, 2].legend(fontsize=9)
axes[2, 2].set_xlim([0, 255])

# Ajustar espaciado
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(directorio, "ejercicio_6_resultado.png"), dpi=150, bbox_inches='tight')
print(f"Figura completa guardada como: ejercicio_6_resultado.png")
plt.show()

print("\n" + "=" * 60)
print("  Ejercicio 6 completado exitosamente.")
print("=" * 60)
