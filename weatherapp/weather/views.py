from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from rest_framework import generics

import datetime
import json

import requests

class WeatherAPIView(generics.CreateAPIView):
    
    def get(self, request, *args, **kwargs):
        city = self.request.GET.get('city', '')
        country = self.request.GET.get('country', '')

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={settings.API_KEY}'

        location_data = requests.get(url).json()

        response = self.get_response_data(location_data)

        return HttpResponse(json.dumps(response, ensure_ascii=False),
            content_type="application/json")

    def get_response_data(self, data):
        """
        This method creates the response data that is returned by the API

        Args:
            param1: self
            param2: data returned by the call to openweathermap API

        Returns:
            A dictionary of data that will be returned by the API
        """
        DEGREE_SIGN = u'\N{DEGREE SIGN}'

        location_name = f"{data['name']}, {data['sys']['country']}"
        # temperature = round(data['main']['temp'] - 273.15) + " " + DEGREE_SIGN + " C" 
        # temperature = f"{round(data['main']['temp'] - 273.15)} {DEGREE_SIGN}C"
        temperature = f"{round(data['main']['temp'] - 273.15)} °C"
        # temperature = f"{round(data['main']['temp'] - 273.15)} C"
        wind = self.windType(data['wind']['speed']) \
               + ', ' \
               + str(data['wind']['speed']) \
               + ' m/s, ' \
               + self.degToDir(data['wind']['deg'])
        cloudiness = data['weather'][0]['description']
        pressure = f"{data['main']['pressure']} hpa"
        humidity = f"{data['main']['humidity']}%"
        sunrise = str(datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'))
        sunset = str(datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'))
        geo_coordinates = [
                            round(data['coord']['lat'], 2),
                            round(data['coord']['lon'], 2),
                            ]
        requested_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # requested_time = str(datetime.datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'))
        forecast = data['weather'][0]

        resp = {
            "location_name": location_name,
            "temperature": temperature,
            "wind": wind,
            "cloudiness": cloudiness,
            "pressure": pressure,
            "humidity": humidity,
            "sunrise": sunrise,
            "sunset": sunset,
            "geo_coordinates": geo_coordinates,
            "requested_time": requested_time,
            "forecast": forecast
        }

        return resp

    @staticmethod
    def degToDir(deg):
        """
        This method evaluates the direction of the wind based on the wind angle

        Args:
            param1: Angle of the wind in degrees

        Returns:
            A string which is the direction of the wind based on angle
        """
        directions = ["north", "north-northeast", "north-east", "east-northeast", 
                      "east", "east-southeast", "south-east", "south-southeast",
                      "south", "south-southwest", "south-west", "west-southwest", 
                      "west", "west-northwest", "north-west", "north-northwest",]
        
        # We have 16 directions and total 360 degrees
        # There is an angle change at every 22.5 degrees (360/16)
        val=int((deg/22.5)+.5)
        
        return directions[(val % 16)]

    @staticmethod
    def windType(speed):
        """
        This method evaluates the type of the wind based on wind speed

        Args:
            param1: Speed of the wind in m/s

        Returns:
            A string which is the type of the wind based on its speed
        """
        # Source for this data: https://en.wikipedia.org/wiki/Beaufort_scale
        wind_types = {(0, 0.5): 'Calm',
                      (0.5, 1.6): 'Light air',
                      (1.6, 3.4): 'Light breeze',
                      (3.4, 5.5): 'Gentle breeze',
                      (5.5, 8): 'Moderate breeze',
                      (8, 10.8): 'Fresh breeze',
                      (10.8, 13.9): 'Strong breeze',
                      (13.9, 17.2): 'Moderate gale',
                      (17.2, 20.8): 'Fresh gale',
                      (20.8, 24.5): 'Strong gale',
                      (2.5, 28.5): 'Whole gale',
                      (28.5, 32.7): 'Violent Storm',
                      (32.7,): 'Hurricane Force'
                      }

        for key in wind_types.keys():
            lower, upper = key
        
            if upper is None:
                return wind_types[key]
        
            if lower <= speed < upper:
                return wind_types[key]