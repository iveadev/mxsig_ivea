# Archivo de deficion para las capas de Coordinaciones de Zona del IVEA
descripcion =  "Coordinaciones de Zona del IVEA"
# Nombre del archivo de salida
output =  "ivea/coordinaciones.map"

# nombre de la tabla en la base de datos, comenzando con el esquema, por ejemplo: "esquema.tabla"
tabla =  "marco_geoestadistico.mun_coordinaciones"
#Campos adicionales a seleccionar en la subconsulta SQL
campos_adicionales = ["clv_zona"]

#Valores globales para las capas, si se definen aquí se aplicarán a todas las capas, si se definen en la capa se sobreescriben
opacity =  "60"
outlinecolor =  "60 60 60"
linewidth =  "0.8"

#Definición de las propiedades de las capas:
#   id_capa: Nombre de la capa generada en mapserver
#   condicional: Condición SQL para filtrar la capa
#   nombre: Nombre de la capa que se mostrará en el mapa
#   color: Color de la capa
#   opacity: Opacidad de la capa, si no está definido se omitirá en la capa
#   outlinecolor: Color del contorno de la capa, si no está definido se omitirá en la capa

capas =  [
    {"id_capa": "cz3001",   "condicional": "clv_zona = 1",  "nombre": "Tantoyuca",       "color": "235 151 78"},
    {"id_capa": "cz3003",   "condicional": "clv_zona = 3",  "nombre": "Chicontepec",     "color": "93 188 210"},
    {"id_capa": "cz3004",   "condicional": "clv_zona = 4",  "nombre": "Tuxpan",          "color": "158 53 147"},
    {"id_capa": "cz3005",   "condicional": "clv_zona = 5",  "nombre": "Poza Rica",       "color": "196 46 96"},
    {"id_capa": "cz3006",   "condicional": "clv_zona = 6",  "nombre": "Papantla",        "color": "74 163 113"},
    {"id_capa": "cz3007",   "condicional": "clv_zona = 7",  "nombre": "Espinal",         "color": "249 220 101"},
    {"id_capa": "cz3008",   "condicional": "clv_zona = 8",  "nombre": "Martinez",        "color": "235 151 78"},
    {"id_capa": "cz3009",   "condicional": "clv_zona = 9",  "nombre": "Perote",          "color": "93 188 210"},
    {"id_capa": "cz3010",   "condicional": "clv_zona = 10", "nombre": "Xalapa",          "color": "158 53 147"},
    {"id_capa": "cz3011",   "condicional": "clv_zona = 11", "nombre": "Coatepec",        "color": "196 46 96"},
    {"id_capa": "cz3012",   "condicional": "clv_zona = 12", "nombre": "Huatusco",        "color": "74 163 113"},
    {"id_capa": "cz3013",   "condicional": "clv_zona = 13", "nombre": "Orizaba",         "color": "249 220 101"},
    {"id_capa": "cz3014",   "condicional": "clv_zona = 14", "nombre": "Cordoba",         "color": "235 151 78"},
    {"id_capa": "cz3015",   "condicional": "clv_zona = 15", "nombre": "Zongolica",       "color": "93 188 210"},
    {"id_capa": "cz3016",   "condicional": "clv_zona = 16", "nombre": "Veracruz",        "color": "158 53 147"},
    {"id_capa": "cz3017",   "condicional": "clv_zona = 17", "nombre": "Boca del Rio",    "color": "196 46 96"},
    {"id_capa": "cz3018",   "condicional": "clv_zona = 18", "nombre": "Tierra Blanca",   "color": "74 163 113"},
    {"id_capa": "cz3019",   "condicional": "clv_zona = 19", "nombre": "Cosamaloapan",    "color": "249 220 101"},
    {"id_capa": "cz3020",   "condicional": "clv_zona = 20", "nombre": "San Andres",      "color": "235 151 78"},
    {"id_capa": "cz3021",   "condicional": "clv_zona = 21", "nombre": "Acayucan",        "color": "93 188 210"},
    {"id_capa": "cz3022",   "condicional": "clv_zona = 22", "nombre": "Minatitlan",       "color": "158 53 147"},
    {"id_capa": "cz3023",   "condicional": "clv_zona = 23", "nombre": "Coatzacoalcos",   "color": "196 46 96"},
    {"id_capa": "cz3024",   "condicional": "clv_zona = 24", "nombre": "Huayacocotla",    "color": "74 163 113"},
    {"id_capa": "cz3025",   "condicional": "clv_zona = 25", "nombre": "Panuco",          "color": "249 220 101"},
    {"id_capa": "cz3029",   "condicional": "clv_zona = 29", "nombre": "Jaltipan",        "color": "235 151 78"},
]
