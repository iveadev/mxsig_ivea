descripcion = "Marco Geoestadistico del Estado de Veracruz"
output = "marco_geoestadistico_ver"

# CONFIGURACIONES GLOBALES
layer = {
    'type': 'POLYGON',
    'class': [
        {
            'outlinecolor' : '0,0,0',
            'width':'1',
            'color':'0,0,0',
        }
    ]
}

# capas
layers =  [
    {
        'name': 'edo_ver',
        'metadata': {
            'wms_title': 'Contorno del Estado de Veracruz',
        },
        'data': {
            'table': 'marco_geoestadistico.entidad_ver'
        },
    },
    {
        'name': 'mun_ver',
        'metadata': {
            'wms_title': 'Municipios del Estado de Veracruz',
        },
        'data': {
            'table': 'marco_geoestadistico.mun_ver',
            #'select':['nomb_ent'],
            #'where': 'nomb_ent = "Veracruz de Ignacio de la Llave"'
        },
        'labelitem': 'nomgeo',
        'class': [
            {
                'style': {
                    'outline': '122,234,10',
                },
            }
        ]
    },
]
