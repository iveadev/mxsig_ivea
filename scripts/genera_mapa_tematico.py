import os
import importlib
import sys

if len(sys.argv) < 2:
    print("Uso: python genera_mapa_tematico.py archivo_configuracion.py")
    sys.exit(1)

nombre_modulo = sys.argv[1]

#Para poder importar el módulo es necesario limpar la ruta del archivo y convertirla en un nombre de módulo válido
if nombre_modulo.endswith(".py"):
  nombre_modulo = nombre_modulo[:-3]
if nombre_modulo.startswith("./"):
  nombre_modulo = nombre_modulo[2:]
if nombre_modulo.startswith(".\\"):
  nombre_modulo = nombre_modulo[2:]
#Reemplazar las barras "/" por puntos "."
nombre_modulo = nombre_modulo.replace("/", ".")
#Reemplazar las barras "/" por puntos "."
nombre_modulo = nombre_modulo.replace("\\", ".")
if nombre_modulo.startswith("scripts."):
  nombre_modulo = nombre_modulo[len("scripts."):]

try:
  # Importar el módulo dinámicamente
  mapa = importlib.import_module(nombre_modulo)

  # Configuración de salida
  archivo_salida = getattr(mapa, 'output', None)

  # Plantilla base para cada una de las capas con la sintaxis de subconsulta SQL en la sección DATA
  plantilla_layer = """
# Capa: {nombre}
LAYER
  NAME "{id_capa}"
  STATUS ON
  TYPE POLYGON
  CONNECTIONTYPE POSTGIS
  CONNECTION "host=mxsig-db port=5432 dbname=mdm6data user=postgres password=P0stgr3s"
  DATA "the_geom FROM (SELECT gid, the_geom{campos_adicionales} FROM {tabla} {condicional}) AS t1 USING UNIQUE gid USING SRID=900913"

  METADATA
    "wms_title" "{nombre}"
    "wms_enable_request" "*"
  END

  CLASS
    NAME "{nombre}"
    STYLE
      {color}
      {opacity}
      {outlinecolor}
      {linewidth}
    END
  END
END
  """  
  print(f"Generando archivo {archivo_salida}...")

  capas_generadas = ""

  with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write("# =================================================================\n")
    f.write(f"# ARCHIVO GENERADO AUTOMÁTICAMENTE A PARTIR DE LA DEFINICIÓN: {nombre_modulo} \n")
    f.write(f"# {mapa.descripcion} \n")
    f.write("# =================================================================\n\n")
      
    for capa in getattr(mapa, 'capas', []):
      # Reemplazamos los valores en la plantilla
      layer_renderizado = plantilla_layer.format(
        tabla=mapa.tabla,
        campos_adicionales= f", {', '.join(getattr(mapa, 'campos_adicionales', []))}" if hasattr(mapa, 'campos_adicionales') else "", #campos adicionales a seleccionar en la subconsulta SQL, si es que esta definido
        id_capa=capa['id_capa'],
        nombre=capa['nombre'],
        condicional= f"WHERE {capa['condicional']}" if 'condicional' in capa else "", #condición SQL para filtrar la capa, si es que esta definida

        #Bloque correspondiente al STYLE de la capa:
        # si no se define en la capa se toma el valor global del mapa, si no se define en el mapa se omite
        color=f"COLOR {capa['color']}" if 'color' in capa else f"COLOR {mapa.color}" if hasattr(mapa, 'color') else "", #color de la capa en formato R G B
        opacity=f"OPACITY {capa['opacity']}" if 'opacity' in capa else f"OPACITY {mapa.opacity}" if hasattr(mapa, 'opacity') else "", #opacidad de la capa
        outlinecolor=f"OUTLINECOLOR {capa['outlinecolor']}" if 'outlinecolor' in capa else f"OUTLINECOLOR {mapa.outlinecolor}" if hasattr(mapa, 'outlinecolor') else "", #color del contorno de la capa en formato R G B
        linewidth=f"WIDTH {capa['linewidth']}" if 'linewidth' in capa else f"WIDTH {mapa.linewidth}" if hasattr(mapa, 'linewidth') else "" #grosor del contorno de la capa
      )
      # Agregamos la capa generada al archivo de salida
      f.write(layer_renderizado)
      # Agregamos la capa generada a la lista de capas generadas
      capas_generadas += f"{capa['id_capa']}, "

  print("¡Archivo generado con éxito!")
  # Quitamos la última coma y espacio; reemplazamos las comas por %2C para que se pueda usar en la URL de MapServer
  print(f"Capas generadas:\nhttp://mdm.ivea.local/cgi-bin/mapserv?map=/opt/map/mdm60/mdm61vectormxsig.map&LAYERS={capas_generadas[:-2].replace(', ', '%2C')}&FORMAT=image%2Fpng&MAXRESOLUTION=4891.969809375&MINZOOMLEVEL=5&ZOOMOFFSET=5&TATO=0&LAYERNAME=&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FIRM=469&SRS=EPSG%3A900913&BBOX=-11586010.97117,1662671.8323836,-9926410.2133399,2754804.0923266&WIDTH=1357&HEIGHT=893\n")

except ModuleNotFoundError:
  print(f"Error: No se encontró el módulo '{nombre_modulo}'.")
  print("El script debe ser ejecutado desde la carpeta raíz del proyecto para que se genere el archivo correctamente.")
