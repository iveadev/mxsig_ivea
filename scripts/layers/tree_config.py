"""
Definición de los grupos y temas del árbol de capas del cliente.

Las llaves de ``GRUPOS`` y ``TEMAS`` son nombres representativos; el orden en
el que aparecen es el orden en el que se publican.  ``genera_tree.py`` los
traduce a identificadores cortos (``G1``, ``G2``... y ``T1``, ``T2``...).

Las capas se agregan a los grupos desde su propia definición
(``_tree["grupo"]``), usando la misma llave representativa de ``GRUPOS``.  Los
temas conservan su arreglo ``layers`` para poder repetir una capa en más de un
tema.
"""

from scripts.layers.constantes import coordinaciones


GRUPOS = {
    "marco_geoestadistico": {
        "label": "L&iacute;mites del Marco Geoestad&iacute;stico de Veracruz 2025",
    },
    "infraestructura_ivea": {
        "label": "Infraestructura IVEA",
    },
    "marco_geoestadistico_ivea": {
        "label": "Marco Geoestadístico IVEA",
    },
    "pobreza_multidimensional_inegi": {
        "label": "Pobreza multidimensional INEGI",
    },
    "coordinaciones_norte": {
        "label": "Coordinaciones Regional Norte",
    },
    "coordinaciones_centro": {
        "label": "Coordinaciones Regional Centro",
    },
    "coordinaciones_sur": {
        "label": "Coordinaciones Regional Sur",
    },
    "rezago_educativo_inea": {
        "label": "Estimación del Rezago Educativo INEA 2025 (temático)",
    },
    "denue": {
        "label": "DENUE",
    },
    "otras_capas": {
        "label": "Otras capas",
    },
    "rezago_educativo_censo": {
        "label": "Rezago Educativo CENSO 2020",
    },
    "rezago_censo_2020_edades_y_sexo": {
        'label': 'Rezago Educativo por edad y sexo CENSO 2020'
    },
    # "rezago_censo_2020_edades_y_sexo_sin_prim": {
    #     'label': 'Rezago Educativo por edad y sexo CENSO 2020 (sin primaria)'
    # },
    
    "test": {
        "label": "***Capas de prueba de compatibilidad con MDM***"
    },
}


TEMAS = {
    "coordinaciones_zona": {
        "label": "Coordinaciones de Zona IVEA",
        "layers": [
            "c_" + cz["id_capa"] for cz in coordinaciones
        ] + [
            "c_oficinas_cz",
        ],
        "desc": "Coordinaciones de Zona IVEA",
        "img": "coordinaciones.png",
    },
    "rezago_educativo": {
        "label": "Rezago Educativo",
        "layers": [
            "c_oficinas_cz",
            "c_rezago_educativo_porcentaje_rezago_total",
        ],
        "desc": "Rezago Educativo",
        "img": "ivea.png",
    },
    "rezago_social": {
        "label": "Rezago social",
        "layers": [
            "c_grado_rezago_social",
        ],
        "desc": "Rezago social 2020",
        "img": "inegi.png",
    },
    "grado_marginacion": {
        "label": "Grado de Marginación",
        "layers": [
            "c_grado_marginacion",
        ],
        "desc": "Grado de Marginación",
        "img": "inegi.png",
    },
    "pobreza": {
        "label": "Pobreza",
        "layers": [
            "c_tematico_pobreza",
        ],
        "desc": "Pobreza",
        "img": "inegi.png",
    },
    "pueblos_indigenas_pvd": {
        "label": "Pueblos Indígenas PVD",
        "layers": [
            "c_municipios_indigenas_pvd",
        ],
        "desc": "Pueblos Indígenas PVD",
        "img": "mun_indigena_pvd.png",
    },
    "regiones_economicas_pvd": {
        "label": "Regiones económicas PVD",
        "layers": [
            "c_mun_regiones_pvd",
        ],
        "desc": "Regiones económicas PVD",
        "img": "regiones.png",
    },
}
