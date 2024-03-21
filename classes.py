
#lager en klasse 
class LocationWeather:
    temp:int
    sky:str # Kan være sun, snow, clear eller rain
    def __init__(self, cityname, temp, sky, date=None) -> None:
        self.temp = temp
        self.sky = sky 
        self.cityname = cityname
        self.date = date
