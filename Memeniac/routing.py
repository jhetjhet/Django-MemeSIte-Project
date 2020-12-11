from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

from main.routing import websocket_urlpatterns as main_websocket_urlpatterns
from user.routing import websocket_urlpatterns as user_websocket_urlpatterns

application = ProtocolTypeRouter({
		'websocket': AuthMiddlewareStack(
				URLRouter(
							main_websocket_urlpatterns + user_websocket_urlpatterns
					)
			),
	})