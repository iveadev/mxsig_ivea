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

# 1. Definición de la escala de Grises para los Clústeres (> 1 punto)
gris_bajo  = "180 180 180"
gris_medio = "120 120 120"
gris_alto  = "70 70 70"

# 2. Definición del Esquema Semáforo para Puntos Individuales (== 1 punto)
semaforo_verde    = "42 212 48"
semaforo_amarillo = "253 141 60"
semaforo_rojo     = "227 26 28"

# 3. Umbrales de población/densidad para la variable 'campo'
limite_bajo_medio = 10
limite_medio_alto = 50

# 4. Diccionario base para las etiquetas de los clústeres
# Tu generador traducirá este bloque como "LABEL ... END" dentro de cada CLASS de clúster
label_cluster_base = {
    "text": f"[{cluster_count}]",   # Indica a MapServer que pinte el conteo del grupo
    "font": "sans",                 # Asegúrate de tener esta fuente mapeada en tu FONTSET
    "type": "truetype",
    "size": 9,
    "align": "center",
    "position": "cc"                # Centrado horizontal y verticalmente en el círculo
}

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
            # PUNTOS INDIVIDUALES (Sin bloque 'label' para que queden limpios)
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
            # CLÚSTERES (Con bloque 'label' inyectado dinámicamente)
            # =========================================================================
            style_base | {
                "name": "Grupo Pequeño (2-49)",
                "color": gris_bajo,
                'outlinecolor': "220 220 220",
                'size': 14,
                'expression': f'[{cluster_count}] > 1 AND [{cluster_count}] < 50',
                # Inyección del Label (texto negro para contraste con fondo claro)
                'label': label_cluster_base | {"color": "0 0 0", "size": 8}
            },
            style_base | {
                "name": "Grupo Medio (50-499)",
                "color": gris_medio,
                'outlinecolor': "180 180 180",
                'size': 22,
                'expression': f'[{cluster_count}] >= 50 AND [{cluster_count}] < 500',
                # Inyección del Label (texto blanco para contraste con fondo medio)
                'label': label_cluster_base | {"color": "255 255 255", "size": 9}
            },
            style_base | {
                "name": "Grupo Grande (>=500)",
                "color": gris_alto,
                'outlinecolor': "120 120 120",
                'size': 32,
                'expression': f'[{cluster_count}] >= 500',
                # Inyección del Label (texto blanco y más grande)
                'label': label_cluster_base | {"color": "255 255 255", "size": 11}
            }
        ],
        "_tree": {
            "grupo": "rezago_educativo_censo",
        },
    })
