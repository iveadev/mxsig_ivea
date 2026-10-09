

# Archivo de deficion para las capas
descripcion =  "Población total del estado de Veracruz"
# Nombre del archivo de salida
output =  "ivea/poblacion_veracruz.map"

# nombre de la tabla en la base de datos, comenzando con el esquema, por ejemplo: "esquema.tabla"
tabla =  "marco_geoestadistico.poblacion"
#Campos adicionales a seleccionar en la subconsulta SQL
campos_adicionales = ["poblacion"]

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

capas = [
  {
    "id_capa": "c_poblacion_1",
    "condicional": "poblacion>=1543 and poblacion<8925",
    "color": "245 255 204",
    "nombre": "Rango de población 1"
  },
  {
    "id_capa": "c_poblacion_2",
    "condicional": "poblacion>=8925 and poblacion<16585",
    "color": "222 252 174",
    "nombre": "Rango de población 2"
  },
  {
    "id_capa": "c_poblacion_3",
    "condicional": "poblacion>=16585 and poblacion<24127",
    "color": "194 247 143",
    "nombre": "Rango de población 3"
  },
  {
    "id_capa": "c_poblacion_4",
    "condicional": "poblacion>=24127 and poblacion<39327",
    "color": "142 219 70",
    "nombre": "Rango de población 4"
  },
  {
    "id_capa": "c_poblacion_5",
    "condicional": "poblacion>=39327 and poblacion<61377",
    "color": "101 179 36",
    "nombre": "Rango de población 5"
  },
  {
    "id_capa": "c_poblacion_6",
    "condicional": "poblacion>=61377 and poblacion<85489",
    "color": "65 138 18",
    "nombre": "Rango de población 6"
  },
  {
    "id_capa": "c_poblacion_7",
    "condicional": "poblacion>=85489 and poblacion<144776",
    "color": "46 102 18",
    "nombre": "Rango de población 7"
  },
  {
    "id_capa": "c_poblacion_8",
    "condicional": "poblacion>=144776 and poblacion<607209",
    "color": "31 66 17",
    "nombre": "Rango de población 8"
  }
]