import importlib
import os

# Import de la definición de coordinaciones de zona
ruta_archivo = 'scripts/layers/00_constantes.py'
nombre_modulo = os.path.splitext(os.path.basename(ruta_archivo))[0]
spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
def_coordinaciones = importlib.util.module_from_spec(spec)
spec.loader.exec_module(def_coordinaciones)
coordinaciones = getattr(def_coordinaciones, 'coordinaciones')

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
            "expression": f"[clv_cz] = {cz['id_cz']}",
            "name": f"{cz['nombre']}",
            "style":
            style_base | # herencia de diccionarios
            {
                "color": f"{cz['color']}"
            },
            "label" : label_base
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
