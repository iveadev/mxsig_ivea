import colorsys
import sys
import os

sys.path.append(os.getcwd())
#from scripts.utils.postgres import obtener_cuartiles_desde_postgres

#==========================================================================
# Definición de la capa
#==========================================================================

descripcion = "Localidades rurales con rezago educativo Censo 2020"
output = "rezago_localidades_rurales"
cluster_count = "Cluster_FeatureCount"


# CONFIGURACIONES GLOBALES
tabla = "rezago_educativo_censo_2020.rez_loc_rur"

layer = {
    'type' : 'POINT',
    "data": {
        'table': tabla,
    },
    "processing":"CLOSE_CONNECTION=DEFER",
}

campos = [
    'analfabetas',
    'sin_primaria',
    'sin_secundaria',
    'rezago_total',
]

wms_titles = [
    'en Rezago Educativo',
    'en condición de analfabetizmo',
    'sin primaria terminada',
    'sin secundaria terminada'    
]

colores = [
    '42,212,48',  #verde
    '194,35,194', #fuscia
    '18,67,227',  #azul
    '245,90,7',   #naranja
]

style_base =  {
    "symbol": 'circulor',
    "size": 10,
    "outlinecolor": "0,0,0",
}


def intensificar_rgb(rgb_str, factor):
    # 1. Separar y normalizar a rango 0.0 - 1.0 para colorsys
    r, g, b = [int(x) / 255.0 for x in rgb_str.split(',')]
    
    # 2. Convertir RGB a HSL (Hue, Lightness, Saturation)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # 3. Modificar: Bajamos la luminosidad con el factor, pero forzamos saturación al máximo (1.0)
    # Esto hace que el color sea oscuro pero extremadamente "vivo" (no lodoso)
    l_nueva = max(0.12, min(1.0, l * factor))
    s_nueva = 1.0 if factor < 1.0 else s # Forzar viveza en los grupos oscuros
    
    # 4. Volver a convertir a RGB y escalar a 0-255
    r_n, g_n, b_n = colorsys.hls_to_rgb(h, l_nueva, s_nueva)
    nuevos_canales = [int(r_n * 255), int(g_n * 255), int(b_n * 255)]
    
    # Retornamos con comas (o espacios según lo procese tu script posterior)
    return ",".join(str(c) for c in nuevos_canales)


# construccion de las capas
layers = []
#for campo in campos:
for i in range(4):
    campo = campos[i]
    color = colores[i]
    bajo = ["255 255 204","217 170 40"]
    medio = ["210 80 10","65 182 196"]
    alto = ["150 10 15","8 29 88"]

    layers.append({
        "name": campo,
        "data": {
            "select": [campo]
        },
        #"labelitem": 'nomgeo',
        "metadata": {
            'wms_title': f"Número de personas {wms_titles[i]} por localidad rural"
        },
        'cluster': {
            'maxdistance': 65,
            'region': 'rectangle',
            'buffer': 0,
        },
        'classitem': cluster_count,
        "class": [
            style_base | {
            "color": color,
            'outlinecolor': color,
            'size': 10,
            'expression': f'[{cluster_count}] = 1'
            },
            style_base | {
            "color": bajo[1],
            'outlinecolor': bajo[0],
            'size': 20,
            'expression': f'[{cluster_count}] > 1 AND [{cluster_count}] < 50'
            },
            style_base | {
            "color": medio[1],
            'outlinecolor': medio[0],
            'size': 40,
            'expression': f'[{cluster_count}] >= 50 AND [{cluster_count}] < 500'
            },
            style_base | {
            "color": alto[1],
            'outlinecolor': alto[0],
            'size': 60,
            'expression': f'[{cluster_count}] >= 500'
            }
        ],
        "_tree": {
            "grupo": "rezago_educativo_censo",
        },
    })

