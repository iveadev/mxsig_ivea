import sys
import os

sys.path.append(os.getcwd())
from scripts.utils.postgres import obtener_cuartiles_desde_postgres

descripcion = "Rezago educativo por edad y sexo Censo 2020"
output = "rezago_municipios_edad_sexo"


# Tablas
esquema = 'rezago_educativo_censo_2020.rez_educ_edad_sexo_2020_'
tablas = [
    'alfa',
    'sin_prim',
    'sin_sec',
]


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


totales = [ # se le concatena el nombre del nivel
    'hombres',
    'mujeres'
]

titulos = [
    "en condición de analfabetismo",
    "sin primaria terminada",
    "sin secundaria terminada",
]

grupo = 'rezago_censo_2020_' # nombrew base para el grupo


# construccion de las capas
layers = []
for idx in range(3):
    #variables
    prefijo = tablas[idx]
    tabla = esquema+prefijo
    for campo_t in totales:
        campo=prefijo+'_'+campo_t
        print(f"{tabla},{campo}")
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
            "name": f"rezago_educativo_sexo_edad_{campo}",
             "data": {
                "table": tabla,
                "select": [campo]
            },
            "labelitem": campo,
            "metadata": {
                'wms_title': f"{campo_t.capitalize()} {titulos[idx]}"
            },
            "class": clases,
            "_tree": {
                "grupo": "rezago_censo_2020_edades_y_sexo",
            },
        })

