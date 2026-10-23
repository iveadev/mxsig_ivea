import sys
import os

# Import de la definición de coordinaciones de zona
sys.path.append(os.getcwd())
from scripts.layers.constantes import coordinaciones

#==========================================================================
# Definición de la capa
#==========================================================================

descripcion = "Mapa tematico con los municipios que abarcan las coordinaciones de zona del IVEA"
output = "tematico_coordinaciones_zona"

# config base
style_base = {
    "outlinecolor": "0,0,0",
}

label_base = {
    "font": "arial",
    "size": "8",
    "color": "0 0 0",
    "outlinecolor": "255 255 255",
    'priority': 10,
    'buffer': 1,
    'position': 'uc',
    "type": "truetype"
}

classes = []
for cz in coordinaciones:
    classes.append(
        {
            "name": f"{cz['nombre']}",
            "expression": f"[clv_zona] = {cz['id_cz']}",
            "style":
            style_base | # herencia de diccionarios
            {
                "color": f"{cz['color']}",
                "opacity": 60,
                "outlinecolor": f"{cz['color']}",
                "width": 0.8
            },
            'label': label_base,
        }
    )

layer = {
    "name": "coordinaciones_zona_tematico",
    "type": "POLYGON",
    "metadata": {
         'wms_title': descripcion,
    },
    "data" : {
        "table": "ivea.cz_disuelto",
        "select":["clv_zona"],
    },
    "class" : classes,
    "labelitem": 'coord_zon',
}
