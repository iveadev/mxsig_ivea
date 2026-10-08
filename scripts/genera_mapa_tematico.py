import os

# 1. Mapa tematico de indoce de pobreza por municipio
rangos = [
  {
    "nombre": "c_pobreza_0",
    "condicional": " porcentaje<50",
    "color": "255 255 255"
  },
  {
    "nombre": "c_pobreza_50",
    "condicional": "porcentaje>=50 and porcentaje<60",
    "color": "240 219 201"
  },
  {
    "nombre": "c_pobreza_60",
    "condicional": "porcentaje>=60 and porcentaje<70",
    "color": "204 169 137"
  },
  {
    "nombre": "c_pobreza_70",
    "condicional": "porcentaje>=70 and porcentaje<80",
    "color": "186 126 69"
  },
  {
    "nombre": "c_pobreza_80",
    "condicional": "porcentaje>=80 and porcentaje<90",
    "color": "143 98 20"
  },
  {
    "nombre": "c_pobreza_90",
    "condicional": "porcentaje>=90",
    "color": "66 52 28"
  }
]

# 2. Configuración de salida
archivo_salida = "ivea/tematico_pobreza.map"

# Plantilla base para cada una de las capas con la sintaxis de subconsulta SQL en la sección DATA para filtrar por clv_zona
plantilla_layer = """
# Capa: {nombre}
LAYER
    NAME "{id_capa}"
    STATUS ON
    TYPE POLYGON
    CONNECTIONTYPE POSTGIS
    CONNECTION "host=mxsig-db port=5432 dbname=mdm6data user=postgres password=P0stgr3s"
    DATA "the_geom FROM (SELECT gid, the_geom, porcentaje FROM coneval.indice_pobreza WHERE {condicional}) AS t1 USING UNIQUE gid USING SRID=900913"
    METADATA
        "wms_title" "{nombre}"
        "wms_enable_request" "*"
    END
    CLASS
        NAME "{nombre}"
        STYLE
            COLOR {color_rgb}
            OUTLINECOLOR 60 60 60
            OPACITY 60
            WIDTH 0.8
        END
    END
END
"""

print(f"Generando archivo {archivo_salida}...")

with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write("# =================================================================\n")
    f.write("# ARCHIVO GENERADO AUTOMÁTICAMENTE: Indice de pobreza \n")
    f.write("# Mapa tematico del indice de pobreza segun CONEVAL \n")
    f.write("# =================================================================\n\n")
    
    for rango in rangos:
        
        # Reemplazamos los valores en la plantilla
        layer_renderizado = plantilla_layer.format(
            nombre=rango['nombre'],
            id_capa=rango['nombre'],
            condicional= rango['condicional'],
            color_rgb=rango['color']
        )
        
        f.write(layer_renderizado)

print("¡Archivo generado con éxito!")
