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

descripcion = "Mapa tematico con los municipios que abarcan las coordinaciones de zona del IVEA"
output = "tematico_coordinaciones_zona"

# config base
style_base = {
    "outlinecolor": "0,0,0",
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
            }
        }
    )

layer = {
    "name": "coordinaciones_zona_tematico",
    "type": "POLYGON",
    "metadata": {
         'wms_title': descripcion,
    },
    "data" : {
        "table": "marco_geoestadistico.mun_coordinaciones",
        "select":["clv_zona"],
    },
    "class" : classes
}
