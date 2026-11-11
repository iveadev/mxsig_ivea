import sys
import os

sys.path.append(os.getcwd())
from scripts.utils.postgres import obtener_cuartiles_desde_postgres

descripcion = "Rezago educativo en municipios índigenas Censo 2020"
output = "rezago_municipios_indigenas"


# CONFIGURACIONES GLOBALES
tabla = "rezago_educativo_censo_2020.rez_mun_indigena"

layer = {
    'type' : 'POLYGON',
    "data": {
        'table': tabla,
    },
}

style_base =  {
    'outlinecolor': '0,0,0',
    "width" : 0.8,
    "opacity" : 60,
}

# datos para personalizar
colores = [
  {
    "name": "bajo",
    "color": "0,128,0",
  },
  {
    "name": "medio",
    "color": "255,255,0",
  },
  {
    "name": "alto",
    "color": "240,120,15",
  },
  {
    "name": "muy_alto",
    "color": "255,0,0",
  }
]

mapas_tematico = [
    "analfabeta",
    "sin_prim",
    "sin_sec",
    "rez_total",
]

wms_titles = [
    "de analfabetismo",
    "sin primaria",
    "sin secundaria",
    "total de Rezago Educativo",
]

# construccion de las capas
layers = []
t=0
for campo in mapas_tematico:
    q1, q2, q3 = obtener_cuartiles_desde_postgres(tabla, campo)
    #condicionales de acuerdo a los cuartiles generados a partir de los datos de la DB
    condicionales = [
        f"[{campo}] <={q1}",
        f"[{campo}] >{q1} and [{campo}] <={q2}",
        f"[{campo}] >{q2} and [{campo}] <={q3}",
        f"[{campo}] >{q3}",
    ]
    clases = []
    # se recorre los colores y las condicionales
    for i in range(4):
        estilo = colores[i]
        clases.append(
            {
                "name": estilo['name'],
                "expression": condicionales[i],
                "style": style_base | {
                    "color": estilo['color'],
                    "outlinecolor": estilo['color'],
                },
                "label": {
                    "font": "arial",
                    "size": "10",
                    "color": "0 0 0",
                    "outlinecolor": "255 255 255",
                    "buffer": '5',
                    "position": "uc",
                    "type": "truetype"
                }
            },
            
        )
    layers.append({
        "name": f"rezago_educativo_{campo}",
         "data": {
            "select": [campo]
        },
        "labelitem": campo,
        "metadata": {
            'wms_title': f"Porcentaje {wms_titles[t]} en municipios índigenas"
        },
        "class": clases,
        "_tree": {
            "grupo": "rezago_educativo_censo",
        },
    })
    t=t+1

