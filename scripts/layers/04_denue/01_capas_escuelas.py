descripcion = "Escuelas primarias en el estado de Veracruz"
output = "denue_escuelas"

tipo_capa = "POINT"

# CONFIGURACIONES GLOBALES
layer = {
    'type' : 'POINT',
    'labelitem': 'nombre_ue',
    'class' : {
        'style': {
            'symbol': 'circulor',
            'size': 9,
            'outlinecolor': '0,0,0'
        }
    }
}

capas_denue =  [
    {'id_capa': 'denue_escuelas_primarias','tabla':'denue.escuelas_primarias', "nombre": "Escuelas primarias", 'color': '11 123 234'},
    {'id_capa': 'denue_escuelas_secundarias','tabla':'denue.escuelas_secundarias', "nombre": "Escuelas secundarias", 'color': '122 234 10'},
    {'id_capa': 'denue_escuelas_media_superior','tabla':'denue.escuelas_media_superior', "nombre": "Escuelas media superior", 'color': '234 10 122'},
]

layers = []
for c in capas_denue:
    layers.append({
        'name':f"{c['id_capa']}",
        "metadata": {
            "wms_title": f"{c['nombre']} (DENUE 2026)",
        },
        'data': {
            'table': f"{c['tabla']}"
        },
        "class" : {
            "style": {
                "color": f"{c['color']}",
            }
        }
    })
