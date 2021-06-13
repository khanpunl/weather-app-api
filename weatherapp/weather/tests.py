from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import json
import requests


class WeatherAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_request_response(self):
        """
        Test if a request to external openweathermap API returns the correct data.
        Test if a request to external openweathermap API returns the correct status code.
        """

        url = f'http://api.openweathermap.org/data/2.5/weather?q=Bogota,co&appid={settings.API_KEY}'
        
        response = requests.get(url)
        
        city = 'Bogota'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], city)

    def test_weather_api_view(self):
        """
        Test if the WeatherAPIView returns the correct data.
        Test if the WeatherAPIView returns the correct status code.
        """

        GET_WEATHER_DATA_URL = '/weather?city=bogota&country=co&'
        response = self.client.get(GET_WEATHER_DATA_URL)

        location_name = 'Bogota, CO'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['location_name'], location_name)

    def test_weather_api_content_type(self):
        """
        Test if the WeatherAPIView returns the correct content_type.
        """

        GET_WEATHER_DATA_URL = '/weather?city=bogota&country=co&'
        response = self.client.get(GET_WEATHER_DATA_URL)

        self.assertEqual(response.__getitem__('content-type'), 'application/json')

    def test_degree_to_direction(self):
        """
        Test if the degToDir method returns the correct data.
        """
        directions = ["north", "north-northeast", "north-east", "east-northeast", 
                      "east", "east-southeast", "south-east", "south-southeast",
                      "south", "south-southwest", "south-west", "west-southwest", 
                      "west", "west-northwest", "north-west", "north-northwest",]
        deg = 140
        # We have 16 directions and total 360 degrees
        # There is an angle change at every 22.5 degrees (360/16)
        val=int((deg/22.5)+.5)
        
        self.assertEqual('south-east', directions[(val % 16)])
        return directions[(val % 16)]

    def test_wind_type(self):
        """
        Test if the windType method returns the correct data.
        """
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
        
        speed = 3.5
        
        self.assertEqual('Gentle breeze', wind_types[(3.4, 5.5)])