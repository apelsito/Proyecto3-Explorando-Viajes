import pandas as pd
import numpy as np
import datetime

# Requests
import requests

from time import sleep
import random

# Para trabajar con archivos dotenv y los tokens
# -----------------------------------------------------------------------
import os
import dotenv
dotenv.load_dotenv()


def get_airport(city):
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
    
    key = os.getenv("airscraperTest") #Api de rapid API Testear
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"
    headers = {
	    "x-rapidapi-key": key,
	    "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    to_json = response.json()
    return to_json


def obtain_df_flights(result_json,flight_class):
    results = result_json
    df_plane = pd.DataFrame()
    for i in range(0,len(results["data"]["itineraries"])):
        precio = results["data"]["itineraries"][i]["price"]["formatted"]
        origen_ida = results["data"]["itineraries"][i]["legs"][0]["origin"]["city"]
        destino_ida = results["data"]["itineraries"][i]["legs"][0]["destination"]["city"]
        duracion_ida = results["data"]["itineraries"][i]["legs"][0]["durationInMinutes"]
        fecha_salida_ida = results["data"]["itineraries"][i]["legs"][0]["departure"]
        fecha_llegada_ida = results["data"]["itineraries"][i]["legs"][0]["arrival"]
        aerolinea_ida = results["data"]["itineraries"][i]["legs"][0]["carriers"]["marketing"][0]["name"]

        origen_vuelta = results["data"]["itineraries"][i]["legs"][1]["origin"]["city"]
        destino_vuelta = results["data"]["itineraries"][i]["legs"][1]["destination"]["city"]
        duracion_vuelta = results["data"]["itineraries"][i]["legs"][1]["durationInMinutes"]
        fecha_salida_vuelta = results["data"]["itineraries"][i]["legs"][1]["departure"]
        fecha_llegada_vuelta = results["data"]["itineraries"][i]["legs"][1]["arrival"]
        aerolinea_vuelta = results["data"]["itineraries"][i]["legs"][1]["carriers"]["marketing"][0]["name"]
        df_temp = pd.DataFrame({
            "clase" : flight_class,
            "precio (€)" : [precio],
            "origen_ida" : [origen_ida],
            "destino_ida" : [destino_ida],
            "duracion_ida (min)" :[duracion_ida],
            "fecha_salida_ida" : [fecha_salida_ida],
            "fecha_llegada_ida" : [fecha_llegada_ida],
            "aerolínea_ida" : [aerolinea_ida],
            "origen_vuelta" : [origen_vuelta],
            "destino_vuelta" : [destino_vuelta],
            "duracion_vuelta (min)" : [duracion_vuelta],
            "fecha_salida_vuelta" : [fecha_salida_vuelta],
            "fecha_llegada_vuelta" : [fecha_llegada_vuelta],
            "aerolínea_vuelta" : [aerolinea_vuelta]
        })
        df_temp["precio (€)"] = df_temp["precio (€)"].str.strip(" €").str.replace(",","").astype(int)
        df_temp["fecha_salida_ida"] = pd.to_datetime(df_temp["fecha_salida_ida"],format="mixed")
        df_temp["fecha_llegada_ida"] = pd.to_datetime(df_temp["fecha_llegada_ida"],format="mixed")
        df_temp["fecha_salida_vuelta"] = pd.to_datetime(df_temp["fecha_salida_vuelta"],format="mixed")
        df_temp["fecha_llegada_vuelta"] = pd.to_datetime(df_temp["fecha_llegada_vuelta"],format="mixed")
        df_temp["duracion_ida (min)"] = df_temp["duracion_ida (min)"].astype(int)
        df_temp["duracion_vuelta (min)"] = df_temp["duracion_vuelta (min)"].astype(int)
        df_plane = pd.concat([df_plane,df_temp],ignore_index=True)
    return df_plane


def get_flights(df_flights):
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
    
    for search_index in range(0,len(querystrings)//2):
        querys_destination1.append(querystrings[search_index]["cabinClass"])
        result = make_search(querystrings[search_index])
        res_searches_destination1.append(result)
        sleep(1)

    for search_index2 in range(len(querystrings)//2,len(querystrings)):
        querys_destination2.append(querystrings[search_index2]["cabinClass"])
        result2 = make_search(querystrings[search_index2])
        res_searches_destination2.append(result2)
        sleep(1)


    return

