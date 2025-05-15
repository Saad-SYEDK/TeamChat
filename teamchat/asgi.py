import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamchat.settings')

application = get_asgi_application()

# Import routing after settings and application are ready
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
