from django.urls import path
from chat import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('<str:username>/', views.room, name="room"),
]