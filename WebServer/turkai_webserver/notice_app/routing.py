# chat/routing.py
from django.urls import re_path

from .websocket_consumer import PersonDataConsumer

websocket_urlpatterns = [
    re_path(r"^ws/interpol_data_stream/$", PersonDataConsumer.as_asgi()),]