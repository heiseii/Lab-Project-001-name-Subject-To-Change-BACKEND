import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
#from users import routing

os.environ.setdefault('DANGO_SETTINGS_MODULE', 'msj_proyect.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            #routing.web_socket_urlpatterns
        ) 
    ),
})