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

descripcion = "Poligonos de los municipios que abarcan las coordinaciones de zona del IVEA"
output = "coordinaciones_zona"

# config base
layer = {
    "type": "POLYGON",
    'data':{
        'table' : 'marco_geoestadistico.mun_coordinaciones',
        'select': ['clv_zona']
    },
    "class" : {
         "style": {
             "color":"",
             "opacity": 60,
             "outlinecolor": "60,60,60",
             "width": 0.8

         }
    }
}

layers = []
for cz in coordinaciones:
    layers.append(
        {
            "name": f"{cz['id_capa']}",
            "metadata": {
                'wms_title': f"Coordinación de Zona {cz['nombre']}",
            },
            "data":{
                "where": f"clv_zona = {cz['id_cz']}",
            },
            "class" : {
                "style":
                {
                    "color": f"{cz['color']}",
                    "outlinecolor": f"{cz['color']}",
                }
            }
        }
    )

