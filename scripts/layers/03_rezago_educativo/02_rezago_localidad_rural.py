import colorsys
import sys
import os

sys.path.append(os.getcwd())
#from scripts.utils.postgres import obtener_cuartiles_desde_postgres

#==========================================================================
# Definición de la capa
#==========================================================================

descripcion = "Localidades rurales con rezago educativo Censo 2020"
output = "rezago_localidades_rurales"
cluster_count = "Cluster_FeatureCount"


# CONFIGURACIONES GLOBALES
tabla = "rezago_educativo_censo_2020.rez_loc_rur"

layer = {
    'type' : 'POINT',
    "data": {
        'table': tabla,
    },
    "processing":"CLOSE_CONNECTION=DEFER",
}

campos = [
    'analfabetas',
    'sin_primaria',
    'sin_secundaria',
    'rezago_total',
]

wms_titles = [
    'en Rezago Educativo',
    'en condición de analfabetizmo',
    'sin primaria terminada',
    'sin secundaria terminada'    
]

colores = [
    '42,212,48',  #verde
    '194,35,194', #fuscia
    '18,67,227',  #azul
    '245,90,7',   #naranja
]

style_base =  {
    "symbol": 'circulor',
    "size": 10,
    "outlinecolor": "0,0,0",
}


def intensificar_rgb(rgb_str, factor):
    # 1. Separar y normalizar a rango 0.0 - 1.0 para colorsys
    r, g, b = [int(x) / 255.0 for x in rgb_str.split(',')]
    
    # 2. Convertir RGB a HSL (Hue, Lightness, Saturation)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # 3. Modificar: Bajamos la luminosidad con el factor, pero forzamos saturación al máximo (1.0)
    # Esto hace que el color sea oscuro pero extremadamente "vivo" (no lodoso)
    l_nueva = max(0.12, min(1.0, l * factor))
    s_nueva = 1.0 if factor < 1.0 else s # Forzar viveza en los grupos oscuros
    
    # 4. Volver a convertir a RGB y escalar a 0-255
    r_n, g_n, b_n = colorsys.hls_to_rgb(h, l_nueva, s_nueva)
    nuevos_canales = [int(r_n * 255), int(g_n * 255), int(b_n * 255)]
    
    # Retornamos con comas (o espacios según lo procese tu script posterior)
    return ",".join(str(c) for c in nuevos_canales)


# 1. Definición de la escala de Grises para los Clústeres (> 1 punto)
gris_bajo  = "180 180 180"  # Gris claro para grupos pequeños
gris_medio = "120 120 120"  # Gris medio
gris_alto  = "70 70 70"     # Gris oscuro para grupos masivos

# 2. Definición del Esquema Semáforo para Puntos Individuales (== 1 punto)
semaforo_verde    = "42 212 48"   # Densidad Baja
semaforo_amarillo = "253 141 60"  # Densidad Media (Naranja/Amarillo brillante)
semaforo_rojo     = "227 26 28"   # Densidad Alta

# 3. Umbrales de población/densidad para la variable 'campo'
# Ajusta estos números según el comportamiento real de tus datos del censo
limite_bajo_medio = 10   # Menos de 10 personas -> Verde
limite_medio_alto = 50   # Entre 10 y 49 -> Amarillo. 50 o más -> Rojo.

layers = []
for i in range(4):
    campo = campos[i]
    
    layers.append({
        "name": campo,
        "data": {
            "select": [campo]
        },
        "labelitem": 'nomgeo',
        "metadata": {
            'wms_title': f"Número de personas {wms_titles[i]} por localidad rural"
        },
        'cluster': {
            'maxdistance': 25,
            'region': 'rectangle',
            'buffer': 0,
        },
        'classitem': cluster_count,
        "class": [
            # =========================================================================
            # PUNTOS INDIVIDUALES (Cluster_FeatureCount = 1) - Semáforo por Densidad
            # =========================================================================
            style_base | {
                "name": "Localidad - Rezago Bajo",
                "color": semaforo_verde,
                'outlinecolor': semaforo_verde,
                'size': 6,
                'expression': f'([{cluster_count}] = 1 AND [{campo}] < {limite_bajo_medio})'
            },
            style_base | {
                "name": "Localidad - Rezago Medio",
                "color": semaforo_amarillo,
                'outlinecolor': semaforo_amarillo,
                'size': 7,
                'expression': f'([{cluster_count}] = 1 AND [{campo}] >= {limite_bajo_medio} AND [{campo}] < {limite_medio_alto})'
            },
            style_base | {
                "name": "Localidad - Rezago Alto",
                "color": semaforo_rojo,
                'outlinecolor': semaforo_rojo,
                'size': 8,
                'expression': f'([{cluster_count}] = 1 AND [{campo}] >= {limite_medio_alto})'
            },
            
            # =========================================================================
            # CLÚSTERES (Cluster_FeatureCount > 1) - Escala de Grises Neutral
            # =========================================================================
            style_base | {
                "name": "Grupo Pequeño (2-49)",
                "color": gris_bajo,
                'outlinecolor': "220 220 220", # Borde claro para resaltar
                'size': 14,
                'expression': f'[{cluster_count}] > 1 AND [{cluster_count}] < 50'
            },
            style_base | {
                "name": "Grupo Medio (50-499)",
                "color": gris_medio,
                'outlinecolor': "180 180 180",
                'size': 22,
                'expression': f'[{cluster_count}] >= 50 AND [{cluster_count}] < 500'
            },
            style_base | {
                "name": "Grupo Grande (>=500)",
                "color": gris_alto,
                'outlinecolor': "120 120 120",
                'size': 32,
                'expression': f'[{cluster_count}] >= 500'
            }
        ],
        "_tree": {
            "grupo": "rezago_educativo_censo",
        },
    })
