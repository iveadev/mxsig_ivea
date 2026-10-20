descripcion = "Regiones económicas del PVD (tematico)"
output = "mun_regiones_pvd"

# CONFIGURACIONES GLOBALES
regiones = [
  {
    "region": "Papaloapan",
    "color": "185, 34, 35"
  },
  {
    "region": "Omealca",
    "color": "227, 72, 140"
  },
  {
    "region": "Nautla",
    "color": "148, 114, 189"
  },
  {
    "region": "Los Tuxtlas",
    "color": "181, 57, 59"
  },
  {
    "region": "Las Montañas",
    "color": "231, 102, 143"
  },
  {
    "region": "Huasteca Baja",
    "color": "244, 155, 172"
  },
  {
    "region": "Huasteca Alta",
    "color": "206, 169, 52"
  },
  {
    "region": "Capital",
    "color": "120, 174, 112"
  },
  {
    "region": "Totonaca",
    "color": "158, 77, 51"
  },
  {
    "region": "Sotavento",
    "color": "204, 38, 38"
  }
]

label_base = {
    "font": "arial",
    "size": "8",
    "color": "0 0 0",
    "outlinecolor": "255 255 255",
    'priority': 10,
    'buffer': 1,
    'position': 'uc',
    "type": "truetype"
}

classes = []


for region in regiones:
    classes.append({
        'name': region['region'],
        'expression': region['region'],
        'style': {
            'outlinecolor' : '0,0,0',
            'width':'1',
            "color": region['color'],
            'opacity':60,
        },
        "label" : label_base
    })
layer = {
    'type': 'POLYGON',
    'name': output,
    'metadata': {
        'wms_title': descripcion,
    },
    'data': {
        'table': 'marco_geoestadistico.mun_ver',
        'select': ['region_pvd']
    },
    #"labelitem": 'region_pvd',
    "classitem": 'region_pvd',
    'class':classes
}
