descripcion = "Regiones económicas del PVD (tematico)"
output = "mun_regiones_pvd"

# CONFIGURACIONES GLOBALES
regiones = [
  { "region": "Huasteca Alta","color": "224,195,121" },
  { "region": "Huasteca Baja","color": "236,178,195" },
  { "region": "Totonaca","color": "173,137,122" },
  { "region": "Nautla","color": "165,148,199" },
  { "region": "Capital","color": "146,185,143" },
  { "region": "Las Montañas","color": "236,178,195" },
  { "region": "Sotavento","color": "165,148,199" },
  { "region": "Papaloapan","color": "173,137,122" },
  { "region": "Los Tuxtlas","color": "236,178,195" },
  { "region": "Olmeca","color": "146,185,143" }
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
        'table': 'marco_geoestadistico.regiones_pvd',
        'select': ['region_pvd']
    },
    "labelitem": 'region_pvd',
    "classitem": 'region_pvd',
    'class':classes
}
