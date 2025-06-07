from django.urls import path

from .consumers import PostUpdateConsumer

websocket_urlpatterns = [
	path('ws/postupdates/', PostUpdateConsumer),
]