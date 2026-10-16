import sys
import os
import importlib.util

def cargar_definicion_externa(ruta_archivo):
    """Carga dinámicamente el archivo de configuración externa del usuario."""
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo de definición '{ruta_archivo}' no existe.")
        sys.exit(1)
        
    nombre_modulo = os.path.splitext(os.path.basename(ruta_archivo))[0]
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

# =====================================================================
# BLOQUES MODULARES DE LÓGICA (Funciones Atómicas)
# =====================================================================

def crear_bloque_metadata(titulo_wms):
    """Genera los metadatos obligatorios para el árbol de capas de MxSIG."""
    return [
        "  METADATA",
        f'    "wms_title" "{titulo_wms}"',
        '    "wms_enable_request" "*"',
        "  END"
    ]

def crear_bloque_style(datos_fila, config):
    """Genera la simbología aplicando prioridad: Valor Local > Valor Global."""
    tipo = getattr(config, "tipo_capa", "POLYGON").upper()
    color = datos_fila.get("color", "200 200 200")
    bloque = ["    STYLE", f"      COLOR {color}"]
    
    if tipo in ["POLYGON", "LINE"]:
        opacity = datos_fila.get("opacity", getattr(config, "opacity_global", None))
        outlinecolor = datos_fila.get("outlinecolor", getattr(config, "outlinecolor_global", None))
        width = datos_fila.get("width", getattr(config, "width_global", None))
        
        if opacity is not None: bloque.append(f"      OPACITY {opacity}")
        if outlinecolor is not None: bloque.append(f"      OUTLINECOLOR {outlinecolor}")
        if width is not None: bloque.append(f"      WIDTH {width}")
        
    elif tipo == "POINT":
        symbol = datos_fila.get("symbol", getattr(config, "symbol_global", "circlor"))
        size = datos_fila.get("size", getattr(config, "size_global", 8))
        outlinecolor = datos_fila.get("outlinecolor", getattr(config, "outlinecolor_global", None))
        
        bloque.append(f"      SYMBOL '{symbol}'")
        bloque.append(f"      SIZE {size}")
        if outlinecolor is not None: bloque.append(f"      OUTLINECOLOR {outlinecolor}")

    bloque.append("    END")
    return bloque

def crear_bloque_class(datos_fila, config, usar_expresion=False):
    """Construye la clase geométrica base."""
    nombre_clase = datos_fila.get("nombre", "Sin Nombre")
    bloque = ["  CLASS", f'    NAME "{nombre_clase}"']
    
    if usar_expresion and "condicional" in datos_fila:
        bloque.append(f"    EXPRESSION ({datos_fila['condicional']})")
        
    bloque.extend(crear_bloque_style(datos_fila, config))
    bloque.append("  END")
    return bloque

def crear_bloque_label(config_labels):
    """Genera la sección LABEL conteniendo un sub-bloque STYLE interno (Label-Style) para MapServer 7.6.4."""
    font = config_labels.get("font", "arial")
    size = config_labels.get("size", 8)
    color = config_labels.get("color", "0 0 0")
    outlinecolor = config_labels.get("outlinecolor", "255 255 255")
    position = config_labels.get("position", "auto")
    
    return [
        "    LABEL",
        f"      FONT '{font}'",
        f"      SIZE {size}",
        f"      COLOR {color}",
        f"      OUTLINECOLOR {outlinecolor}",
        f"      POSITION {position}",
        "      TYPE truetype",
        #"      STYLE",
        #"      END",
        "    END"
    ]

def crear_bloque_class_etiqueta(datos_fila, config_labels, usar_expresion=False):
    """Construye la clase para LEYENDAS (Cumple con: no class->styles)."""
    nombre_clase = datos_fila.get("nombre", "Sin Nombre")
    bloque = ["  CLASS", f'    NAME "Texto {nombre_clase}"']
    
    if usar_expresion and "condicional" in datos_fila:
        bloque.append(f"    EXPRESSION ({datos_fila['condicional']})")
        
    # Agrega el bloque LABEL (que ahora tiene su STYLE interno reglamentario)
    bloque.extend(crear_bloque_label(config_labels))
    bloque.append("  END")
    return bloque



def construir_layer_base(id_capa, tipo_capa, select_sql, encoding_capa=None):
    """Construye las cabeceras genéricas del LAYER de MapServer."""
    conexion_base = "host=mxsig-db port=5432 dbname=mdm6data user=postgres password=P0stgr3s"
    bloque = [
        "LAYER",
        f'  NAME "{id_capa}"',
        "  STATUS ON",
        f"  TYPE {tipo_capa}",
        "  CONNECTIONTYPE POSTGIS",
        f'  CONNECTION "{conexion_base}"',
        f'  DATA "{select_sql}"'
    ]
    if encoding_capa:
        bloque.append(f'  ENCODING "{encoding_capa}"')
    return bloque

# =====================================================================
# ORQUESTADOR PRINCIPAL
# =====================================================================

def main():
    if len(sys.argv) < 2:
        print("Uso correcto: python genera_layers.py <archivo_definicion.py>")
        sys.exit(1)
        
    archivo_config = sys.argv[1]
    cfg = cargar_definicion_externa(archivo_config)

    carpeta_base = getattr(cfg, "carpeta_base", "ivea/")
    subfolder_geometria = 'poligonos/' if cfg.tipo_capa == 'POLYGON' else 'puntos/'
    
    # NUEVA ESTRUCTURA REQUERIDA POR MXSIG (Espejo Vector vs Leyendas)
    ruta_vector = os.path.join(carpeta_base, subfolder_geometria)
    ruta_leyendas = os.path.join(carpeta_base, "leyendas")
    
    # Crear carpetas si no existen
    os.makedirs(ruta_vector, exist_ok=True)
    
    nombre_salida_vector = os.path.join(ruta_vector, f"{cfg.output}.map")
    nombre_salida_leyendas = os.path.join(ruta_leyendas, f"{cfg.output}.map")

    encoding_actual = getattr(cfg, "encoding_global", None)

    # -----------------------------------------------------------------
    # PROCESAMIENTO A: ARQUITECTURA VECTORIAL (mxsigvector)
    # -----------------------------------------------------------------
    lineas_geo = [
        f"# {cfg.output}.map - CAPAS GEOMETRICAS BASE (mxsigvector)",
        "#" + "="*70,
        f"# GENERADO AUTOMÁTICAMENTE A PARTIR DE: {archivo_config}",
        f"# Descripción: {cfg.descripcion}",
        f"# Modo de Operación: {cfg.modo_generacion}",
        "#" + "="*70 + "\n"
    ]

    if cfg.modo_generacion == "MULTIPLES_CAPAS":
        for c in cfg.capas:
            campos_adicionales = c['campos_adicionales'] if 'campos_adicionales' in c else getattr(cfg, 'campos_adicionales', [])
            campos_select = ", ".join(["gid", "the_geom"] + campos_adicionales)
            tabla = f"{c['tabla']}" if 'tabla' in c else cfg.tabla_global
            where = f" WHERE {c['condicional']}" if 'condicional' in c else ""
            sql = f"the_geom FROM (SELECT {campos_select} FROM {tabla}{where}) AS t1 USING UNIQUE gid USING SRID=900913"
            lineas_geo.extend(construir_layer_base('c_' + c["id_capa"], cfg.tipo_capa, sql, encoding_actual))
            lineas_geo.extend(crear_bloque_metadata(c["nombre"]))
            lineas_geo.extend(crear_bloque_class(c, cfg, usar_expresion=False))
            lineas_geo.append("END\n")

    elif cfg.modo_generacion == "MULTIPLES_ESTILOS":
        id_global = getattr(cfg, "id_capa_global", cfg.output)
        campos_adicionales = c['campos_adicionales'] if 'campos_adicionales' in c else getattr(cfg, 'campos_adicionales', [])
        campos_select = ", ".join(["gid", "the_geom"] + campos_adicionales)
        sql = f"the_geom FROM (SELECT {campos_select} FROM {cfg.tabla}) AS t1 USING UNIQUE gid USING SRID=900913"
        lineas_geo.extend(construir_layer_base('c_' + id_global, cfg.tipo_capa, sql, encoding_actual))
        lineas_geo.extend(crear_bloque_metadata(cfg.descripcion))
        for c in cfg.capas:
            lineas_geo.extend(crear_bloque_class(c, cfg, usar_expresion=True))
        lineas_geo.append("END\n")

    with open(nombre_salida_vector, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_geo))
    print(f" Capa vectorial guardada en: {nombre_salida_vector}")



    # -----------------------------------------------------------------
    # PROCESAMIENTO B: ARQUITECTURA DE ETIQUETAS (mxsigleyendas)
    # -----------------------------------------------------------------
    config_labels = getattr(cfg, "config_etiquetas", None)
    if config_labels:
        os.makedirs(ruta_leyendas, exist_ok=True)
        lineas_labels = [
            f"# {cfg.output}.map - CAPAS DE LEYENDAS / TEXTOS (mxsigleyendas)",
            "#" + "="*70,
            f"# GENERADO AUTOMÁTICAMENTE PARA MXSIG",
            "#" + "="*70 + "\n"
        ]
        label_item = config_labels["label_item"]

    
        if cfg.modo_generacion == "MULTIPLES_CAPAS":
            for c in cfg.capas:
                campos_adicionales = c['campos_adicionales'] if 'campos_adicionales' in c else getattr(cfg, 'campos_adicionales', [])
                campos_con_label = ["gid", "the_geom"] + campos_adicionales + [label_item]
                campos_select_labels = ", ".join(campos_con_label)
                tabla = f"{c['tabla']}" if 'tabla' in c else cfg.tabla_global
                where = f" WHERE {c['condicional']}" if 'condicional' in c else ""
                # Usamos campos_select_labels en lugar de campos_select tradicional
                sql = f"the_geom FROM (SELECT {campos_select_labels} FROM {tabla}{where}) AS t1 USING UNIQUE gid USING SRID=900913"
                
                lineas_labels.extend(construir_layer_base('t_' + c["id_capa"], cfg.tipo_capa, sql, encoding_actual))
                lineas_labels.extend(crear_bloque_metadata(f"Texto {c['nombre']}"))
                lineas_labels.append(f'  LABELITEM "{label_item}"')
                lineas_labels.extend(crear_bloque_class_etiqueta(c, config_labels, usar_expresion=False))
                lineas_labels.append("END\n")


        elif cfg.modo_generacion == "MULTIPLES_ESTILOS":
            id_global = getattr(cfg, "id_capa_global", cfg.output)
            # Usamos campos_select_labels aquí también
            sql = f"the_geom FROM (SELECT {campos_select_labels} FROM {cfg.tabla}) AS t1 USING UNIQUE gid USING SRID=900913"
            
            lineas_labels.extend(construir_layer_base(id_global, cfg.tipo_capa, sql, encoding_actual))
            lineas_labels.extend(crear_bloque_metadata(f"Etiquetas - {cfg.descripcion}"))
            lineas_labels.append(f'  LABELITEM "{label_item}"')
            for c in cfg.capas:
                lineas_labels.extend(crear_bloque_class_etiqueta(c, config_labels, usar_expresion=True))
            lineas_labels.append("END\n")
            


        with open(nombre_salida_leyendas, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas_labels))
        print(f" Capa de leyendas guardada en: {nombre_salida_leyendas}")

if __name__ == "__main__":
    main()
