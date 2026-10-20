descripcion = "Lenguas indigenas por municipio"
output = "lengua_indigena_mun"

# CONFIGURACIONES GLOBALES
layer = {
    'type': 'POLYGON',
    'name': output,
    'metadata': {
        'wms_title': descripcion,
    },
    'data': {
        'table': 'marco_geoestadistico.mun_ver'
    },
    "labelitem": 'lengua',
    'class':{
        'style': {
            'outlinecolor' : '0,0,0',
            'width':'1',
            "color": "255,51,34",
        }
    }
}
