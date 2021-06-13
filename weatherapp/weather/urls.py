from django.urls import path, include
from django.views.decorators.cache import cache_page

from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'weather'

urlpatterns = [
    path('', cache_page(60*2)(views.WeatherAPIView.as_view()), name='info')
]