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

def get_flights():
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"
    querystring = {"originSkyId":"LOND",
                   "destinationSkyId":"NYCA",
                   "originEntityId":"27544008",
                   "destinationEntityId":"27537542",
                   "cabinClass":"economy",
                   "adults":"1",
                   "sortBy":"best",
                   "currency":"USD",
                   "market":"en-US",
                   "countryCode":"US"
                   }
    return