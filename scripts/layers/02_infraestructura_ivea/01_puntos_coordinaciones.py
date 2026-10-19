from random import randrange
import sys
import os

# Import de la definición de coordinaciones de zona
sys.path.append(os.getcwd())
from scripts.layers.constantes import coordinaciones

#==========================================================================
# Definición de la capa
#==========================================================================

descripcion = "Puntos de las Oficinas de Coordinacion IVEA"
output = "oficinas_cz"

# config base
style_base = {
    "symbol" : "circulor",
    "size": "9",
    "outlinecolor": "0,0,0",
}

label_base = {
    "font": "arial",
    "size": "8",
    "color": "0 0 0",
    "outlinecolor": "255 255 255",
    "position": "auto",
    "type": "truetype"
}

classes = []
for cz in coordinaciones:
    classes.append(
        {
            "name": f"{cz['nombre']}",
            "expression": f"[clv_cz] = {cz['id_cz']}",
            "style":
            style_base | # herencia de diccionarios
            {
                "color": f"{cz['color']}"
            },
            "label" : label_base | {
                'priority': randrange(1, 10),
            }
        }
    )

layer = {
    "name": "oficinas_cz",
    "type": "POINT",
    "metadata": {
         'wms_title': 'Puntos en donde se ubican las coordinaciones de zona del IVEA',
    },
    "data" : {
        "table": "ivea.oficinas_cz",
        "select":["clv_cz"],
    },
    "labelitem": "nom_cz",
    "class" : classes
}
