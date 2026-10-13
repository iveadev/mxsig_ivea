

# Archivo de deficion para las capas Indice de Pobreza del CONEVAL
descripcion =  "Indice de Pobreza del CONEVAL en munucipios de Veracruz"
# Nombre del archivo de salida
output =  "ivea/tematico_pobreza.map"

# nombre de la tabla en la base de datos, comenzando con el esquema, por ejemplo: "esquema.tabla"
tabla =  "coneval.indice_pobreza"
#Campos adicionales a seleccionar en la subconsulta SQL
campos_adicionales = ["porcentaje"]

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
    {"id_capa": "c_pobreza_0",
        "condicional": "porcentaje<50",
        "nombre": "Menor al 50%",
        "color": "255 255 255"
    },
    {
        "id_capa": "c_pobreza_50",
        "condicional" : "porcentaje>=50 and porcentaje<60",
        "nombre": "50% a 59%",
        "color": "240 219 201"
    },
    {
        "id_capa": "c_pobreza_60",
        "condicional" : "porcentaje>=60 and porcentaje<70",
        "nombre": "60% a 69%",
        "color": "204 169 137"
    },
    {
        "id_capa": "c_pobreza_70",
        "condicional" : "porcentaje>=70 and porcentaje<80",
        "nombre": "70% a 79%",
        "color": "186 126 69"
    },
    {
        "id_capa": "c_pobreza_80",
        "condicional" : "porcentaje>=80 and porcentaje<90",
        "nombre": "80% a 89%",
        "color": "143 98 20"
    },
    {
        "id_capa": "c_pobreza_90",
        "condicional" : "porcentaje>=90",
        "nombre": "90% o más",
        "color": "66 52 28"
    }
]