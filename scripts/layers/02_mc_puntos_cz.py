# scripts/layers/02_mc_oficinas.py
descripcion = "Puntos de las Oficinas de Coordinacion IVEA"
output = "oficinas_cz"
tabla = "ivea.oficinas_cz"
campos_adicionales = ["clv_cz"]
tipo_capa = "POINT"
id_capa_global = "capa_oficinas_cz"

# RESPATE DE CARACTERES: Corrige los acentos rotos de la BD (como 'CRDOBA') al vuelo
encoding_global = "ISO-8859-1" 

# CONFIGURACIONES GLOBALES PARA PUNTOS
symbol_global = "circulor"
size_global = 9
outlinecolor_global = "0 0 0"

modo_generacion = "MULTIPLES_ESTILOS"

capas =  [
    {"id_capa": "cz3001_p",   "condicional": "[clv_cz] = 1",  "nombre": "Tantoyuca",       "color": "235 151 78"},
    {"id_capa": "cz3003_p",   "condicional": "[clv_cz] = 3",  "nombre": "Chicontepec",     "color": "93 188 210"},
    {"id_capa": "cz3004_p",   "condicional": "[clv_cz] = 4",  "nombre": "Tuxpan",          "color": "158 53 147"},
    {"id_capa": "cz3005_p",   "condicional": "[clv_cz] = 5",  "nombre": "Poza Rica",       "color": "196 46 96"},
    {"id_capa": "cz3006_p",   "condicional": "[clv_cz] = 6",  "nombre": "Papantla",        "color": "74 163 113"},
    {"id_capa": "cz3007_p",   "condicional": "[clv_cz] = 7",  "nombre": "Espinal",         "color": "249 220 101"},
    {"id_capa": "cz3008_p",   "condicional": "[clv_cz] = 8",  "nombre": "Martinez",        "color": "235 151 78"},
    {"id_capa": "cz3009_p",   "condicional": "[clv_cz] = 9",  "nombre": "Perote",          "color": "93 188 210"},
    {"id_capa": "cz3010_p",   "condicional": "[clv_cz] = 10", "nombre": "Xalapa",          "color": "158 53 147"},
    {"id_capa": "cz3011_p",   "condicional": "[clv_cz] = 11", "nombre": "Coatepec",        "color": "196 46 96"},
    {"id_capa": "cz3012_p",   "condicional": "[clv_cz] = 12", "nombre": "Huatusco",        "color": "74 163 113"},
    {"id_capa": "cz3013_p",   "condicional": "[clv_cz] = 13", "nombre": "Orizaba",         "color": "249 220 101"},
    {"id_capa": "cz3014_p",   "condicional": "[clv_cz] = 14", "nombre": "Cordoba",         "color": "235 151 78"},
    {"id_capa": "cz3015_p",   "condicional": "[clv_cz] = 15", "nombre": "Zongolica",       "color": "93 188 210"},
    {"id_capa": "cz3016_p",   "condicional": "[clv_cz] = 16", "nombre": "Veracruz",        "color": "158 53 147"},
    {"id_capa": "cz3017_p",   "condicional": "[clv_cz] = 17", "nombre": "Boca del Rio",    "color": "196 46 96"},
    {"id_capa": "cz3018_p",   "condicional": "[clv_cz] = 18", "nombre": "Tierra Blanca",   "color": "74 163 113"},
    {"id_capa": "cz3019_p",   "condicional": "[clv_cz] = 19", "nombre": "Cosamaloapan",    "color": "249 220 101"},
    {"id_capa": "cz3020_p",   "condicional": "[clv_cz] = 20", "nombre": "San Andres",      "color": "235 151 78"},
    {"id_capa": "cz3021_p",   "condicional": "[clv_cz] = 21", "nombre": "Acayucan",        "color": "93 188 210"},
    {"id_capa": "cz3022_p",   "condicional": "[clv_cz] = 22", "nombre": "Minatitlan",       "color": "158 53 147"},
    {"id_capa": "cz3023_p",   "condicional": "[clv_cz] = 23", "nombre": "Coatzacoalcos",   "color": "196 46 96"},
    {"id_capa": "cz3024_p",   "condicional": "[clv_cz] = 24", "nombre": "Huayacocotla",    "color": "74 163 113"},
    {"id_capa": "cz3025_p",   "condicional": "[clv_cz] = 25", "nombre": "Panuco",          "color": "249 220 101"},
    {"id_capa": "cz3029_p",   "condicional": "[clv_cz] = 29", "nombre": "Jaltipan",        "color": "235 151 78"},
]

# leyendas
config_etiquetas = {
    'label_item': 'nom_cz',
}