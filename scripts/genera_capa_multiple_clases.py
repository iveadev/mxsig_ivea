import os
import importlib
import sys

if len(sys.argv) < 2:
    print("Uso: python genera_capa_multiclase.py archivo_configuracion.py")
    sys.exit(1)

nombre_modulo = sys.argv[1]

# Limpieza de nombre de módulo
if nombre_modulo.endswith(".py"): nombre_modulo = nombre_modulo[:-3]
if nombre_modulo.startswith("./"): nombre_modulo = nombre_modulo[2:]
if nombre_modulo.startswith(".\\"): nombre_modulo = nombre_modulo[2:]
nombre_modulo = nombre_modulo.replace("/", ".").replace("\\", ".")
if nombre_modulo.startswith("scripts."): nombre_modulo = nombre_modulo[len("scripts."):]

try:
    capa = importlib.import_module(nombre_modulo)
    archivo_salida = getattr(capa, 'output', None)

    plantilla_cabecera_layer = """
LAYER
  NAME "{id_capa}"
  STATUS ON
  TYPE POLYGON
  CONNECTIONTYPE POSTGIS
  CONNECTION "host=mxsig-db port=5432 dbname=mdm6data user=postgres password=P0stgr3s"
  DATA "the_geom FROM (SELECT gid, the_geom{campos_adicionales} FROM {tabla}) AS t1 USING UNIQUE gid USING SRID=900913"

  METADATA
    "wms_title" "{wms_title}"
    "wms_enable_request" "*"
  END
"""

    plantilla_class = """
  CLASS
    NAME "{nombre_clase}"
    EXPRESSION ({expresion})
    STYLE
      {color}
      {opacity}
      {outlinecolor}
      {linewidth}
    END
  END
  
"""

    print(f"Generando archivo {archivo_salida}...")

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("# =================================================================\n")
        f.write(f"# ARCHIVO GENERADO AUTOMÁTICAMENTE (MULTICLASE) A PARTIR DE: {nombre_modulo} \n")
        f.write(f"# {capa.descripcion} \n")
        f.write("# =================================================================\n\n")
        
        # Escribimos la cabecera única del LAYER
        id_capa_activa = getattr(capa, 'id_capa', 'capa_tematica_unica')
        campos_add = f", {', '.join(getattr(capa, 'campos_adicionales', []))}" if hasattr(capa, 'campos_adicionales') else ""
        
        f.write(plantilla_cabecera_layer.format(
            id_capa=id_capa_activa,
            wms_title=getattr(capa, 'wms_title_global', 'Capa Tematica'),
            tabla=capa.tabla,
            campos_adicionales=campos_add
        ))
        
        # Bucle para inyectar cada uno de los estilos (CLASS)
        for clase in getattr(capa, 'clases', []):
            # Formateo de los estilos individuales o globales
            color_str = f"COLOR {clase['color']}" if 'color' in clase else f"COLOR {capa.color}" if hasattr(capa, 'color') else ""
            opacity_str = f"OPACITY {clase['opacity']}" if 'opacity' in clase else f"OPACITY {capa.opacity}" if hasattr(capa, 'opacity') else ""
            outline_str = f"OUTLINECOLOR {clase['outlinecolor']}" if 'outlinecolor' in clase else f"OUTLINECOLOR {capa.outlinecolor}" if hasattr(capa, 'outlinecolor') else ""
            width_str = f"WIDTH {clase['linewidth']}" if 'linewidth' in clase else f"WIDTH {capa.linewidth}" if hasattr(capa, 'linewidth') else ""
            
            # Ajuste de expresión: si viene texto o número en la condición sql
            expresion = clase['condicional']
            
            class_renderizado = plantilla_class.format(
                nombre_clase=clase['nombre'],
                expresion=expresion,
                color=color_str,
                opacity=opacity_str,
                outlinecolor=outline_str,
                linewidth=width_str
            )
            f.write(class_renderizado)
            
        # Al terminar las clases, cerramos el bloque LAYER
        f.write("\nEND # Fin del LAYER\n")

    print("¡Archivo generado con éxito!")
    print(f"\nURL para probar en el navegador:\nhttp://mdm.ivea.local/cgi-bin/mapserv?map=/opt/map/mdm60/mdm61vectormxsig.map&LAYERS={id_capa_activa}&FORMAT=image%2Fpng&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A900913&BBOX=-11586010,1662671,-9926410,2754804&WIDTH=1357&HEIGHT=893\n")

except ModuleNotFoundError:
    print(f"Error: No se encontró el módulo '{nombre_modulo}'.")
