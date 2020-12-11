from django.urls import path

from .consumers import UserUpdatesConsumer

websocket_urlpatterns = [
	path('ws/userupdates/', UserUpdatesConsumer),
]