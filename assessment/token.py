from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from typing import Any


@database_sync_to_async
def get_user(scope):
    try:
        token_string = parse_qs(scope["query_string"].decode("utf-8"))["token"][0]
        token = Token.objects.get(key=token_string)
        return token.user
    except (KeyError, Token.DoesNotExist):
        return AnonymousUser


class TokenMiddlewareInstance:
    def __init__(self, scope, middleware) -> None:
        self.scope = dict(scope)
        self.inner = middleware.inner
    
    async def __call__(self, receive, send) -> Any:
        self.scope["user"] = await get_user(self.scope)
        # inner = self.inner(self.scope)
        return await self.inner(self.scope, receive, send)


class TokenAuthMiddleware:
    def __init__(self, inner) -> None:
        self.inner = inner
    
    def __call__(self, scope) -> TokenMiddlewareInstance:
        return TokenMiddlewareInstance(scope, self)
