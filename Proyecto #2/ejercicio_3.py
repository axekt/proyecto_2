"""
EJERCICIO 3: Separación de canales RGB y conversión a escala de grises
=====================================================================

Dada una imagen fotográfica a color (imagen "b"):
    1. Separa sus planos de color R, G y B.
    2. Grafica cada plano de forma individual con Matplotlib.
    3. Convierte la imagen original a escala de grises.

La conversión a gris se realiza con OpenCV y también manualmente con la
fórmula de luminancia ITU-R BT.601:
    Gris = 0.299·R + 0.587·G + 0.114·B
"""

import os 

import cv2 
import numpy as np 
import matplotlib .pyplot as plt 

directorio =os .path .dirname (os .path .abspath (__file__ ))




RUTA_IMAGEN_B =os .path .join (directorio ,"flores.png")
RUTA_SALIDA_CANALES =os .path .join (directorio ,"ejercicio_3_canales.png")
RUTA_SALIDA_GRIS =os .path .join (directorio ,"ejercicio_3_gris.png")
RUTA_IMAGEN_GRIS =os .path .join (directorio ,"flores_gris.png")

NOMBRES_CANALES =("Rojo (R)","Verde (G)","Azul (B)")
COLORES_HIST =("#e23d4a","#2ea860","#346ee6")


def cargar_imagen_rgb (ruta ):
    """
    Carga una imagen a color con OpenCV y la convierte de BGR a RGB
    (Matplotlib espera el orden RGB).

    Parámetros
    ----------
    ruta : str
        Ruta del archivo de imagen.

    Retorna
    -------
    np.ndarray (alto, ancho, 3) uint8 en orden RGB.
    """
    img_bgr =cv2 .imread (ruta ,cv2 .IMREAD_COLOR )
    if img_bgr is None :
        raise FileNotFoundError (f"No se pudo cargar la imagen: {ruta }")
    return cv2 .cvtColor (img_bgr ,cv2 .COLOR_BGR2RGB )


def separar_canales (img_rgb ):
    """
    Separa la imagen RGB en sus tres planos de color.

    Retorna
    -------
    (R, G, B) : tupla de matrices 2D uint8 (una intensidad por píxel).
    """
    r ,g ,b =cv2 .split (img_rgb )
    return r ,g ,b 


def canal_coloreado (canal ,indice ):
    """
    Construye una imagen RGB donde solo el canal 'indice' conserva sus
    valores y los otros dos se ponen en cero (visualización "teñida").
    """
    img =np .zeros ((*canal .shape ,3 ),dtype =np .uint8 )
    img [:,:,indice ]=canal 
    return img 


def convertir_a_gris (img_rgb ):
    """
    Convierte la imagen RGB a escala de grises por dos métodos:

    1. OpenCV: cv2.cvtColor(..., COLOR_RGB2GRAY)
    2. Manual: Gris = 0.299·R + 0.587·G + 0.114·B

    Retorna
    -------
    (gris_opencv, gris_manual) : matrices 2D uint8.
    """
    gris_opencv =cv2 .cvtColor (img_rgb ,cv2 .COLOR_RGB2GRAY )

    r ,g ,b =[c .astype (np .float64 )for c in separar_canales (img_rgb )]
    gris_manual =np .clip (np .round (0.299 *r +0.587 *g +0.114 *b ),0 ,255 ).astype (np .uint8 )

    return gris_opencv ,gris_manual 


def graficar_canales (img_rgb ,canales ,ruta_salida =None ):
    """
    Grafica con Matplotlib la imagen original y cada plano de color de
    forma individual:
        Fila 1: original + cada canal como intensidad (mapa de grises).
        Fila 2: histograma de los 3 canales + cada canal "teñido" en su color.
    """
    fig ,axes =plt .subplots (2 ,4 ,figsize =(20 ,9 ))
    fig .suptitle ("Ejercicio 3: Separación de los planos de color R, G, B",
    fontsize =16 ,fontweight ="bold")


    axes [0 ,0 ].imshow (img_rgb )
    axes [0 ,0 ].set_title ("Imagen original \"b\" (RGB)",fontsize =12 ,fontweight ="bold")
    axes [0 ,0 ].axis ("off")


    max_interno =0 
    for canal ,nombre ,color in zip (canales ,NOMBRES_CANALES ,COLORES_HIST ):
        hist =cv2 .calcHist ([canal ],[0 ],None ,[256 ],[0 ,256 ]).ravel ()
        max_interno =max (max_interno ,hist [1 :255 ].max ())
        axes [1 ,0 ].plot (hist ,color =color ,label =nombre ,linewidth =1.4 )
        axes [1 ,0 ].fill_between (range (256 ),hist ,color =color ,alpha =0.15 )
    axes [1 ,0 ].set_title ("Histograma por canal",fontsize =12 ,fontweight ="bold")
    axes [1 ,0 ].set_xlim (0 ,255 )


    axes [1 ,0 ].set_ylim (0 ,max_interno *1.15 )
    axes [1 ,0 ].set_xlabel ("Nivel de intensidad")
    axes [1 ,0 ].set_ylabel ("Frecuencia")
    axes [1 ,0 ].legend ()
    axes [1 ,0 ].grid (alpha =0.3 )


    for i ,(canal ,nombre )in enumerate (zip (canales ,NOMBRES_CANALES )):

        axes [0 ,i +1 ].imshow (canal ,cmap ="gray",vmin =0 ,vmax =255 )
        axes [0 ,i +1 ].set_title (f"Canal {nombre } – intensidad\n"
        f"media = {canal .mean ():.1f}",fontsize =11 )
        axes [0 ,i +1 ].axis ("off")


        axes [1 ,i +1 ].imshow (canal_coloreado (canal ,i ))
        axes [1 ,i +1 ].set_title (f"Canal {nombre } – teñido",fontsize =11 )
        axes [1 ,i +1 ].axis ("off")

    plt .tight_layout (rect =[0 ,0 ,1 ,0.95 ])
    if ruta_salida :
        fig .savefig (ruta_salida ,dpi =150 ,bbox_inches ="tight")
        print (f"  Figura de canales guardada como: {os .path .basename (ruta_salida )}")
    return fig 


def graficar_gris (img_rgb ,gris_opencv ,gris_manual ,ruta_salida =None ):
    """
    Grafica la imagen original junto a sus versiones en escala de grises
    (OpenCV y fórmula manual) y el mapa de diferencias entre ambas.
    """
    diferencia =cv2 .absdiff (gris_opencv ,gris_manual )

    fig ,axes =plt .subplots (1 ,4 ,figsize =(20 ,5 ))
    fig .suptitle ("Ejercicio 3: Conversión a escala de grises",fontsize =16 ,fontweight ="bold")

    axes [0 ].imshow (img_rgb )
    axes [0 ].set_title ("Original (RGB)",fontsize =12 )

    axes [1 ].imshow (gris_opencv ,cmap ="gray",vmin =0 ,vmax =255 )
    axes [1 ].set_title ("Gris – cv2.cvtColor(RGB2GRAY)",fontsize =12 )

    axes [2 ].imshow (gris_manual ,cmap ="gray",vmin =0 ,vmax =255 )
    axes [2 ].set_title ("Gris – 0.299R + 0.587G + 0.114B",fontsize =12 )

    im =axes [3 ].imshow (diferencia ,cmap ="magma",vmin =0 ,vmax =max (1 ,int (diferencia .max ())))
    axes [3 ].set_title (f"|OpenCV − Manual|  (máx = {diferencia .max ()})",fontsize =12 )
    fig .colorbar (im ,ax =axes [3 ],fraction =0.035 ,pad =0.02 )

    for ax in axes :
        ax .axis ("off")

    plt .tight_layout (rect =[0 ,0 ,1 ,0.92 ])
    if ruta_salida :
        fig .savefig (ruta_salida ,dpi =150 ,bbox_inches ="tight")
        print (f"  Figura de escala de grises guardada como: {os .path .basename (ruta_salida )}")
    return fig 


def procesar_imagen_b (ruta ,mostrar =True ):
    """
    Script completo del ejercicio: carga la imagen "b", separa y grafica
    sus canales R, G, B y la convierte a escala de grises.

    Retorna
    -------
    dict con 'canales' (R, G, B), 'gris_opencv' y 'gris_manual'.
    """
    img_rgb =cargar_imagen_rgb (ruta )
    alto ,ancho ,_ =img_rgb .shape 
    print (f"\nImagen: {os .path .basename (ruta )}")
    print (f"  Tamaño: {ancho } x {alto } píxeles  |  Canales: {img_rgb .shape [2 ]}")


    print ("\n--- Separación de canales ---")
    canales =separar_canales (img_rgb )
    for canal ,nombre in zip (canales ,NOMBRES_CANALES ):
        print (f"  {nombre :<10} forma={canal .shape }  media={canal .mean ():7.2f}  "
        f"mín={canal .min ():3d}  máx={canal .max ():3d}")
    graficar_canales (img_rgb ,canales ,RUTA_SALIDA_CANALES )


    print ("\n--- Conversión a escala de grises ---")
    gris_opencv ,gris_manual =convertir_a_gris (img_rgb )
    print (f"  Gris OpenCV: forma={gris_opencv .shape }  media={gris_opencv .mean ():.2f}")
    print (f"  Gris manual: forma={gris_manual .shape }  media={gris_manual .mean ():.2f}")
    print (f"  Diferencia máxima entre métodos: {cv2 .absdiff (gris_opencv ,gris_manual ).max ()}")
    cv2 .imwrite (RUTA_IMAGEN_GRIS ,gris_opencv )
    print (f"  Imagen en gris guardada como: {os .path .basename (RUTA_IMAGEN_GRIS )}")
    graficar_gris (img_rgb ,gris_opencv ,gris_manual ,RUTA_SALIDA_GRIS )

    if mostrar :
        plt .show ()

    return {"canales":canales ,"gris_opencv":gris_opencv ,"gris_manual":gris_manual }


if __name__ =="__main__":
    print ("="*60 )
    print ("  EJERCICIO 3: Separación de canales y conversión a gris")
    print ("="*60 )

    procesar_imagen_b (RUTA_IMAGEN_B )

    print ("\n"+"="*60 )
    print ("  Ejercicio 3 completado exitosamente.")
    print ("="*60 )
