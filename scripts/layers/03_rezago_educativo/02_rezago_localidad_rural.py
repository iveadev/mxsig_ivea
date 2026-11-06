import sys
import os

sys.path.append(os.getcwd())
#from scripts.utils.postgres import obtener_cuartiles_desde_postgres

#==========================================================================
# Definición de la capa
#==========================================================================

descripcion = "Localidades rurales con rezago educativo Censo 2020"
output = "rezago_localidades_rurales"


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

style_base =  {
    "symbol": 'circulor',
    "size": 10,
    "outlinecolor": "0,0,0",
}


# construccion de las capas
layers = []
#for campo in campos:
for i in range(4):
    # q1, q2, q3 = obtener_cuartiles_desde_postgres(tabla, campo)
    # #condicionales de acuerdo a los cuartiles generados a partir de los datos de la DB
    # condicionales = [
    #     f"[{campo}] <={q1}",
    #     f"[{campo}] >{q1} and [{campo}] <={q2}",
    #     f"[{campo}] >{q2} and [{campo}] <={q3}",
    #     f"[{campo}] >{q3}",
    # ]
    #clases = []
    # se recorre los colores y las condicionales
    
    campo = campos[i]
    color = colores[i]
        # clases.append(
        #     {
        #         "name": estilo['name'],
        #         "expression": condicionales[i],
        #         "style": style_base | {
        #             "color": estilo['color'],
        #             "outlinecolor": estilo['color'],
        #         },
        #         "label": {
        #             "font": "arial",
        #             "size": "10",
        #             "color": "0 0 0",
        #             "outlinecolor": "255 255 255",
        #             "buffer": '5',
        #             "position": "uc",
        #             "type": "truetype"
        #         }
        #     },
            
        # )
    layers.append({
        "name": campo,
        "data": {
            "select": [campo]
        },
        "labelitem": 'nomgeo',
        "metadata": {
            'wms_title': f"Número de personas {wms_titles[i]} por localidad rural"
        },
        "class": style_base | {
            "color": color,
        },
        "label": {
            "font": "arial",
            "size": "10",
            "color": "0 0 0",
            "outlinecolor": "255 255 255",
            "buffer": '5',
            "position": "uc",
            "type": "truetype"
        },
        "_tree": {
            "grupo": "rezago_educativo_censo",
        },
    })

