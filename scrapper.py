import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

primera_request = requests.get("https://www.promiedos.com.ar/primera")
primera_pagina = BeautifulSoup(primera_request.content, "html.parser")

categorias_raw = []
categorias = []

datos_equipo_raw = []
datos_equipo = []
datos_equipos = []


#busco tabla en la web
tabla_actual_raw = primera_pagina.find(id="posiciones")
#filtro en una lista el codigo de todos los equipos y su categoria, tr es el formato de tabla/lista de promiedos
equipos_raw = tabla_actual_raw.find_all("tr")


#para cada elemento de la lista, es decir cada fila de la tabla
for e in equipos_raw:

    #busco las categorias
    if e.find("th"):

        #lista con todas las categorias raw
        categorias_raw = e.find_all("th")

        #las filtro en formato texto
        for i in categorias_raw:
            categorias.append(i.text)
        datos_equipos.append(categorias)

    else:
        #pongo en lista raw todos los equipos
        datos_equipo_raw = e.find_all("td")

        #filtro los datos en una lista en texto para cada equipo
        for i in datos_equipo_raw:
            datos_equipo.append(i.text)
        datos_equipos.append(datos_equipo)

        #limpio la variable temporal
        datos_equipo = []

tabla = np.array(datos_equipos)
print(tabla)

