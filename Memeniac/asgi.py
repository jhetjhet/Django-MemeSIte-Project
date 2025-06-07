"""
ASGI config for Memeniac project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Memeniac.settings')

django_asgi_app  = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from main.routing import websocket_urlpatterns as main_websocket_urlpatterns
from user.routing import websocket_urlpatterns as user_websocket_urlpatterns

application = ProtocolTypeRouter({
	'http': django_asgi_app ,  # Django's ASGI application will handle HTTP requests
	'websocket': AuthMiddlewareStack(
			URLRouter(
						main_websocket_urlpatterns + user_websocket_urlpatterns
				)
		),
})