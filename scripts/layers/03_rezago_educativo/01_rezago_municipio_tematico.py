import sys
import os

sys.path.append(os.getcwd())
from scripts.utils.postgres import obtener_cuartiles_desde_postgres

#==========================================================================
# Definición de la capa
#==========================================================================

descripcion = "Mapa tematico de la estimación del rezago educativo INEA2025"
output = "tematico_rezago_educativo_inea2025"


# CONFIGURACIONES GLOBALES
tabla = "rezago_educativo_estimacion_inea2025.tematico_indice_alfa"

layer = {
    'type' : 'POLYGON',
    "data": {
        'table': tabla,
    },
    "class": {
        'style': {
            'outlinecolor': '0,0,0',
            "width" : 0.8
        }
    }
}

# datos para personalizar
colores = [
  {
    "name": "bajo",
    "color": "255,255,0",
  },
  {
    "name": "medio",
    "color": "0,128,0",
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
    "porcentaje_analfabetismo",
    "porcentaje_sin_primaria",
    "porcentaje_sin_secundaria",
    "porcentaje_rezago_total",
]

# construccion de las capas
layers = []
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
                "style": {
                    "color": estilo['color'],
                }
            }
        )
    layers.append({
        "name": f"rezago_educativo_{campo}",
        "metadata": {
            'wms_title': f"{descripcion} ({campo})"
        },
        "class": clases
    })

