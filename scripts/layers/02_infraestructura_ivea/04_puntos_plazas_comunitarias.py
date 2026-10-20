descripcion = "Ubicacion de las plazas comunitarias"
output = "plazas_comunitarias"

# CONFIGURACIONES GLOBALES
layer = {
    'type': 'POINT',
    'name': 'plazas_comunitarias',
    'metadata': {
        'wms_title': descripcion,
    },
    'labelitem':'nombre_plaza',
    'data': {
        'table': 'ivea.plazas_comunitarias'
    },
    'class':{
        'style': {
            "symbol" : "circulor",
            "size": "9",
            "outlinecolor": "0,0,0",
        }
    }
}
