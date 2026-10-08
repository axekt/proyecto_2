from PIL import Image
import matplotlib.pyplot as plt
import os

directorio = os.path.dirname(os.path.abspath(__file__))

ruta_superponer = os.path.join(directorio, "fig_00.jpg")

rutas_fondo = [
    os.path.join(directorio, "fig_01.jpg"),
    os.path.join(directorio, "fig_02.jpg"),
    os.path.join(directorio, "fig_03.jpg"),
    os.path.join(directorio, "fig_04.jpg"),
]

rutas_plantillas = [
    os.path.join(directorio, "pla_01.jpg"),
    os.path.join(directorio, "pla_02.jpg"),
    os.path.join(directorio, "pla_03.jpg"),
    os.path.join(directorio, "pla_04.jpg"),
]

nombres_plantillas = ["Círculo", "Rectángulo", "Pentágono", "Corazón"]

nombres_fondo = ["Libros con planta", "Universidad", "Libro en pasto", "Libro fantástico"]

print("=" * 60)
print("  EJERCICIO 4: Composición con Plantillas Geométricas")
print("=" * 60)

img_superponer = Image.open(ruta_superponer).convert("RGB")
print(f"\nImagen a superponer: fig_00.jpg")
print(f"  Tamaño: {img_superponer.size}")
print(f"  Modo: {img_superponer.mode}")

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
fig.suptitle("Ejercicio 4: Composición de Imágenes con Plantillas Geométricas",
             fontsize=16, fontweight='bold', y=0.98)

for i in range(4):
    img_fondo = Image.open(rutas_fondo[i]).convert("RGB")
    img_plantilla = Image.open(rutas_plantillas[i]).convert("L")
    tamaño = img_fondo.size
    img_sup_resized = img_superponer.resize(tamaño, Image.LANCZOS)
    mascara_resized = img_plantilla.resize(tamaño, Image.LANCZOS)
    resultado = Image.composite(img_sup_resized, img_fondo, mascara_resized)

    print(f"\n--- Composición {i+1}: Plantilla {nombres_plantillas[i]} ---")
    print(f"  Fondo: {nombres_fondo[i]} ({img_fondo.size})")
    print(f"  Plantilla: {nombres_plantillas[i]} ({img_plantilla.size})")
    print(f"  Resultado: {resultado.size}")

    nombre_salida = f"resultado_ej4_{nombres_plantillas[i].lower()}.jpg"
    ruta_salida = os.path.join(directorio, nombre_salida)
    resultado.save(ruta_salida, quality=95)
    print(f"  Guardado como: {nombre_salida}")

    axes[i, 0].imshow(img_fondo)
    axes[i, 0].set_title(f"Fondo: {nombres_fondo[i]}", fontsize=10)
    axes[i, 0].axis('off')

    axes[i, 1].imshow(mascara_resized, cmap='gray')
    axes[i, 1].set_title(f"Plantilla: {nombres_plantillas[i]}", fontsize=10)
    axes[i, 1].axis('off')

    axes[i, 2].imshow(img_sup_resized)
    axes[i, 2].set_title("Imagen Superpuesta (Lena)", fontsize=10)
    axes[i, 2].axis('off')

    axes[i, 3].imshow(resultado)
    axes[i, 3].set_title(f"Resultado ({nombres_plantillas[i]})", fontsize=10)
    axes[i, 3].axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(directorio, "ejercicio_4_resultado.png"), dpi=150, bbox_inches='tight')
print("\n\nFigura completa guardada como: ejercicio_4_resultado.png")
plt.show()

print("\n" + "=" * 60)
print("  Ejercicio 4 completado exitosamente.")
print("=" * 60)
