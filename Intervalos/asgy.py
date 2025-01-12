import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Intervalos.routing  # Substitua 'pausas' pelo nome da sua app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intervalos.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Intervalos.routing.websocket_urlpatterns  # Definiremos isso no próximo passo
        )
    ),
})