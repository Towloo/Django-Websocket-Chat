from urllib.parse import parse_qs
from django.contrib.auth import login
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from chat.models import Thread
from chat.serializers import LoginSerializer


def room(req, username):
    try:
        token = parse_qs(req.scope["query_string"].decode("utf-8"))["token"][0]
        token = Token.objects.get(key=token)
        user = User.objects.get(username=username)
        if user and token and token.user != user:
            thread = Thread.objects.get_or_create_thread(token.user, user)
            return render(req, "room.html", {
                "destination": user,
                "source": token.user,
                "messages": thread.message_set.all()
            })
    except Exception as e:
        print(e)
        pass
    return redirect("login")


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, req):
        serializer = LoginSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validate(req.data)["user"]
        login(req, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token":token.key
        }, status=200)
