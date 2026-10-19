# Mapa tematico de pobreza
descripcion="Mapa tematico de pobreza"
output= 'tematico_pobreza'

pobreza = [
  {
    "name": "bajo/bajo",
    "color": "244 142 95"
  },
  {
    "name": "bajo/medio",
    "color": "186 116 56"
  },
  {
    "name": "bajo/alto",
    "color": "214 110 27"
  },
  {
    "name": "medio/medio",
    "color": "196 75 68"
  },
  {
    "name": "medio/alto",
    "color": "237 21 21"
  },
  {
    "name": "alto/medio",
    "color": "139 79 37"
  }
]

style_base =  {
    'outlinecolor': '0,0,0',
    "width" : 0.8,
    "opacity" : 60,
}

tabla = 'coneval.indice_pobreza'
clases = []

for mapa in pobreza:
    clases.append({
        'name': mapa['name'],
        "expression": f'{mapa['name']}',
        "style": style_base |
        {
            "color":mapa['color'],
            "outlinecolor":mapa['color'],
        },
        "label": {
            "font": "arial",
            "size": "8",
            "color": "0 0 0",
            "outlinecolor": "255 255 255",
            "position": "auto",
            "type": "truetype"
        }
    })
layer = {
    "name":"tematico_pobreza",
    "data": {
        "table": tabla,
        "select":['porcentaje'],
    },
    'classitem': 'porcentaje',
    'labelitem': 'porcentaje',
    "class":clases
}   