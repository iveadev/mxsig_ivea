#---------------------------------------------------------------------
# Multiples Capas (a partir de una condicional)
#---------------------------------------------------------------------

descripcion = "Escuelas primarias en el estado de Veracruz"
output = "denue_escuelas_primarias"
tabla = "denue.escuelas_primarias"
campos_adicionales = [""]
tipo_capa = "POINT"

# CONFIGURACIONES GLOBALES PARA PUNTOS
symbol_global = "circulor"
size_global = 9
outlinecolor_global = "0 0 0"
color_global = '0 0 0'

# --- VARIABLE SELECTORA DEL CASO DE USO ---
# Opciones soportadas: 
# 1. "MULTIPLES_CAPAS"  -> Genera un LAYER individual por cada fila (Tu enfoque actual de MxSIG)
# 2. "MULTIPLES_ESTILOS" -> Genera UN SOLO LAYER en MxSIG con múltiples bloques CLASS dentro
modo_generacion = "MULTIPLES_CAPAS" 

#Definición de las propiedades de las capas:
#   id_capa: Nombre de la capa generada en mapserver
#   condicional: Condición SQL para filtrar la capa
#   nombre: Nombre de la capa que se mostrará en el mapa

#   Valores a sobrescribir de acuerdo al tipo de capa:
#   color: Color de la capa
#   opacity: Opacidad de la capa, si no está definido se omitirá en la capa
#   outlinecolor: Color del contorno de la capa, si no está definido se omitirá en la capa

capas =  [
    {'id_capa': 'c_denue_escuelas_primarias', "nombre": "primarias", 'color': '23 23 23'},
]
