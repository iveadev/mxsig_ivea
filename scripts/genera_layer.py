import os
import sys
import importlib

if len(sys.argv) < 2:
    print("Uso: python genera_layers.py archivo_configuracion.py")
    sys.exit(1)

nombre_modulo = sys.argv[1].replace(".py", "").replace("/", ".").replace("\\", ".").replace("scripts.", "")

CARPETA_RAIZ = "ivea"

# Estructura e infraestructura base del contenedor de MxSIG
estructura_base = {
    "name": "Capa base",
    "status": "ON",
    "type": "POLYGON",
    "connectiontype": "POSTGIS",
    "connection": "host=mxsig-db port=5432 dbname=mdm6data user=postgres password=P0stgr3s",
    "data": {},
    "metadata": {
        "wms_title": "capa base",
        "wms_enable_request" : "*"
    },
    "labelitem": "", # Inicializado vacío; si el usuario lo define, detona el modo dual
    "class" : {
        "label": {
            "font": "arial",
            "size": "8",
            "color": "0 0 0",
            "outlinecolor": "255 255 255",
            "position": "auto",
            "type": "truetype"
        }
    }
    
}

requiere_doble_comillas = ["NAME", "WMS_TITLE", "WMS_ENABLE_REQUEST", "LABELITEM", "CONNECTION", "FONT"]

def deep_update(dicc_base, dicc_usuario):
    resultado = dicc_base.copy()
    for k, v in dicc_usuario.items():
        if k in resultado and isinstance(resultado[k], dict) and isinstance(v, dict):
            resultado[k] = deep_update(resultado[k], v)
        else:
            resultado[k] = v
    return resultado

def procesar_valor(clave, valor):
    clave = clave.upper()
    if clave in requiere_doble_comillas:   
        return f'"{valor}"'
    else:
        match clave:
            case "COLOR" | "OUTLINECOLOR":
                return str(valor).replace(",", " ").strip()
            case "EXPRESSION":
                return f"({valor})"
            case _:
                return str(valor)

def renderizar_diccionario(dicc, nivel=0):
    lineas = []
    espacio = "  " * nivel
    
    for k, v in dicc.items():
        clave_mapserver = k.strip().upper()

        if isinstance(v, dict):
            match clave_mapserver:
                case "METADATA":
                    lineas.append(f"{espacio}METADATA")
                    for mk, mv in v.items():
                        lineas.append(f'{espacio}  "{mk.strip().lower()}" "{mv}"')
                    lineas.append(f"{espacio}END")
                case "DATA":
                    campos_adicionales = v.get('select', [])
                    campos_select = ", ".join(["gid", "the_geom"] + campos_adicionales)
                    tabla = v['table']
                    where = f" WHERE {v['where']}" if 'where' in v else ""
                    sql = f"the_geom FROM (SELECT {campos_select} FROM {tabla}{where}) AS t1 USING UNIQUE gid USING SRID=900913"
                    lineas.append(f'{espacio}DATA "{sql}"')
                case _:
                    if not v: continue # Evita bloques vacíos
                    lineas.append(f"{espacio}{clave_mapserver}")
                    lineas.extend(renderizar_diccionario(v, nivel + 1))
                    lineas.append(f"{espacio}END")
                
        elif isinstance(v, list):
            for elemento in v:
                lineas.extend(renderizar_diccionario({clave_mapserver: elemento}, nivel))
        else:
            if str(v).strip() == "": continue
            valor_formateado = procesar_valor(clave_mapserver, v)
            lineas.append(f"{espacio}{clave_mapserver} {valor_formateado}")
            
    return lineas

# FUNCIÓN DE PODA ADAPTATIVA
def podar_diccionario(dicc, modo="BASE"):
    if not isinstance(dicc, dict): return dicc
    dicc_limpio = {}
    for k, v in dicc.items():
        clave_upper = k.strip().upper()
        
        if modo == "BASE" and clave_upper in ["LABELITEM", "LABEL"]: continue
        if modo == "TEXTO" and clave_upper == "STYLE": continue
        
        if isinstance(v, dict):
            dicc_limpio[k] = podar_diccionario(v, modo)
        elif isinstance(v, list):
            dicc_limpio[k] = [podar_diccionario(item, modo) for item in v]
        else:
            dicc_limpio[k] = v
    return dicc_limpio

try:
    mapa = importlib.import_module(nombre_modulo)
    config_global_final = deep_update(estructura_base, getattr(mapa, "layer", {}))
    
    # Determinamos el tipo de geometría para saber en qué subcarpeta guardar
    tipo_geom = config_global_final.get("type", "POLYGON").upper()
    subcarpeta = "poligonos" if "POLYGON" in tipo_geom else "puntos" if "POINT" in tipo_geom else "lineas"
    ruta_destino = os.path.join(CARPETA_RAIZ, subcarpeta)
    ruta_destino_labels = os.path.join(CARPETA_RAIZ, 'leyendas')
    os.makedirs(ruta_destino, exist_ok=True) # Crea las carpetas automáticamente si no existen
    
    prefix_output = getattr(mapa, 'output', 'salida_mxsig')
    archivo_base = os.path.join(ruta_destino, f"{prefix_output}.map")
    archivo_labels = os.path.join(ruta_destino_labels, f"{prefix_output}.map")
    
    contenido_base = []
    contenido_labels = []
    procesa_dual = False
    
    for ly in getattr(mapa, "layers", [config_global_final]):
        capa_completa = deep_update(config_global_final, ly)
        nombre_original = capa_completa.get("name", "capa")
        titulo_original = capa_completa.get("metadata", {}).get("wms_title", "Capa")
        
        # Evaluamos si el usuario definió un labelitem real para procesar el modo dual
        if capa_completa.get("labelitem", ""):
            procesa_dual = True

        # 1. PASADA MAPA BASE: Forzamos prefijo "c_" y podamos bloques LABEL
        capa_base = capa_completa.copy()
        capa_base["name"] = f"c_{nombre_original}"
        capa_base = podar_diccionario(capa_base, modo="BASE")
        contenido_base.extend(renderizar_diccionario({"LAYER": capa_base}))
        contenido_base.append("")
        
        # 2. PASADA TEXTOS: Forzamos prefijo "t_", "Texto..." en título y podamos STYLES
        if procesa_dual:
            capa_texto = deep_update(capa_completa, {
                "name": f"t_{nombre_original}",
                "metadata": {"wms_title": f"Texto {titulo_original}"}
            })

            capa_texto["data"]["select"] = capa_texto["data"].get("select", [])
            if capa_texto["labelitem"] not in capa_texto["data"]["select"]:
                capa_texto["data"]["select"].append(capa_texto["labelitem"])
            # # Modificamos el Name dentro del bloque CLASS interno para que diga "Texto..."
            # if "class" in capa_texto:
            #     for cl in capa_texto["class"]:
            #         cl["name"] = f"Texto {cl.get('name', titulo_original)}"
            
            capa_texto = podar_diccionario(capa_texto, modo="TEXTO")
            contenido_labels.extend(renderizar_diccionario({"LAYER": capa_texto}))
            contenido_labels.append("")

    # Guardamos los archivos en sus respectivas rutas estructuradas
    with open(archivo_base, "w", encoding="utf-8") as f:
        f.write("# =================================================================\n")
        f.write("# MAPA BASE DE GEOMETRÍAS\n")
        f.write(f"# ARCHIVO GENERADO AUTOMÁTICAMENTE A PARTIR DE LA DEFINICIÓN: {nombre_modulo} \n")
        f.write(f"# DESCRIPCIÓN: {mapa.descripcion} \n")
        f.write("# =================================================================\n\n")
        f.write("\n".join(contenido_base))
    print(f"Mapfile BASE generado con éxito en: '{archivo_base}'")

    if procesa_dual:
        with open(archivo_labels, "w", encoding="utf-8") as f:
            f.write("# =================================================================\n")
            f.write("# MAPA EXCLUSIVO DE TEXTOS (leyendas)\n")
            f.write(f"# ARCHIVO GENERADO AUTOMÁTICAMENTE A PARTIR DE LA DEFINICIÓN: {nombre_modulo} \n")
            f.write(f"# DESCRIPCIÓN: {mapa.descripcion} \n")
            f.write("# =================================================================\n\n")
            f.write("\n".join(contenido_labels))
        print(f"Mapfile LABELS generado con éxito en: '{archivo_labels}'")

except Exception as e:
    print(f"Error durante la compilación: {e}")
