

# Archivo de deficion para las capas
descripcion =  "Población total del estado de Veracruz"

# Se toma la descripción, se puede editar en caso de ser ncesario
wms_title_global = descripcion

# Nombre del archivo de salida
output =  "ivea/poblacion_veracruz.map"

# Nombre de la capa global
id_capa = "capa_poblacion_veracruz"

# nombre de la tabla en la base de datos, comenzando con el esquema, por ejemplo: "esquema.tabla"
tabla =  "marco_geoestadistico.poblacion"

#Campos adicionales a seleccionar en la subconsulta SQL
campos_adicionales = ["poblacion"]

#Valores globales para las capas, si se definen aquí se aplicarán a todas las capas, si se definen en la capa se sobreescriben
opacity =  "60"
outlinecolor =  "60 60 60"
linewidth =  "0.8"

#Definición de las propiedades de las capas:
#   condicional: Condición para aplicar las clases, el campo debe estar entre corchetes, por ejemplo: [porcentaje]<50
#   nombre: Nombre de la clase
#   color: Color de relleno
#   opacity: Opacidad de la capa, si no está definido se omitirá en la capa
#   outlinecolor: Color del contorno de la capa, si no está definido se omitirá en la capa

clases = [
  {
    "condicional": "[poblacion]>=1543 and [poblacion]<8925",
    "color": "245 255 204",
    "nombre": "Rango de población 1"
  },
  { 
    "condicional": "[poblacion]>=8925 and [poblacion]<16585",
    "color": "222 252 174",
    "nombre": "Rango de población 2"
  },
  { 
    "condicional": "[poblacion]>=16585 and [poblacion]<24127",
    "color": "194 247 143",
    "nombre": "Rango de población 3"
  },
  { 
    "condicional": "[poblacion]>=24127 and [poblacion]<39327",
    "color": "142 219 70",
    "nombre": "Rango de población 4"
  },
  { 
    "condicional": "[poblacion]>=39327 and [poblacion]<61377",
    "color": "101 179 36",
    "nombre": "Rango de población 5"
  },
  { 
    "condicional": "[poblacion]>=61377 and [poblacion]<85489",
    "color": "65 138 18",
    "nombre": "Rango de población 6"
  },
  { 
    "condicional": "[poblacion]>=85489 and [poblacion]<144776",
    "color": "46 102 18",
    "nombre": "Rango de población 7"
  },
  { 
    "condicional": "[poblacion]>=144776 and [poblacion]<607209",
    "color": "31 66 17",
    "nombre": "Rango de población 8"
  }
]