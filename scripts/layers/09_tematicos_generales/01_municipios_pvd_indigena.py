descripcion = "Municipios indigenas del Plan Veracruzano de Desarrollo"
output = "municipios_pvd_indigena"

# CONFIGURACIONES GLOBALES
layer = {
    'type': 'POLYGON',
    'name': 'municipios_indigenas_pvd',
    'metadata': {
        'wms_title': descripcion,
    },
    'data': {
        'table': 'mun_indigenas_pvd.mun_indigenas_pvd'
    },
    'class':{
        'style': {
            'outlinecolor' : '0,0,0',
            'width':'1',
            "color": "114,47,55",
        }
    }
}
