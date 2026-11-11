import sys
import os

descripcion = "Rezago educativo por manzanas, Censo 2020"
output = "rez_loc_urb_manzanas"


# CONFIGURACIONES GLOBALES
tabla = "rezago_educativo_censo_2020.rez_loc_urb_manzanas_limpio"

layer = {
    'type' : 'POLYGON',
    "data": {
        'table': tabla,
    },
}

style_base =  {
    'outlinecolor': '205,205,205',
    "width" : 0.8,
}


mapas_tematico = [
    "analfabeta",
    #"sin_prim",
    #"sin_sec",
    #"rez_total",
]

wms_titles = [
    "de analfabetismo",
    #"sin primaria",
    #"sin secundaria",
    #"total de Rezago Educativo",
]

# construccion de las capas
layers = []
t=0

for campo in mapas_tematico:    
    clases = []
    # se recorre los colores y las condicionales
    for i in range(4):
        clases.append(
            {
                "name": f'estilo para el campo {campo}',
                "style": style_base,
                "label": {
                    "font": "arial",
                    "size": "10",
                    "color": "0 0 0",
                    "outlinecolor": "255 255 255",
                    "buffer": '5',
                    "position": "cc",
                    "type": "truetype"
                }
            },
            
        )
    layers.append({
        "name": f"rezago_educativo_{campo}_loc_urb_manzana",
        # "data": {
        #     "select": [campo]
        # },
        "labelitem": campo,
        "metadata": {
            'wms_title': f"Rezago {wms_titles[t]} por localidad urbana (manzana)"
        },
        "class": clases,
        "_tree": {
            "grupo": "test",
        },
    })
    t=t+1
    

