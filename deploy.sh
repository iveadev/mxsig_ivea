#!/bin/bash
#-----------------------------------------------
# 1.- copia de archivos de capas IVEA a mapserver
#-----------------------------------------------
rsync -avh  ivea/ ../mxsig/mapserver/map/mdm60/ivea/

#-----------------------------------------------
# 2.- copia de archivos de personalización en el cliente web
#-----------------------------------------------
rsync -avh mapa/ ../mxsig/clientes/mapa/ 

