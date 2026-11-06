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

def intensificar_rgb(rgb_str, factor):
    rgb = [int(x) for x in rgb_str.split(',')]
    nuevos_canales = [max(0, int(c * factor)) for c in rgb]
    return " ".join(str(c) for c in nuevos_canales)

style_base =  {
    "symbol": 'circulor',
    "size": 10,
    "outlinecolor": "0,0,0",
}


# construccion de las capas
layers = []
#for campo in campos:
for i in range(4):
    campo = campos[i]
    color = colores[i]
    color2 = intensificar_rgb(color,0.75)
    color3 = intensificar_rgb(color,0.5)

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
            'maxdistance': 40,
            'region': 'ellipse',
        },
        'classitem': cluster_count,
        "class": [
            style_base | {
            "color": color,
            'expression': f'[{cluster_count}] = 1'
            },
            style_base | {
            "color": color2,
            'expression': f'[{cluster_count}] > 1 AND [{cluster_count}] <= 100'
            },
            style_base | {
            "color": color3,
            'expression': f'[{cluster_count}] > 100'
            }
        ],
        "_tree": {
            "grupo": "rezago_educativo_censo",
        },
    })

