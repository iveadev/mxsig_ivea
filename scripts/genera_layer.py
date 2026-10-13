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
    
    # --- Configuración para POLÍGONOS o LÍNEAS ---
    if tipo in ["POLYGON", "LINE"]:
        opacity = datos_fila.get("opacity", getattr(config, "opacity_global", None))
        outlinecolor = datos_fila.get("outlinecolor", getattr(config, "outlinecolor_global", None))
        width = datos_fila.get("width", getattr(config, "width_global", None))
        
        if opacity is not None: bloque.append(f"      OPACITY {opacity}")
        if outlinecolor is not None: bloque.append(f"      OUTLINECOLOR {outlinecolor}")
        if width is not None: bloque.append(f"      WIDTH {width}")
        
    # --- Configuración específica para PUNTOS ---
    elif tipo == "POINT":
        symbol = datos_fila.get("symbol", getattr(config, "symbol_global", "circle"))
        size = datos_fila.get("size", getattr(config, "size_global", 8))
        outlinecolor = datos_fila.get("outlinecolor", getattr(config, "outlinecolor_global", None))
        
        bloque.append(f"      SYMBOL '{symbol}'")
        bloque.append(f"      SIZE {size}")
        if outlinecolor is not None: bloque.append(f"      OUTLINECOLOR {outlinecolor}")

    bloque.append("    END")
    return bloque

def crear_bloque_class(datos_fila, config, usar_expresion=False):
    """Construye la clase y decide si inyecta EXPRESSION (Modo Estilos)."""
    nombre_clase = datos_fila.get("nombre", "Sin Nombre")
    bloque = ["  CLASS", f'    NAME "{nombre_clase}"']
    
    if usar_expresion and "condicional" in datos_fila:
        bloque.append(f"    EXPRESSION ({datos_fila['condicional']})")
        
    bloque.extend(crear_bloque_style(datos_fila, config))
    bloque.append("  END")
    return bloque

def construir_layer_base(id_capa, tipo_capa, select_sql, encoding_capa=None):
    """Construye las cabeceras genéricas del LAYER e inyecta el ENCODING si existe."""
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
    
    # Aquí solucionamos el problema de caracteres rotos si el usuario lo activa
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

    lineas_resultado = [
        f"# {cfg.output}.map",
        "#" + "="*70,
        f"# GENERADO AUTOMÁTICAMENTE A PARTIR DE: {archivo_config}",
        f"# Descripción: {cfg.descripcion}",
        f"# Modo de Operación: {cfg.modo_generacion}",
        "#" + "="*70 + "\n"
    ]
    
    # Recorremos siempre usando 'the_geom' nativo de tus tablas de MxSIG
    campos_select = ", ".join(["gid", "the_geom"] + cfg.campos_adicionales)
    encoding_actual = getattr(cfg, "encoding_global", None)

    # --- MODO 1: MÚLTIPLES CAPAS ---
    if cfg.modo_generacion == "MULTIPLES_CAPAS":
        for c in cfg.capas:
            sql = f"the_geom FROM (SELECT {campos_select} FROM {cfg.tabla} WHERE {c['condicional']}) AS t1 USING UNIQUE gid USING SRID=900913"
            lineas_resultado.extend(construir_layer_base(c["id_capa"], cfg.tipo_capa, sql, encoding_actual))
            lineas_resultado.extend(crear_bloque_metadata(c["nombre"]))
            lineas_resultado.extend(crear_bloque_class(c, cfg, usar_expresion=False))
            lineas_resultado.append("END\n")

    # --- MODO 2: MÚLTIPLES ESTILOS ---
    elif cfg.modo_generacion == "MULTIPLES_ESTILOS":
        sql = f"the_geom FROM (SELECT {campos_select} FROM {cfg.tabla}) AS t1 USING UNIQUE gid USING SRID=900913"
        lineas_resultado.extend(construir_layer_base(cfg.output, cfg.tipo_capa, sql, encoding_actual))
        lineas_resultado.extend(crear_bloque_metadata(cfg.descripcion))
        for c in cfg.capas:
            lineas_resultado.extend(crear_bloque_class(c, cfg, usar_expresion=True))
        lineas_resultado.append("END\n")

    # Guardar archivo listo para el INCLUDE de MxSIG
    nombre_salida = f"{cfg.output}.map"
    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_resultado))
        
    print(f"¡Éxito! Archivo '{nombre_salida}' generado en modo '{cfg.modo_generacion}'.")

if __name__ == "__main__":
    main()
