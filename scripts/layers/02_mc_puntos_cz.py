# scripts/layers/02_mc_oficinas.py
descripcion = "Puntos de las Oficinas de Coordinacion IVEA"
output = "oficinas_cz"
tabla = "ivea.oficinas_cz"
campos_adicionales = ["clv_cz", "nom_cz"]
tipo_capa = "POINT"

# RESPATE DE CARACTERES: Corrige los acentos rotos de la BD (como 'CRDOBA') al vuelo
encoding_global = "ISO-8859-1" 

# CONFIGURACIONES GLOBALES PARA PUNTOS
symbol_global = "circle"
size_global = 9
outlinecolor_global = "0 0 0"

modo_generacion = "MULTIPLES_CAPAS"

capas = [
    {"id_capa": "cz3001_p", "condicional": "clv_cz = 1",  "nombre": "Tantoyuca", "color": "235 151 78"},
    {"id_capa": "cz3003_p", "condicional": "clv_cz = 3",  "nombre": "Chicontepec", "color": "93 188 210"},
    {"id_capa": "cz3004_p", "condicional": "clv_cz = 4",  "nombre": "Tuxpan", "color": "158 53 147"},
    {"id_capa": "cz3014_p", "condicional": "clv_cz = 14", "nombre": "Córdoba", "color": "188 53 53"}
]
