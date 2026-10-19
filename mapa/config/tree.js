/*
Archivo personalizado para IVEA, sustituye al archivo original de MXSIG
*/

// Definición de las coordinaciones de zona IVEA
const coordinaciones = [
  {
    "id": "c_cz3001",
    "label": "Tantoyuca",
    "regional": "Norte"
  },
  {
    "id": "c_cz3003",
    "label": "Chicontepec",
    "regional": "Norte"
  },
  {
    "id": "c_cz3004",
    "label": "Tuxpan",
    "regional": "Norte"
  },
  {
    "id": "c_cz3005",
    "label": "Poza Rica",
    "regional": "Norte"
  },
  {
    "id": "c_cz3006",
    "label": "Papantla",
    "regional": "Norte"
  },
  {
    "id": "c_cz3007",
    "label": "Espinal",
    "regional": "Norte"
  },
  {
    "id": "c_cz3008",
    "label": "Martinez",
    "regional": "Norte"
  },
  {
    "id": "c_cz3009",
    "label": "Perote",
    "regional": "Centro"
  },
  {
    "id": "c_cz3010",
    "label": "Xalapa",
    "regional": "Centro"
  },
  {
    "id": "c_cz3011",
    "label": "Coatepec",
    "regional": "Centro"
  },
  {
    "id": "c_cz3012",
    "label": "Huatusco",
    "regional": "Centro"
  },
  {
    "id": "c_cz3013",
    "label": "Orizaba",
    "regional": "Centro"
  },
  {
    "id": "c_cz3014",
    "label": "Cordoba",
    "regional": "Centro"
  },
  {
    "id": "c_cz3015",
    "label": "Zongolica",
    "regional": "Centro"
  },
  {
    "id": "c_cz3016",
    "label": "Veracruz",
    "regional": "Centro"
  },
  {
    "id": "c_cz3017",
    "label": "Boca del Rio",
    "regional": "Sur"
  },
  {
    "id": "c_cz3018",
    "label": "Tierra Blanca",
    "regional": "Sur"
  },
  {
    "id": "c_cz3019",
    "label": "Cosamaloapan",
    "regional": "Sur"
  },
  {
    "id": "c_cz3020",
    "label": "San Andres",
    "regional": "Sur"
  },
  {
    "id": "c_cz3021",
    "label": "Acayucan",
    "regional": "Sur"
  },
  {
    "id": "c_cz3022",
    "label": "Minatitlan",
    "regional": "Sur"
  },
  {
    "id": "c_cz3023",
    "label": "Coatzacoalcos",
    "regional": "Sur"
  },
  {
    "id": "c_cz3024",
    "label": "Huayacocotla",
    "regional": "Norte"
  },
  {
    "id": "c_cz3025",
    "label": "Panuco",
    "regional": "Norte"
  },
  {
    "id": "c_cz3029",
    "label": "Jaltipan",
    "regional": "Sur"
  }
];

// objeto para el grupo de capas de coordinaciones de zona IVEA
const layers_norte = {};
const layers_centro = {};
const layers_sur = {};
let posicion_capa=10
coordinaciones.forEach((cz) => {
    if(cz.regional === 'Norte') {
        layers_norte[cz.id] = {
            label: cz.id.toUpperCase().replace("C_","") + ' - ' + cz.label,
            scale: 1,
            position: posicion_capa++,
            active: false
        };
    } else if(cz.regional === 'Centro') {
        layers_centro[cz.id] = {
            label: cz.id.toUpperCase().replace("C_","") + ' - ' + cz.label,
            scale: 1,
            position: posicion_capa++,
            active: false
        };
    } else if(cz.regional === 'Sur') {
        layers_sur[cz.id] = {
            label: cz.id.toUpperCase().replace("C_","") + ' - ' + cz.label,
            scale: 1,
            position: posicion_capa++,
            active: false
        };
    }
});

const layers_coneval = {};
const coneval = [
  {
    "id_capa": "t_tematico_pobreza",
    "label": "Pobreza",
  },
  {
    "id_capa": "t_tematico_marginacion",
    "label": "Marginación",  
  },
  {
    "id_capa": "t_tematico_rezago_social",
    "label": "Rezago Social",
  },
];


coneval.forEach((p)=> {
  layers_coneval[p.id_capa] = 
     {
        label: p.label,
        scale: 1,
        position: posicion_capa++,
        active: false,
        texts:{
          scale:1,
          active:false
        }
    };
})





define(function() {
    var data = {
        themes:{
			T1:{
				label:'Coordinaciones de Zona IVEA',
                    layers:coordinaciones.map(cz => cz.id).concat(['c_oficinas_cz']),
                    desc:'Coordinaciones de Zona IVEA',
                    img:'mexico.jpg'
                },
        	},
        baseLayers:{
              B1:{
                type:'Wms',
                label:'Topogr&aacute;fico sin sombreado - INEGI',
                img:'mapa_sin_sombreado.jpg',		             
                url:['https://gaiamapas1.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas3.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas2.inegi.org.mx/mdmCache/service/wms?'],
				layer:'MapaBaseTopograficov61_sinsombreado',
                rights:'Derechos Reservados &copy; INEGI',
                tiled:true,
				legendlayer:['c100','c101','c102','c102-r','c102m','c103','c109','c110','c111','c112','c200','c201','c202','c203','c206','c300','c301','c302','c310','c311','c762','c793','c795'],
                desc:'REPRESENTACION DE RECURSOS NATURALES Y CULTURALES DEL TERRITORIO NACIONAL A ESCALA 1: 250 000, BASADO EN IMAGENES DE SATELITE DEL  2002 Y TRABAJO DE CAMPO REALIZADO EN 2003',
                clasification:'VECTORIAL'
            },
			 B2:{
                type:'Wms',
                label:'Topogr&aacute;fico gris - INEGI ',
                img:'mapa_gris.jpg',		             
                url:['https://gaiamapas1.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas3.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas2.inegi.org.mx/mdmCache/service/wms?'],
				layer:'MapaBaseTopograficov61_sinsombreado_gris', 
                rights:'Derechos Reservados &copy; INEGI',
                tiled:true,
				legendlayer:['c100','c101','c102','c102m','c103','c109','c110','c112','c200','c202','c203','c300','c301','c302','c310','c311','c793','c795'],
				legendUrl:'http://10.152.11.41:82/cgi-bin/ms62/mapserv?map=/opt/map/mdm60/mdm61leyendaprueba_gris.map&Request=GetLegendGraphic&format=image/png&Version=1.1.1&Service=WMS&LAYER=',
                desc:'REPRESENTACION DE RECURSOS NATURALES Y CULTURALES DEL TERRITORIO NACIONAL A ESCALA 1: 250 000, BASADO EN IMAGENES DE SATELITE DEL  2002 Y TRABAJO DE CAMPO REALIZADO EN 2003',
                clasification:'VECTORIAL'
            },
			B3:{
               type:'Wms',
                label:'Topogr&aacute;fico con sombreado - INEGI',
                img:'mapa_con_sombreado.jpg',		             
                  url:['https://gaiamapas1.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas3.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas2.inegi.org.mx/mdmCache/service/wms?'],
				 layer:'MapaBaseTopograficov61_consombreado',
                rights:'Derechos Reservados &copy; INEGI',
                tiled:true,
				legendlayer:['c100','c101','c102','c102-r','c102m','c103','c109','c110','c111','c112','c200','c201','c202','c203','c206','c300','c301','c302','c310','c311','c762','c793','c795'],
                desc:'REPRESENTACION DE RECURSOS NATURALES Y CULTURALES DEL TERRITORIO NACIONAL A ESCALA 1: 250 000, BASADO EN IMAGENES DE SATELITE DEL  2002 Y TRABAJO DE CAMPO REALIZADO EN 2003',
                clasification:'VECTORIAL'
            },
            B4:{
                type:'Wms',
                label:'Hipsogr&aacute;fico - INEGI',
                img:'baseHipsografico.jpg',		             
                url:['https://gaiamapas1.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas3.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas2.inegi.org.mx/mdmCache/service/wms?'],
                layer:'MapaBaseHipsografico',
				rights:'&copy; INEGI 2013',
                tiled:true,
                legendlayer:['img_altimetria.png'],
                desc:'IMAGEN DE RELIEVE QUE MUESTRA UNA COMBINACION DE ELEVACION A TRAVES DE COLORES HIPSOGRAFICOS, GENERADA POR PROCESAMIENTO DEL CONTINUO DE ELEVACIONES MEXICANOS DE 3.0 DE 15 METROS.',
                clasification:'RASTER'
            },
            B5:{
                type:'Wms',
                label:'Ortofotos - INEGI',
                img:'baseOrtos.jpg',		             
                url:['https://gaiamapas1.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas3.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas2.inegi.org.mx/mdmCache/service/wms?'],
                layer:'MapaBaseOrtofoto',
				rights:'&copy; INEGI 2013',
                tiled:true,
                desc:'CONJUNTO DE IMAGENES AEREAS ORTORECTIFICADAS A DIVERSAS ESCALAS Y RESOLUCIONES, PROVENIENTES DEL ACERVO DE ORTOFOTOS DE INEGI Y QUE CORRESPONDEN A TOMAS REALIZADAS EN EL LAPSO 2005-2012.',
                clasification:'RASTER'
                },		
			 B6:{
                type:'Wms',
                label:'ICDS - INEGI',
                img:'baseICDS.jpg',		             
                url:['https://gaiamapas1.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas3.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas2.inegi.org.mx/mdmCache/service/wms?'],
                //Check ip,
                layer:'ICDS',
				rights:'&copy; INEGI 2017',
                tiled:true,
                desc:'CONJUNTO DE IMAGENES CARTOGÁFICAS DIGITALES DE LA CARTAS TOPOGRÁFICAS ESCALA 1:50,000',
                clasification:'RASTER'
                },		
            B7:{
                type:'Osm',
                label:'Open Street Map',
                img:'Osm.jpg',
                rights:'&copy; OpenStreetMap contributors',
                clasification:'VECTORIAL'
            },
			B9:{
				type:'Esri',
				label:'Esri map',
				img:'Esri.jpg',
				url:'http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/${z}/${y}/${x}',
				rights:'&copy; ESRI',
				clasification:'VECTORIAL'
			},
			B10:{
				hidden:true,
                type:'Wms',
                label:'Topográfico gris INE-INEGI',
                img:'mapa_gris.jpg',		             
                url:['https://gaiamapas1.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas3.inegi.org.mx/mdmCache/service/wms?','https://gaiamapas2.inegi.org.mx/mdmCache/service/wms?'],
                //Check ip,
                layer:'MapaBase_geoelectoral_sl',
				rights:'&copy; INEGI 2017',
                tiled:true,
                desc:'CONJUNTO DE IMAGENES CARTOGÁFICAS DIGITALES DE LA CARTAS TOPOGRÁFICAS ESCALA 1:50,000',
                clasification:'VECTORIAL'
                }
        },
		layers:{
            groups:{			
			G1:{
                    label:'L&iacute;mites del Marco Geoestad&iacute;stico de Veracruz 2025',
                    layers:{
                        c_edo_ver:{
                            label:'Estatal',
                            synonymous:['estado','estatales'],
                            scale:1,
                            position:1,
                            active:true,
                        },
                        c_mun_ver:{
                            label:'Municipal',
                            synonymous:['municipios','mun'],
                            scale:1,
                            position:1,
                            active:false,
                            texts:{
                                scale:1,
                                active:false
                            }
                        },
                    }
                },
      G2:{
              label:'Infraestructura IVEA',
              layers: {
                c_oficinas_cz:{
                  label: 'Ubicación de las Coordinaciones de Zona (puntos)',
                  scale:1,
                  position:2,
                  active:false,
                  texts:{
                      scale:1,
                      active:false
                  }
                },
              },
            },
       G3:{
              label:'Marco Geoestadístico IVEA',
              layers: {
                c_tematico_cz:{
                  label: 'Coordinaciones de Zona (tematico)',
                  scale:1,
                  position:3,
                  active:false,
                }
              }
          },
      G4:{
              label:'CONEVAL',
              layers:layers_coneval,
          },

			G5:{
          label:'Coordinaciones Reginal Norte',
          layers:layers_norte,
      },
        G6:{
                label:'Coordinaciones Regional Centro',
                layers:layers_centro,
            },
        G7:{
                label:'Coordinaciones Regional Sur',
                layers:layers_sur,
            },
            
          G8:{
            label:'Estimación del Rezago Educativo INEA2025 (tematico)',
            layers:{
              c_rezago_educativo_porcentaje_rezago_total:{
                label: 'Porcentaje total del rezago en Veracruz',
                scale:1,
                position:posicion_capa++,
                active:false,
                texts:{
                  scale:1,
                  active:false
                }
              },
              c_rezago_educativo_porcentaje_analfabetismo:{
                label: 'Porcentaje de analfabetismo',
                scale:1,
                position: posicion_capa++,
                active:false,
                texts:{
                  scale:1,
                  active:false
                }
              },
              c_rezago_educativo_porcentaje_sin_primaria:{
                label: 'Porcentaje sin primaria',
                scale:1,
                position: posicion_capa++,
                active:false,
                texts:{
                  scale:1,
                  active:false
                }
              },
              c_rezago_educativo_porcentaje_sin_secundaria:{
                label: 'Porcentaje sin secundaria',
                scale:1,
                position: posicion_capa++,
                active:false,
                texts:{
                  scale:1,
                  active:false
                }
              }
            },
          },
          G9:{
            label:'DENUE',
            layers:{
              c_denue_escuelas_primarias:{
                label: 'Escuelas primarias',
                scale:1,
                position:posicion_capa++,
                active:false,
                texts:{
                  scale:1,
                  active:false
                }
              },
              c_denue_escuelas_secundarias:{
                label: 'Escuelas secundarias',
                scale:1,
                position: posicion_capa++,
                active:false,
                texts:{
                  scale:1,
                  active:false
                }
              },
              c_denue_escuelas_media_superior:{
                label: 'Escuelas Media Superior',
                scale:1,
                position: posicion_capa++,
                active:false,
                texts:{
                  scale:1,
                  active:false
                }
              },
            },
          },      
        },
      }
    };
	if(typeof(treeConfig)!='undefined'){
        data = $.extend(data, treeConfig);
    }
    return data;
});