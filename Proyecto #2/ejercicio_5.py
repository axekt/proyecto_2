from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(directorio, "fig_05.jpg") 

print("=" * 60)
print("  EJERCICIO 5: Separación de Planos R, G, B")
print("=" * 60)

img = Image.open(ruta_imagen).convert("RGB")
print(f"\nImagen original: fig_05.jpg")
print(f"  Tamaño: {img.size[0]} x {img.size[1]} píxeles")
print(f"  Modo: {img.mode}")
print(f"  Total de píxeles: {img.size[0] * img.size[1]:,}")

plano_R, plano_G, plano_B = img.split()

arr_R = np.array(plano_R)
arr_G = np.array(plano_G)
arr_B = np.array(plano_B)

total_pixeles = arr_R.size

umbral = 30

pixeles_R = np.sum(arr_R > umbral)
pixeles_G = np.sum(arr_G > umbral)
pixeles_B = np.sum(arr_B > umbral)

porcentaje_R = (pixeles_R / total_pixeles) * 100
porcentaje_G = (pixeles_G / total_pixeles) * 100
porcentaje_B = (pixeles_B / total_pixeles) * 100

print(f"\n{'-' * 55}")
print(f"  Análisis de Área por Plano (umbral = {umbral})")
print(f"{'-' * 55}")
print(f"  {'Plano':<12} {'Píxeles Activos':>18} {'Porcentaje':>12}")
print(f"{'-' * 55}")
print(f"  {'Rojo (R)':<12} {pixeles_R:>18,} {porcentaje_R:>11.2f}%")
print(f"  {'Verde (G)':<12} {pixeles_G:>18,} {porcentaje_G:>11.2f}%")
print(f"  {'Azul (B)':<12} {pixeles_B:>18,} {porcentaje_B:>11.2f}%")
print(f"{'-' * 55}")
print(f"  {'Total':<12} {total_pixeles:>18,} {'100.00%':>12}")
print(f"{'-' * 55}")

print(f"\n{'-' * 55}")
print(f"  Estadísticas de Intensidad por Plano")
print(f"{'-' * 55}")
for nombre, arr, color in [("Rojo (R)", arr_R, "R"),
                             ("Verde (G)", arr_G, "G"),
                             ("Azul (B)", arr_B, "B")]:
    print(f"\n  Plano {nombre}:")
    print(f"    Mínimo:    {arr.min()}")
    print(f"    Máximo:    {arr.max()}")
    print(f"    Media:     {arr.mean():.2f}")
    print(f"    Desv.Std:  {arr.std():.2f}")

img_solo_R = Image.merge("RGB", (plano_R, Image.new("L", img.size, 0), Image.new("L", img.size, 0)))
img_solo_G = Image.merge("RGB", (Image.new("L", img.size, 0), plano_G, Image.new("L", img.size, 0)))
img_solo_B = Image.merge("RGB", (Image.new("L", img.size, 0), Image.new("L", img.size, 0), plano_B))

fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle("Ejercicio 5: Separación de Planos R, G, B - Imagen de Neuronas",
             fontsize=16, fontweight='bold', y=0.98)

axes[0, 0].imshow(img)
axes[0, 0].set_title("Imagen Original", fontsize=12, fontweight='bold')
axes[0, 0].axis('off')

axes[0, 1].imshow(arr_R, cmap='gray')
axes[0, 1].set_title(f"Plano R (gris)\nÁrea: {porcentaje_R:.2f}%", fontsize=11)
axes[0, 1].axis('off')

axes[0, 2].imshow(arr_G, cmap='gray')
axes[0, 2].set_title(f"Plano G (gris)\nÁrea: {porcentaje_G:.2f}%", fontsize=11)
axes[0, 2].axis('off')

axes[0, 3].imshow(arr_B, cmap='gray')
axes[0, 3].set_title(f"Plano B (gris)\nÁrea: {porcentaje_B:.2f}%", fontsize=11)
axes[0, 3].axis('off')

axes[1, 0].imshow(img_solo_R)
axes[1, 0].set_title(f"Plano Rojo\n{pixeles_R:,} px", fontsize=11, color='red')
axes[1, 0].axis('off')

axes[1, 1].imshow(img_solo_G)
axes[1, 1].set_title(f"Plano Verde\n{pixeles_G:,} px", fontsize=11, color='green')
axes[1, 1].axis('off')

axes[1, 2].imshow(img_solo_B)
axes[1, 2].set_title(f"Plano Azul\n{pixeles_B:,} px", fontsize=11, color='blue')
axes[1, 2].axis('off')

colores = ['#FF4444', '#44BB44', '#4444FF']
nombres = ['Rojo (R)', 'Verde (G)', 'Azul (B)']
valores = [porcentaje_R, porcentaje_G, porcentaje_B]
barras = axes[1, 3].bar(nombres, valores, color=colores, edgecolor='black', linewidth=0.5)
axes[1, 3].set_title("Área Ocupada por Canal (%)", fontsize=11, fontweight='bold')
axes[1, 3].set_ylabel("Porcentaje (%)")
axes[1, 3].set_ylim(0, 100)

for barra, valor in zip(barras, valores):
    axes[1, 3].text(barra.get_x() + barra.get_width() / 2., barra.get_height() + 1,
                    f'{valor:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(directorio, "ejercicio_5_resultado.png"), dpi=150, bbox_inches='tight')
print(f"\nFigura completa guardada como: ejercicio_5_resultado.png")
plt.show()

print("\n" + "=" * 60)
print("  Ejercicio 5 completado exitosamente.")
print("=" * 60)