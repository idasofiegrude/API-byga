from flask import Flask, jsonify
from flask_cors import CORS
from visualcrossingapi import get_weather_from_visual_crossing
from datetime import date
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


app = Flask(__name__)
CORS(app)

## INNGANGSPORTER TIL KODEN MIN, SOM KAN NÅS VIA NETTVERK
@app.route('/by/<city>/<fra_dato>/<til_dato>') #år-mnd-dag
def get_daily_weather_list(city, fra_dato, til_dato):
    cityname = str(city)
    fra_dato = str(fra_dato)
    til_dato = str(til_dato)
    weatherList = get_weather_from_visual_crossing(cityname, fra_dato, til_dato)
    dict_list = []


    for class_object in weatherList:
        dict = vars(class_object)
        dict_list.append(dict)

    return jsonify(dict_list)



# bruker flask 
@app.route('/by/<city>') #<city> er at det kan være hvilken som helst city
def get_current_weather(city):
    
    today = date.today()
    print("Today's date:", today)
    cityname = str(city)
    weather = get_weather_from_visual_crossing(cityname, today, today)
    return vars(weather[0]) 
#vars er en funksjon som endrer json til en dictonary
#fordi det er det som fungerer i python



if __name__ == '__main__':
    app.run(debug=True)