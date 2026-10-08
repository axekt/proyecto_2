# ==============================================================================
# Ejercicio 4: Composición de Imágenes con Plantillas Geométricas
# ==============================================================================
# Este script superpone una imagen (fig_00 - Lena) sobre imágenes originales
# utilizando diferentes plantillas como máscara:
#   - pla_01.jpg: Círculo
#   - pla_02.jpg: Rectángulo
#   - pla_03.jpg: Pentágono
#   - pla_04.jpg: Corazón
#
# Se utiliza Image.composite() para combinar las imágenes usando la plantilla
# como máscara: donde la máscara es blanca se muestra la imagen superpuesta,
# donde es negra se muestra la imagen de fondo.
# ==============================================================================

from PIL import Image
import matplotlib.pyplot as plt
import os

# --- Configuración de rutas ---
# Directorio donde se encuentran las imágenes
directorio = os.path.dirname(os.path.abspath(__file__))

# Imagen que se va a superponer (Lena - mujer en el espejo)
ruta_superponer = os.path.join(directorio, "fig_00.jpg")

# Imágenes de fondo sobre las cuales se realizará la composición
rutas_fondo = [
    os.path.join(directorio, "fig_01.jpg"),  # Libros con planta
    os.path.join(directorio, "fig_02.jpg"),  # Edificio/universidad
    os.path.join(directorio, "fig_03.jpg"),  # Libro abierto en el pasto
    os.path.join(directorio, "fig_04.jpg"),  # Libro fantástico
]

# Plantillas geométricas (máscaras en blanco y negro)
rutas_plantillas = [
    os.path.join(directorio, "pla_01.jpg"),  # Círculo
    os.path.join(directorio, "pla_02.jpg"),  # Rectángulo
    os.path.join(directorio, "pla_03.jpg"),  # Pentágono
    os.path.join(directorio, "pla_04.jpg"),  # Corazón
]

# Nombres descriptivos para las plantillas
nombres_plantillas = ["Círculo", "Rectángulo", "Pentágono", "Corazón"]

# Nombres descriptivos para las imágenes de fondo
nombres_fondo = ["Libros con planta", "Universidad", "Libro en pasto", "Libro fantástico"]

# --- Carga de la imagen a superponer ---
print("=" * 60)
print("  EJERCICIO 4: Composición con Plantillas Geométricas")
print("=" * 60)

img_superponer = Image.open(ruta_superponer).convert("RGB")
print(f"\nImagen a superponer: fig_00.jpg")
print(f"  Tamaño: {img_superponer.size}")
print(f"  Modo: {img_superponer.mode}")

# --- Proceso de composición ---
# Crear figura con subplots: 4 filas (una por plantilla) x 4 columnas
# Columnas: [Fondo original, Plantilla, Imagen a superponer, Resultado]
fig, axes = plt.subplots(4, 4, figsize=(18, 18))
fig.suptitle("Ejercicio 4: Composición de Imágenes con Plantillas Geométricas",
             fontsize=16, fontweight='bold', y=0.98)

for i in range(4):
    # Cargar imagen de fondo
    img_fondo = Image.open(rutas_fondo[i]).convert("RGB")
    
    # Cargar plantilla (máscara)
    img_plantilla = Image.open(rutas_plantillas[i]).convert("L")  # Convertir a escala de grises
    
    # Redimensionar todas las imágenes al mismo tamaño para la composición
    # Usamos el tamaño de la imagen de fondo como referencia
    tamaño = img_fondo.size
    
    # Redimensionar la imagen a superponer al tamaño del fondo
    img_sup_resized = img_superponer.resize(tamaño, Image.LANCZOS)
    
    # Redimensionar la plantilla (máscara) al tamaño del fondo
    mascara_resized = img_plantilla.resize(tamaño, Image.LANCZOS)
    
    # Realizar la composición:
    # Image.composite(imagen1, imagen2, mascara)
    # Donde mascara blanca = imagen1, mascara negra = imagen2
    resultado = Image.composite(img_sup_resized, img_fondo, mascara_resized)
    
    # Información en consola
    print(f"\n--- Composición {i+1}: Plantilla {nombres_plantillas[i]} ---")
    print(f"  Fondo: {nombres_fondo[i]} ({img_fondo.size})")
    print(f"  Plantilla: {nombres_plantillas[i]} ({img_plantilla.size})")
    print(f"  Resultado: {resultado.size}")
    
    # Guardar resultado
    nombre_salida = f"resultado_ej4_{nombres_plantillas[i].lower()}.jpg"
    ruta_salida = os.path.join(directorio, nombre_salida)
    resultado.save(ruta_salida, quality=95)
    print(f"  Guardado como: {nombre_salida}")
    
    # --- Visualización ---
    # Columna 0: Imagen de fondo original
    axes[i, 0].imshow(img_fondo)
    axes[i, 0].set_title(f"Fondo: {nombres_fondo[i]}", fontsize=10)
    axes[i, 0].axis('off')
    
    # Columna 1: Plantilla (máscara)
    axes[i, 1].imshow(mascara_resized, cmap='gray')
    axes[i, 1].set_title(f"Plantilla: {nombres_plantillas[i]}", fontsize=10)
    axes[i, 1].axis('off')
    
    # Columna 2: Imagen a superponer
    axes[i, 2].imshow(img_sup_resized)
    axes[i, 2].set_title("Imagen Superpuesta (Lena)", fontsize=10)
    axes[i, 2].axis('off')
    
    # Columna 3: Resultado de la composición
    axes[i, 3].imshow(resultado)
    axes[i, 3].set_title(f"Resultado ({nombres_plantillas[i]})", fontsize=10)
    axes[i, 3].axis('off')

# Ajustar espaciado
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(directorio, "ejercicio_4_resultado.png"), dpi=150, bbox_inches='tight')
print("\n\nFigura completa guardada como: ejercicio_4_resultado.png")
plt.show()

print("\n" + "=" * 60)
print("  Ejercicio 4 completado exitosamente.")
print("=" * 60)
