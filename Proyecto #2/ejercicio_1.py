

import os 

import cv2 
import numpy as np 
import matplotlib .pyplot as plt 

directorio =os .path .dirname (os .path .abspath (__file__ ))




RUTA_FIGURA_1A =os .path .join (directorio ,"a.png")
RUTA_FIGURA_1B =os .path .join (directorio ,"b.png")
RUTA_FIGURA_1C =os .path .join (directorio ,"c.png")
RUTA_SALIDA =os .path .join (directorio ,"ejercicio_1_resultado.png")





def cargar_imagen_binaria (ruta ):
   
    img_bgr =cv2 .imread (ruta ,cv2 .IMREAD_COLOR )
    if img_bgr is None :
        raise FileNotFoundError (f"No se pudo cargar la imagen: {ruta }")

    gris =cv2 .cvtColor (img_bgr ,cv2 .COLOR_BGR2GRAY )
    _ ,binaria =cv2 .threshold (gris ,0 ,1 ,cv2 .THRESH_BINARY_INV +cv2 .THRESH_OTSU )

    if binaria .mean ()>0.5 :
        binaria =1 -binaria 

    return img_bgr ,binaria .astype (np .uint8 )


def obtener_coordenadas (binaria ):
    filas ,columnas =np .indices (binaria .shape ,dtype =np .float64 )
    return columnas ,filas 


def momento_espacial (binaria ,p ,q ):
    x ,y =obtener_coordenadas (binaria )
    f =binaria .astype (np .float64 )
    return float (np .sum ((x **p )*(y **q )*f ))


def centroide_por_momentos (binaria ):
    m00 =momento_espacial (binaria ,0 ,0 )
    if m00 ==0 :
        raise ValueError ("La imagen no contiene ningún objeto (m00 = 0).")
    return momento_espacial (binaria ,1 ,0 )/m00 ,momento_espacial (binaria ,0 ,1 )/m00 


def momento_central (binaria ,p ,q ):
    x ,y =obtener_coordenadas (binaria )
    f =binaria .astype (np .float64 )
    x_c ,y_c =centroide_por_momentos (binaria )
    return float (np .sum (((x -x_c )**p )*((y -y_c )**q )*f ))


def momento_central_normalizado (binaria ,p ,q ):
    mu00 =momento_central (binaria ,0 ,0 )
    gamma =(p +q )/2.0 +1.0 
    return momento_central (binaria ,p ,q )/(mu00 **gamma )


def dibujar_cruz (img_bgr ,x ,y ,escala ,color ,tipo =cv2 .MARKER_CROSS ,tam =40 ,grosor =2 ):
    punto =(int (round ((x +0.5 )*escala )),int (round ((y +0.5 )*escala )))
    cv2 .drawMarker (img_bgr ,punto ,color ,markerType =tipo ,
    markerSize =tam ,thickness =grosor ,line_type =cv2 .LINE_AA )





def analizar_figura_1a (ruta ,escala =5 ):
    img_bgr ,binaria =cargar_imagen_binaria (ruta )


    area =int (np .count_nonzero (binaria ))


    ys ,xs =np .nonzero (binaria )
    cx_geo ,cy_geo =float (xs .mean ()),float (ys .mean ())


    m00 =momento_espacial (binaria ,0 ,0 )
    m10 =momento_espacial (binaria ,1 ,0 )
    m01 =momento_espacial (binaria ,0 ,1 )
    cx_mom ,cy_mom =m10 /m00 ,m01 /m00 


    M =cv2 .moments (binaria ,binaryImage =True )
    cx_cv ,cy_cv =M ["m10"]/M ["m00"],M ["m01"]/M ["m00"]


    img_marcada =cv2 .resize (img_bgr ,None ,fx =escala ,fy =escala ,
    interpolation =cv2 .INTER_NEAREST )

    dibujar_cruz (img_marcada ,cx_geo ,cy_geo ,escala ,(255 ,80 ,0 ),
    cv2 .MARKER_CROSS ,tam =50 ,grosor =3 )
    dibujar_cruz (img_marcada ,cx_mom ,cy_mom ,escala ,(0 ,0 ,0 ),
    cv2 .MARKER_TILTED_CROSS ,tam =30 ,grosor =2 )

    print ("\n--- a) Figura 1.a: Área y Centroides ---")
    print (f"  Área (píxeles del objeto):        {area }")
    print (f"  m00 = {m00 :.0f}   m10 = {m10 :.0f}   m01 = {m01 :.0f}")
    print (f"  Centroide geométrico  (x, y):     ({cx_geo :.4f}, {cy_geo :.4f})")
    print (f"  Centroide por momentos (x, y):    ({cx_mom :.4f}, {cy_mom :.4f})")
    print (f"  Centroide cv2.moments  (x, y):    ({cx_cv :.4f}, {cy_cv :.4f})")

    return {
    "area":area ,
    "centroide":(cx_geo ,cy_geo ),
    "centroide_momentos":(cx_mom ,cy_mom ),
    "centroide_opencv":(cx_cv ,cy_cv ),
    "momentos":{"m00":m00 ,"m10":m10 ,"m01":m01 },
    "imagen_marcada":cv2 .cvtColor (img_marcada ,cv2 .COLOR_BGR2RGB ),
    "binaria":binaria ,
    }





def momentos_figura_1b (ruta ,p =2 ,q =3 ,escala =5 ):
    img_bgr ,binaria =cargar_imagen_binaria (ruta )

    m_pq =momento_espacial (binaria ,p ,q )
    mu_pq =momento_central (binaria ,p ,q )
    eta_pq =momento_central_normalizado (binaria ,p ,q )
    cx ,cy =centroide_por_momentos (binaria )


    M =cv2 .moments (binaria ,binaryImage =True )
    validacion ={
    "m21":(momento_espacial (binaria ,2 ,1 ),M ["m21"]),
    "mu21":(momento_central (binaria ,2 ,1 ),M ["mu21"]),
    "nu21":(momento_central_normalizado (binaria ,2 ,1 ),M ["nu21"]),
    }

    img_marcada =cv2 .resize (img_bgr ,None ,fx =escala ,fy =escala ,
    interpolation =cv2 .INTER_NEAREST )
    dibujar_cruz (img_marcada ,cx ,cy ,escala ,(0 ,0 ,255 ),tam =40 ,grosor =3 )

    print (f"\n--- b) Figura 1.b: Momentos de orden p={p }, q={q } ---")
    print (f"  Centroide (x_c, y_c):                ({cx :.4f}, {cy :.4f})")
    print (f"  Momento de orden        m({p },{q })   = {m_pq :.6e}")
    print (f"  Momento central         mu({p },{q })  = {mu_pq :.6e}")
    print (f"  Momento central normal. eta({p },{q }) = {eta_pq :.6e}")
    print ("  Validación contra cv2.moments (orden 2,1):")
    for nombre ,(propio ,opencv )in validacion .items ():
        print (f"    {nombre :<5} propio = {propio : .6e}   OpenCV = {opencv : .6e}")

    return {
    "p":p ,"q":q ,
    "m":m_pq ,"mu":mu_pq ,"eta":eta_pq ,
    "centroide":(cx ,cy ),
    "validacion":validacion ,
    "imagen_marcada":cv2 .cvtColor (img_marcada ,cv2 .COLOR_BGR2RGB ),
    "binaria":binaria ,
    }





def momentos_hu_figura_1c (ruta ,escala =3 ):
    img_bgr ,binaria =cargar_imagen_binaria (ruta )

    eta ={f"eta{p }{q }":momento_central_normalizado (binaria ,p ,q )
    for p ,q in [(2 ,0 ),(0 ,2 ),(1 ,1 ),(3 ,0 ),(1 ,2 ),(2 ,1 ),(0 ,3 )]}

    h1 =eta ["eta20"]+eta ["eta02"]
    h2 =(eta ["eta20"]-eta ["eta02"])**2 +4 *eta ["eta11"]**2 
    h3 =(eta ["eta30"]-3 *eta ["eta12"])**2 +(3 *eta ["eta21"]-eta ["eta03"])**2 

    hu_cv =cv2 .HuMoments (cv2 .moments (binaria ,binaryImage =True )).flatten ()[:3 ]

    img_ampliada =cv2 .resize (img_bgr ,None ,fx =escala ,fy =escala ,
    interpolation =cv2 .INTER_NEAREST )

    print ("\n--- c) Figura 1.c: Momentos invariantes de Hu ---")
    for i ,(propio ,opencv )in enumerate (zip ((h1 ,h2 ,h3 ),hu_cv ),start =1 ):
        print (f"  H{i }: propio = {propio :.6e}   OpenCV = {opencv :.6e}")

    return {
    "hu":(h1 ,h2 ,h3 ),
    "hu_opencv":tuple (float (v )for v in hu_cv ),
    "eta":eta ,
    "imagen":cv2 .cvtColor (img_ampliada ,cv2 .COLOR_BGR2RGB ),
    "binaria":binaria ,
    }





def _panel_texto (ax ,titulo ,texto ):
    """Dibuja un panel de texto con formato monoespaciado en un eje."""
    ax .axis ("off")
    ax .set_title (titulo ,fontsize =12 ,fontweight ="bold")
    ax .text (0.02 ,0.95 ,texto ,transform =ax .transAxes ,va ="top",ha ="left",
    family ="monospace",fontsize =10.5 ,
    bbox =dict (boxstyle ="round,pad=0.8",facecolor ="#f4f6fb",edgecolor ="#c9d1e3"))


def graficar_resultados (res_a ,res_b ,res_c ,ruta_salida =None ,mostrar =True ):
    fig ,axes =plt .subplots (3 ,2 ,figsize =(15 ,15 ),
    gridspec_kw ={"width_ratios":[1.1 ,1 ]})
    fig .suptitle ("Ejercicio 1: Momentos y Centroides",fontsize =16 ,fontweight ="bold")


    axes [0 ,0 ].imshow (res_a ["imagen_marcada"])
    axes [0 ,0 ].set_title ("a) Figura 1.a – Centroides\n"
    "Cruz azul: geométrico  |  Aspa negra: por momentos",fontsize =11 )
    axes [0 ,0 ].axis ("off")
    cx ,cy =res_a ["centroide"]
    mx ,my =res_a ["centroide_momentos"]
    ox ,oy =res_a ["centroide_opencv"]
    _panel_texto (axes [0 ,1 ],"a) Área y Centroide",(
    f"Área (píxeles)     = {res_a ['area']}\n\n"
    f"m00 = {res_a ['momentos']['m00']:.0f}\n"
    f"m10 = {res_a ['momentos']['m10']:.0f}\n"
    f"m01 = {res_a ['momentos']['m01']:.0f}\n\n"
    f"Centroide geométrico:\n  (x, y) = ({cx :.3f}, {cy :.3f})\n\n"
    f"Centroide por momentos (m10/m00, m01/m00):\n  (x, y) = ({mx :.3f}, {my :.3f})\n\n"
    f"Verificación cv2.moments:\n  (x, y) = ({ox :.3f}, {oy :.3f})"))


    p ,q =res_b ["p"],res_b ["q"]
    axes [1 ,0 ].imshow (res_b ["imagen_marcada"])
    axes [1 ,0 ].set_title ("b) Figura 1.b – Centroide (cruz roja)",fontsize =11 )
    axes [1 ,0 ].axis ("off")
    bx ,by =res_b ["centroide"]
    texto_val ="\n".join (f"  {k :<5} propio={v [0 ]: .4e}  cv2={v [1 ]: .4e}"
    for k ,v in res_b ["validacion"].items ())
    _panel_texto (axes [1 ,1 ],f"b) Momentos de orden p={p }, q={q }",(
    f"Centroide (x_c, y_c) = ({bx :.3f}, {by :.3f})\n\n"
    f"Momento de orden            m({p },{q })   = {res_b ['m']:.6e}\n"
    f"Momento central             mu({p },{q })  = {res_b ['mu']:.6e}\n"
    f"Momento central normalizado eta({p },{q }) = {res_b ['eta']:.6e}\n\n"
    f"Validación de la implementación (orden 2,1):\n{texto_val }"))


    axes [2 ,0 ].imshow (res_c ["imagen"])
    axes [2 ,0 ].set_title ("c) Figura 1.c",fontsize =11 )
    axes [2 ,0 ].axis ("off")
    texto_hu ="\n".join (
    f"H{i } = {h :.6e}   (cv2: {hc :.6e})"
    for i ,(h ,hc )in enumerate (zip (res_c ["hu"],res_c ["hu_opencv"]),start =1 ))
    texto_eta ="\n".join (f"  {k } = {v : .6e}"for k ,v in res_c ["eta"].items ())
    _panel_texto (axes [2 ,1 ],"c) Momentos invariantes de Hu",(
    f"{texto_hu }\n\n"
    f"Momentos centrales normalizados usados:\n{texto_eta }"))

    plt .tight_layout (rect =[0 ,0 ,1 ,0.97 ])
    if ruta_salida :
        plt .savefig (ruta_salida ,dpi =150 ,bbox_inches ="tight")
        print (f"\nFigura guardada como: {os .path .basename (ruta_salida )}")
    if mostrar :
        plt .show ()
    return fig 





if __name__ =="__main__":
    print ("="*60 )
    print ("  EJERCICIO 1: Cálculo de Momentos y Centroides")
    print ("="*60 )

    resultado_a =analizar_figura_1a (RUTA_FIGURA_1A )
    resultado_b =momentos_figura_1b (RUTA_FIGURA_1B ,p =2 ,q =3 )
    resultado_c =momentos_hu_figura_1c (RUTA_FIGURA_1C )

    graficar_resultados (resultado_a ,resultado_b ,resultado_c ,ruta_salida =RUTA_SALIDA )

    print ("\n"+"="*60 )
    print ("  Ejercicio 1 completado exitosamente.")
    print ("="*60 )
