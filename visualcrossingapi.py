import requests
from classes import LocationWeather
import os 


def translate_vc_condition_to_sky_string(visual_crossing_type):
    snowGroup = ["type_9","type_40", "type_1", "type_10", "type_11", "type_12", "type_13", "type_14", "type_15", "type_16", "type_17", "type_22","type_23",
                 "type_31", "type_32", "type_33", "type_34", "type_35"]
    
    sunGroup = ["type_43"]

    cloudsun = ["type_42"] 

    clearGroup = ["type_5", "type_6"]

    rainGroup= ["type_5","type_6","type_19","type_2","type_20","type_21", "type_24","type_25","type_26", "type_3","type_4"]

    cloudGroup= ["type_8", "type_27", "type_28", "type_29","type_30", "type_41"]

    thunderGroup = ["type_37", "type_38", "type_39"]

    print(visual_crossing_type)
    if visual_crossing_type in snowGroup:
        return "snow"
    elif visual_crossing_type in sunGroup:
        return "sun"
    elif visual_crossing_type in cloudsun:
        return "sun and cloud"
    elif visual_crossing_type in clearGroup:
        return "clear"
    elif visual_crossing_type in rainGroup:
        return "rain"
    elif visual_crossing_type in cloudGroup:
        return "cloudy"
    elif visual_crossing_type in thunderGroup:
        return "lightning and thunder"



def get_weather_from_visual_crossing(city:str, fra_dato:str, til_dato:str )->[LocationWeather]: #det betyr at funksjonen vil returnere en liste CityWeather objekt # tidsrange ser sånn ut : '2023-10-25/2023-10-28'
    api_key = os.getenv("VISUAL_CROSSING_API_KEY")
    response = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{fra_dato}/{til_dato}?unitGroup=metric&key={api_key}&lang=id")
    
    data = response.json()

    dayList = data["days"] #dager hentet fra apiet 

    myWeatherList = [] #min liste som fylles med cityweather objekter

    for day in dayList:
        
        conditions = day["conditions"].split(", ")
        first_condition = conditions[0]

        temp = day["temp"]
        sky = translate_vc_condition_to_sky_string(first_condition) #trenger denne for beskrivelse av værtypen for at jeg skal kunne vise icon
        cityname = data["resolvedAddress"]
        date = day["datetime"]
        

        weather = LocationWeather(temp=temp, cityname=cityname, date=date, sky=sky) 
        # Lag et nytt cityweather objekt basert på dataene i day objektet som er ett objekt fra listen du fikk i APIet
        myWeatherList.append(weather) # Legg til objektet i din egen liste


    return myWeatherList # Returner en liste med CityWeather Objekter