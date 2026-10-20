descripcion = "Lenguas indigenas por municipio (tematico)"
output = "lengua_indigena_mun"

# CONFIGURACIONES GLOBALES
lenguas = [
  {
    "lengua": "Otomí",
    "color": "242, 100, 87"
  },
  {
    "lengua": "Nahualt de la Huasteca",
    "color": "246, 134, 69"
  },
  {
    "lengua": "Popoluca",
    "color": "249, 178, 51"
  },
  {
    "lengua": "Nahua dePajapan",
    "color": "247, 219, 96"
  },
  {
    "lengua": "Huasteco",
    "color": "186, 216, 101"
  },
  {
    "lengua": "Nahua de Mecayapan",
    "color": "61, 131, 107"
  },
  {
    "lengua": "Náhuatl de la Sierra Negra de Zongolica",
    "color": "43, 114, 131"
  },
  {
    "lengua": "Nahua de Zaragoza",
    "color": "52, 94, 138"
  },
  {
    "lengua": "Tepehua",
    "color": "69, 81, 133"
  },
  {
    "lengua": "Totonaco",
    "color": "87, 75, 142"
  },
  {
    "lengua": "Lenguas zapotecas",
    "color": "124, 76, 138"
  },
  {
    "lengua": "Nahuatl",
    "color": "158, 79, 126"
  },
  {
    "lengua": "Lenguas chinantecas",
    "color": "173, 71, 109"
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


for lengua in lenguas:
    classes.append({
        'name': lengua['lengua'],
        'expression': lengua['lengua'],
        'style': {
            'outlinecolor' : '0,0,0',
            'width':'1',
            "color": lengua['color'],
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
        'where' "lengua != 'No"
        'select': ['lengua']
    },
    "labelitem": 'lengua',
    "classitem": 'lengua',
    'class':classes
}
