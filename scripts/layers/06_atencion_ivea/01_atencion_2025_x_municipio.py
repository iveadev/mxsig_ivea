import sys
import os

sys.path.append(os.getcwd())
from scripts.utils.postgres import obtener_cuartiles_desde_postgres

descripcion = "Atención IVEA 2025"
output = "atencion_ivea_2025_x_municipio"


# Tablas
tabla = 'ivea.resultados_por_municipio_2025'
niveles = [
    'alfa',
    'prim',
    'sec',
    'total',
]
atn= [
    'inc',
    'atn',
    'ucn',
]
campos = []
for a in atn:
    for n in niveles:
        campos.append(f"{a}_{n}")

titulos_nivel = [
    "en alfabetización",
    "en primaria",
    "en secundaria",
    "totales",
]
titulos_atn = [
    "incorporación",
    "atención",
    "conclución de nivel",
]
titulos = []
for ta in titulos_atn:
    for tn in titulos_nivel:
        titulos.append(f"Resultados de {ta} {tn}")

layer = {
    'type' : 'POLYGON',
}

style_base =  {
    'outlinecolor': '0,0,0',
    "width" : 0.8,
    "opacity" : 60,
}

# datos para personalizar
colores = [
    {
        "name": "nulo",
        "color": "80,80,80",
    },
    {
        "name": "bajo",
        "color": "255,0,0",
    },
    {
        "name": "medio",
        "color": "240,120,15",
    },
    {
        "name": "alto",
        "color": "255,255,0",
    },

    {
        "name": "muy_alto",
        "color": "0,128,0",
    },
]

# construccion de las capas
layers = []
t=0
for campo in campos:
    q1, q2, q3 = obtener_cuartiles_desde_postgres(tabla, campo)
    #condicionales de acuerdo a los cuartiles generados a partir de los datos de la DB
    condicionales = [
        f"[{campo}] = 0",
        f"[{campo}] >=1 and [{campo}] <={q1}",
        f"[{campo}] >{q1} and [{campo}] <={q2}",
        f"[{campo}] >{q2} and [{campo}] <={q3}",
        f"[{campo}] >{q3}",
    ]
    clases = []
    # se recorre los colores y las condicionales
    for i in range(5):
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
        "name": f"atencion_ivea_2025_{campo}",
         "data": {
            "table": tabla,
            "select": [campo]
        },
        "labelitem": campo,
        "metadata": {
            'wms_title': f"{titulos[t]}"
        },
        "class": clases,
        "_tree": {
            "grupo": "atencion_ivea_2025",
        },
    })
    t=t+1

