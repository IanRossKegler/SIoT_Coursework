import pyowm
import datetime


def get_weather():

    try:
        owm = pyowm.OWM('####')  # You MUST provide a valid API key
        obs = owm.weather_at_place('London,GB')
        w = obs.get_weather()
        uvi = owm.uvindex_around_coords(51.5074, 0.1278)
        return [uvi.get_value(), w.get_clouds()]

    except:
        f = open('errors.txt', 'w')
        f.write('OWM error at ' + str(datetime.datetime.now()))
        f.close()
        return ['NA', 'NA']
