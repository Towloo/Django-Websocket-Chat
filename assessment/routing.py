from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from assessment.token import TokenAuthMiddleware
from chat import routing

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    )
})