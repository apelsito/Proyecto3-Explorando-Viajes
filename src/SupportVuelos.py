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

def search_querys(df_flights,dates):
    skyId = df_flights["skyId"].tolist()
    entityId = df_flights["entityId"].tolist()
    cabinClass = ["economy","premium_economy","business","first"]
    querystrings = []

    for i in range(1,len(entityId)):
        for date in dates:
            for clase in cabinClass:
                querystring = {
                    "originSkyId":skyId[0],
                    "destinationSkyId":"NCE",
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

def get_flights(df_flights,dates):
    
    key = os.getenv("airscraperTest")
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"

    querystring = search_querys(df_flights,dates)

    headers = {
	    "x-rapidapi-key": key,
	    "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return

