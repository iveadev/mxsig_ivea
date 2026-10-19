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
layer = {
    'type' : 'POLYGON',
}



clase_base = {
    'style': {
        'outlinecolor': '0,0,0',
        "width" : 0.8
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
    {
        "campo" : "porcentaje_analfabetismo",
        "inicial":12,
        "final": 30,
    },
    {
        "campo" : "porcentaje_sin_primaria",
        "inicial":12,
        "final": 30,
    },
    {
        "campo" : "porcentaje_sin_secundaria",
        "inicial":12,
        "final": 30,
    },
    {
        "campo" : "porcentaje_rezago_total",
        "inicial":12,
        "final": 30,
    },
]

# construccion de las capas
layers = []
tabla = "rezago_educativo_estimacion_inea2025.tematico_indice_alfa"
for mapa in mapas_tematico:
    q1, q2, q3 = obtener_cuartiles_desde_postgres(tabla, mapa['campo'])
    print(q1, q2, q3)




