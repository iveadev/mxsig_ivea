import os

# 1. Catálogo de Coordinaciones de Zona (Nombre de capa, clave y color RGB asignado)
coordinaciones = [
    {"id": "cz3001",    "clv_zona": "1",  "nombre": "Tantoyuca",       "color": "235 151 78"},
    {"id": "cz3003",    "clv_zona": "3",  "nombre": "Chicontepec",     "color": "93 188 210"},
    {"id": "cz3004",    "clv_zona": "4",  "nombre": "Tuxpan",          "color": "158 53 147"},
    {"id": "cz3005",    "clv_zona": "5",  "nombre": "Poza Rica",       "color": "196 46 96"},
    {"id": "cz3006",    "clv_zona": "6",  "nombre": "Papantla",        "color": "74 163 113"},
    {"id": "cz3007",    "clv_zona": "7",  "nombre": "Espinal",         "color": "249 220 101"},
    {"id": "cz3008",    "clv_zona": "8",  "nombre": "Martinez",        "color": "235 151 78"},
    {"id": "cz3009",    "clv_zona": "9",  "nombre": "Perote",          "color": "93 188 210"},
    {"id": "cz3010",    "clv_zona": "10", "nombre": "Xalapa",          "color": "158 53 147"},
    {"id": "cz3011",    "clv_zona": "11", "nombre": "Coatepec",        "color": "196 46 96"},
    {"id": "cz3012",    "clv_zona": "12", "nombre": "Huatusco",        "color": "74 163 113"},
    {"id": "cz3013",    "clv_zona": "13", "nombre": "Orizaba",         "color": "249 220 101"},
    {"id": "cz3014",    "clv_zona": "14", "nombre": "Cordoba",         "color": "235 151 78"},
    {"id": "cz3015",    "clv_zona": "15", "nombre": "Zongolica",       "color": "93 188 210"},
    {"id": "cz3016",    "clv_zona": "16", "nombre": "Veracruz",        "color": "158 53 147"},
    {"id": "cz3017",    "clv_zona": "17", "nombre": "Boca del Rio",    "color": "196 46 96"},
    {"id": "cz3018",    "clv_zona": "18", "nombre": "Tierra Blanca",   "color": "74 163 113"},
    {"id": "cz3019",    "clv_zona": "19", "nombre": "Cosamaloapan",    "color": "249 220 101"},
    {"id": "cz3020",    "clv_zona": "20", "nombre": "San Andres",      "color": "235 151 78"},
    {"id": "cz3021",    "clv_zona": "21", "nombre": "Acayucan",        "color": "93 188 210"},
    {"id": "cz3022",    "clv_zona": "22", "nombre": "Minatitlan",       "color": "158 53 147"},
    {"id": "cz3023",    "clv_zona": "23", "nombre": "Coatzacoalcos",   "color": "196 46 96"},
    {"id": "cz3024",    "clv_zona": "24", "nombre": "Huayacocotla",    "color": "74 163 113"},
    {"id": "cz3025",    "clv_zona": "25", "nombre": "Panuco",          "color": "249 220 101"},
    {"id": "cz3029",    "clv_zona": "29", "nombre": "Jaltipan",        "color": "235 151 78"}
]

# 2. Configuración de salida
archivo_salida = "ivea/coordinaciones.map"

# Plantilla base para cada una de las capas con la sintaxis de subconsulta SQL en la sección DATA para filtrar por clv_zona
plantilla_layer = """
# Coordinación de Zona: {nombre}
LAYER
    NAME "{id_capa}"
    STATUS ON
    TYPE POLYGON
    CONNECTIONTYPE POSTGIS
    CONNECTION "host=mxsig-db port=5432 dbname=mdm6data user=postgres password=P0stgr3s"
    DATA "the_geom FROM (SELECT gid, the_geom, clv_zona FROM marco_geoestadistico.mun_coordinaciones WHERE clv_zona = {clv_zona}) AS t1 USING UNIQUE gid USING SRID=900913"
    METADATA
        "wms_title" "CZ {nombre}"
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
    f.write("# ARCHIVO GENERADO AUTOMÁTICAMENTE: Coordinaciones de Zona IVEA \n")
    f.write("# Filtra la tabla mun_coordinaciones por clave de la CZ \n")
    f.write("# =================================================================\n\n")
    
    for cz in coordinaciones:
        
        # Reemplazamos los valores en la plantilla
        layer_renderizado = plantilla_layer.format(
            nombre=cz['nombre'],
            id_capa=cz['id'],
            clv_zona= cz['clv_zona'],
            color_rgb=cz['color']
        )
        
        f.write(layer_renderizado)

print("¡Archivo generado con éxito!")
