# -----------------------------------------------------------------------
# Librerías para manejo de datos
# -----------------------------------------------------------------------
import pandas as pd   # Manipulación de datos tabulares
import numpy as np    # Operaciones numéricas y manejo de matrices
import datetime       # Manejo de fechas y tiempos

# -----------------------------------------------------------------------
# Librerías para solicitudes HTTP y peticiones a APIs
# -----------------------------------------------------------------------
import requests       # Para hacer solicitudes HTTP (GET, POST, etc.)
from time import sleep  # Para pausar la ejecución entre solicitudes
import random         # Para generar números aleatorios (si se necesita algún tipo de aleatorización)

# -----------------------------------------------------------------------
# Librerías para visualización de progreso
# -----------------------------------------------------------------------
from tqdm import tqdm  # Para crear barras de progreso durante los bucles

# -----------------------------------------------------------------------
# Librerías para manejo de variables de entorno y tokens
# -----------------------------------------------------------------------
import os             # Para interactuar con el sistema de archivos
import dotenv         # Para cargar variables de entorno desde un archivo .env
dotenv.load_dotenv()  # Cargar las variables de entorno en el entorno de ejecución

# -----------------------------------------------------------------------
# Librerías para trabajar con archivos JSON
# -----------------------------------------------------------------------
import json           # Para leer y escribir datos en formato JSON



def aiports_to_df(airports):
    """
    Convierte una lista de aeropuertos en un DataFrame de pandas, donde cada aeropuerto contiene información clave
    como 'skyId', 'entityId', 'flightPlaceType' y 'localizedName'.

    Args:
        airports (list): Una lista de listas, donde cada sublista contiene la información de un aeropuerto. 
                         Cada sublista tiene el formato:
                         - skyId (str): ID del aeropuerto en el sistema de la API.
                         - entityId (str): Identificador de la entidad del aeropuerto.
                         - flightPlaceType (str): Tipo de lugar (generalmente 'AIRPORT').
                         - localizedName (str): Nombre del aeropuerto.

    Returns:
        pd.DataFrame: Un DataFrame de pandas con las columnas 'skyId', 'entityId', 'flightPlaceType', y 'localizedName',
                      que contiene la información de todos los aeropuertos proporcionados en la lista 'airports'.

    Example:
        airports = [["123", "456", "AIRPORT", "Madrid Barajas"], ["789", "012", "AIRPORT", "Barcelona El Prat"]]
        df = aiports_to_df(airports)
    """
    df = pd.DataFrame()
    for i in range(0,len(airports)):
        df_temp = pd.DataFrame({
            "skyId": [airports[i][0]],
            "entityId": [airports[i][1]],
            "flightPlaceType" : [airports[i][2]],
            "localizedName" : [airports[i][3]]})
        df = pd.concat([df,df_temp],ignore_index=True)
    
    return df


def get_airport(city):
    """
    Realiza una búsqueda en la API de Sky-Scrapper para obtener información sobre un aeropuerto en función de una ciudad dada.

    Args:
        city (str): El nombre de la ciudad para la cual se busca información del aeropuerto.

    Returns:
        list: Una lista con los detalles del aeropuerto en el siguiente formato:
              [skyid, entityid, place_type, airport_name]. Si se encuentran varios resultados, solo se devuelve el primero que es un aeropuerto.
              - skyid (str): ID del aeropuerto en el sistema de la API.
              - entityid (str): Identificador de la entidad del aeropuerto.
              - place_type (str): Tipo de lugar (generalmente 'AIRPORT').
              - airport_name (str): Nombre del aeropuerto.

    Raises:
        Exception: Puede lanzar una excepción si la clave de API no está configurada correctamente o si hay un error en la solicitud a la API.
    """
    key = os.getenv("airscraper")
    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

    querystring = {
        "query":city,
        "locale":"es-ES"
        }

    headers = {
	    "x-rapidapi-key": key,
	    "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    sleep(1)
    response = requests.get(url, headers=headers, params=querystring)

    json_file = response.json()
    resultado = []
    if len(json_file["data"]) == 1:
        skyid = json_file["data"][0]["navigation"]["relevantFlightParams"]["skyId"]
        resultado.append(skyid)
        entityid = json_file["data"][0]["navigation"]["relevantFlightParams"]["entityId"]
        resultado.append(entityid)
        place_type = json_file["data"][0]["navigation"]["relevantFlightParams"]["flightPlaceType"]
        resultado.append(place_type)
        airport_name = json_file["data"][0]["navigation"]["relevantFlightParams"]["localizedName"]
        resultado.append(airport_name)
    else:
        for i in range(0,len(json_file["data"])):
            if json_file["data"][i]["navigation"]["relevantFlightParams"]["flightPlaceType"] == "AIRPORT":
                skyid = json_file["data"][i]["navigation"]["relevantFlightParams"]["skyId"]
                resultado.append(skyid)
                entityid = json_file["data"][i]["navigation"]["relevantFlightParams"]["entityId"]
                resultado.append(entityid)
                place_type = json_file["data"][i]["navigation"]["relevantFlightParams"]["flightPlaceType"]
                resultado.append(place_type)
                airport_name = json_file["data"][i]["navigation"]["relevantFlightParams"]["localizedName"]
                resultado.append(airport_name)
                break
            else:
                pass

    return resultado

def search_querys(df_flights,dates,cabinclass):
    """
    Genera una lista de cadenas de consulta (querystrings) para realizar búsquedas de vuelos en función de las fechas, 
    clases de cabina y datos de vuelos proporcionados.

    Args:
        df_flights (pd.DataFrame): Un DataFrame que contiene información de vuelos, incluyendo los campos 'skyId' y 'entityId'.
        dates (list): Una lista de listas que contienen pares de fechas de ida y vuelta en formato "YYYY-MM-DD".
                      Ejemplo: [["2024-10-24", "2024-10-27"], ["2024-11-01", "2024-11-05"], ...]
        cabinclass (list): Una lista con las clases de cabina a consultar. Ejemplo: ["economy", "premium_economy", "business", "first"].

    Returns:
        list: Devuelve una lista de diccionarios, donde cada diccionario es una cadena de consulta (querystring) para realizar búsquedas de vuelos.
              Cada querystring contiene información como el origen, destino, fechas de ida y vuelta, clase de cabina, y otros parámetros relevantes.
    
    Example:
        querystrings = search_querys(df_flights, dates, ["economy", "business"])

    """    
    skyId = df_flights["skyId"].tolist()
    entityId = df_flights["entityId"].tolist()
    querystrings = []

    for i in range(1,len(entityId)):
        for date in dates:
            for clase in cabinclass:
                querystring = {
                    "originSkyId":skyId[0],
                    "destinationSkyId":skyId[i],
                    "originEntityId": entityId[0],
                    "destinationEntityId": entityId[i],
                    "date":date[0],
                    "returnDate":date[1],
                    "cabinClass":clase,
                    "adults":"4",
                    "sortBy":"best",
                    "limit" : "10",
                    "currency":"EUR",
                    "market":"es-ES",
                    "countryCode":"ES"
                    }
                
                querystrings.append(querystring)
        
    return querystrings


def make_search(querystring):
    """
    Realiza una solicitud a la API de Sky-Scrapper para buscar vuelos completos basados en los parámetros de consulta proporcionados.

    Args:
        querystring (dict): Un diccionario que contiene los parámetros de la consulta para la búsqueda de vuelos. Los campos incluyen:
                            - originSkyId (str): ID del aeropuerto de origen.
                            - destinationSkyId (str): ID del aeropuerto de destino.
                            - originEntityId (str): ID de la entidad de origen.
                            - destinationEntityId (str): ID de la entidad de destino.
                            - date (str): Fecha de salida en formato "YYYY-MM-DD".
                            - returnDate (str): Fecha de regreso en formato "YYYY-MM-DD".
                            - cabinClass (str): Clase de cabina ("economy", "business", etc.).
                            - adults (str): Número de adultos para la búsqueda.
                            - sortBy (str): Criterio de ordenación de los resultados.
                            - limit (str): Número máximo de resultados.
                            - currency (str): Moneda de los precios (ej. "EUR").
                            - market (str): Mercado local (ej. "es-ES").
                            - countryCode (str): Código del país (ej. "ES").

    Returns:
        dict: Un diccionario en formato JSON que contiene los resultados de la búsqueda de vuelos si la solicitud es exitosa (código 200).
              Si la respuesta no es exitosa, imprime un mensaje de error y devuelve `None`.

    Raises:
        requests.RequestException: Si ocurre algún error en la solicitud HTTP, se captura la excepción y se imprime un mensaje de error.
    
    Example:
        querystring = {
            "originSkyId": "1234",
            "destinationSkyId": "5678",
            "originEntityId": "910",
            "destinationEntityId": "112",
            "date": "2024-10-24",
            "returnDate": "2024-10-30",
            "cabinClass": "economy",
            "adults": "4",
            "sortBy": "best",
            "limit": "10",
            "currency": "EUR",
            "market": "es-ES",
            "countryCode": "ES"
        }
        result = make_search(querystring)
    """
    
    key = os.getenv("airscraper")  # API de RapidAPI para Testear
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            to_json = response.json()
            return to_json
        else:
            print(f"Error en la respuesta: Código {response.status_code}")
            pass
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        pass

    key = os.getenv("airscraper") #Api de rapid API Testear
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"
    headers = {
	    "x-rapidapi-key": key,
	    "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            to_json = response.json()
            return to_json
        else:
            print(f"Error en la respuesta: Código {response.status_code}")
            pass
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        pass


def obtain_df_flights(result_json, flight_class):
    """
    Convierte los datos de itinerarios de vuelos en un DataFrame a partir de un resultado JSON de búsqueda de vuelos.
    La función procesa un máximo de 10 itinerarios por búsqueda, si están disponibles.

    Args:
        result_json (dict): Un diccionario en formato JSON que contiene los resultados de la búsqueda de vuelos,
                            incluyendo información como itinerarios, precios y detalles de los vuelos.
        flight_class (str): La clase de cabina del vuelo (por ejemplo, "economy", "business", etc.) para el vuelo actual.

    Returns:
        pd.DataFrame: Un DataFrame de pandas que contiene la información de los vuelos procesados con las siguientes columnas:
                      - "clase": Clase del vuelo.
                      - "precio (€)": Precio del vuelo en euros.
                      - "origen_ida": Ciudad de origen del vuelo de ida.
                      - "destino_ida": Ciudad de destino del vuelo de ida.
                      - "duracion_ida (min)": Duración del vuelo de ida en minutos.
                      - "fecha_salida_ida": Fecha de salida del vuelo de ida.
                      - "fecha_llegada_ida": Fecha de llegada del vuelo de ida.
                      - "aerolínea_ida": Aerolínea del vuelo de ida.
                      - "origen_vuelta": Ciudad de origen del vuelo de vuelta.
                      - "destino_vuelta": Ciudad de destino del vuelo de vuelta.
                      - "duracion_vuelta (min)": Duración del vuelo de vuelta en minutos.
                      - "fecha_salida_vuelta": Fecha de salida del vuelo de vuelta.
                      - "fecha_llegada_vuelta": Fecha de llegada del vuelo de vuelta.
                      - "aerolínea_vuelta": Aerolínea del vuelo de vuelta.

    Raises:
        KeyError: Si falta alguna de las claves esperadas en el resultado JSON.
        ValueError: Si hay un problema al convertir los precios o las fechas a su formato adecuado.

    Example:
        df_flights = obtain_df_flights(result_json, "economy")
    """
    results = result_json
    df_plane = pd.DataFrame()

    # Verificar si existe la clave "data" y "itineraries", para que no de error
    # A veces da error la búsqueda si no hay vuelos disponibles
    if "data" not in result_json or "itineraries" not in result_json["data"]:
        print(f"No hay datos disponibles en la búsqueda de {flight_class}.")
        return

    for i in range(0,len(results["data"]["itineraries"])):
        if i < 11:
            try:
                precio = results["data"]["itineraries"][i]["price"]["formatted"]
                # Datos del itinerario de ida
                origen_ida = results["data"]["itineraries"][i]["legs"][0]["origin"]["city"]
                destino_ida = results["data"]["itineraries"][i]["legs"][0]["destination"]["city"]
                duracion_ida = results["data"]["itineraries"][i]["legs"][0]["durationInMinutes"]
                fecha_salida_ida = results["data"]["itineraries"][i]["legs"][0]["departure"]
                fecha_llegada_ida = results["data"]["itineraries"][i]["legs"][0]["arrival"]
                aerolinea_ida = results["data"]["itineraries"][i]["legs"][0]["carriers"]["marketing"][0]["name"]

                # Datos del itinerario de vuelta
                origen_vuelta = results["data"]["itineraries"][i]["legs"][1]["origin"]["city"]
                destino_vuelta = results["data"]["itineraries"][i]["legs"][1]["destination"]["city"]
                duracion_vuelta = results["data"]["itineraries"][i]["legs"][1]["durationInMinutes"]
                fecha_salida_vuelta = results["data"]["itineraries"][i]["legs"][1]["departure"]
                fecha_llegada_vuelta = results["data"]["itineraries"][i]["legs"][1]["arrival"]
                aerolinea_vuelta = results["data"]["itineraries"][i]["legs"][1]["carriers"]["marketing"][0]["name"]

                df_temp = pd.DataFrame({
                    "clase": flight_class,
                    "precio (€)": [precio],
                    "origen_ida": [origen_ida],
                    "destino_ida": [destino_ida],
                    "duracion_ida (min)": [duracion_ida],
                    "fecha_salida_ida": [fecha_salida_ida],
                    "fecha_llegada_ida": [fecha_llegada_ida],
                    "aerolínea_ida": [aerolinea_ida],
                    "origen_vuelta": [origen_vuelta],
                    "destino_vuelta": [destino_vuelta],
                    "duracion_vuelta (min)": [duracion_vuelta],
                    "fecha_salida_vuelta": [fecha_salida_vuelta],
                    "fecha_llegada_vuelta": [fecha_llegada_vuelta],
                    "aerolínea_vuelta": [aerolinea_vuelta]
                })

                df_temp["precio (€)"] = df_temp["precio (€)"].str.strip(" €").str.replace(",", "").astype(int)
                df_temp["fecha_salida_ida"] = pd.to_datetime(df_temp["fecha_salida_ida"], format="mixed", errors="coerce")
                df_temp["fecha_llegada_ida"] = pd.to_datetime(df_temp["fecha_llegada_ida"], format="mixed", errors="coerce")
                df_temp["fecha_salida_vuelta"] = pd.to_datetime(df_temp["fecha_salida_vuelta"], format="mixed", errors="coerce")
                df_temp["fecha_llegada_vuelta"] = pd.to_datetime(df_temp["fecha_llegada_vuelta"], format="mixed", errors="coerce")
                df_temp["duracion_ida (min)"] = df_temp["duracion_ida (min)"].astype(int)
                df_temp["duracion_vuelta (min)"] = df_temp["duracion_vuelta (min)"].astype(int)

                df_plane = pd.concat([df_plane, df_temp], ignore_index=True)

            except:
                print(f"Error")
        else:
            break
         
    return df_plane



def get_flights(df_flights):
    """
    Convierte los resultados JSON obtenidos de la búsqueda de vuelos en un DataFrame, limitando los resultados a un máximo de 10 itinerarios.

    Args:
        result_json (dict): Un diccionario en formato JSON que contiene los resultados de la búsqueda de vuelos.
        flight_class (str): La clase de vuelo (economy, premium_economy, business, first) que corresponde a la búsqueda.

    Returns:
        pd.DataFrame: Un DataFrame que contiene los datos de los vuelos, incluyendo el precio, origen, destino, duración, fechas, y aerolíneas tanto de ida como de vuelta.
                      Si no hay resultados disponibles o ocurre un error, devuelve un DataFrame vacío.
    
    Raises:
        KeyError: Si no existen claves esperadas en el JSON para alguno de los itinerarios.
        Exception: Cualquier otro error en la extracción de datos se captura y muestra un mensaje de error.
    """
    dates = [["2024-10-24","2024-10-27"],["2024-10-31","2024-11-03"],["2024-11-07","2024-11-10"],["2024-11-14","2024-11-17"],["2024-11-21","2024-11-24"]]
    #Va a sacar 40 resultados si buscamos por todas las clases (economy, business...)
    cabinclass = ["economy","premium_economy","business","first"]
    querystrings = search_querys(df_flights,dates,cabinclass)
    #query por destino, hacemos dos listas
    querys_destination1 = []
    #Sacamos 20 resultados, que son todas las clases y fechas
    res_searches_destination1 = []
    #query por destino, hacemos dos listas
    querys_destination2 = []
    #Sacamos 20 resultados, que son todas las clases y fechas
    res_searches_destination2 = []
    #Hacemos división entera con //
    print("Buscando Primer Destino")
    for search_index in tqdm(range(0,len(querystrings)//2)):
        querys_destination1.append(querystrings[search_index]["cabinClass"])
        result = make_search(querystrings[search_index])
        #Guardamos cada json en una lista
        res_searches_destination1.append(result)
        sleep(0.3)
    print("Buscando Segundo Destino")
    for search_index2 in tqdm(range(len(querystrings)//2,len(querystrings))):
        querys_destination2.append(querystrings[search_index2]["cabinClass"])
        result2 = make_search(querystrings[search_index2])
        #Guardamos cada json en una lista
        res_searches_destination2.append(result2)
        sleep(0.3)

# Si la búsqueda falla, puedes descomentar esto y analizar que falla en la devolución de resultados en un json
#    data_to_save = {
#        "res_searches_destination1.json": res_searches_destination1,
#        "res_searches_destination2.json": res_searches_destination2
#    }   
    
#    for filename, data in data_to_save.items():
#        file_path = os.path.join("../datos/json_backups/", filename)
#        with open(file_path, "w") as file:
#            json.dump(data, file)

    df_result1 = [obtain_df_flights(json_res,querys_destination1[i]) for i, json_res in enumerate(res_searches_destination1)]
    df_results1 = pd.concat(df_result1, ignore_index=True)
    df_result2 = [obtain_df_flights(json_res,querys_destination2[i]) for i, json_res in enumerate(res_searches_destination2)]
    df_results2 = pd.concat(df_result2, ignore_index=True)
    df = pd.concat([df_results1,df_results2],ignore_index=True)
    return df