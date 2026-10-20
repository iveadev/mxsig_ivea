descripcion = "Grado de marginacion y rezago social por municipio (tematico)"
output = "marginacion_rezago_social_por_mun"

# CONFIGURACIONES GLOBALES
escalas = [
  {
    "grado": "Muy bajo",
    "color": "39,174,96"
  },
  {
    "grado": "Bajo",
    "color": "162,217,104"
  },
  {
    "grado": "Medio",
    "color": "241,196,15"
  },
  {
    "grado": "Alto",
    "color": "230,126,34"
  },
  {
    "grado": "Muy alto",
    "color": "231,76,60"
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


for escala in escalas:
    classes.append({
        'name': escala['grado'],
        'expression': escala['grado'],
        'style': {
            'outlinecolor' : '0,0,0',
            'width':'1',
            "color": escala['color'],
            'opacity':60,
        },
        "label" : label_base
    })


layer = { 
  'type': 'POLYGON',
  'data': {
      'table': 'marco_geoestadistico.mun_ver',
      "select": []
  }
}

layers =[
  {
    "name": 'grado_marginacion',
    'metadata': {
          'wms_title': 'Grado de marginacion por municipio',
      },

    "labelitem": 'grado_marginacion',
    "classitem": 'grado_marginacion',
    'class':classes
  },
  { 
      "name": 'grado_rezago_social',
      'metadata': {
            'wms_title': 'rezago social por municipio',
        },
  
      "labelitem": 'grado_rezago_social',
      "classitem": 'grado_rezago_social',
      'class':classes
    }
]
