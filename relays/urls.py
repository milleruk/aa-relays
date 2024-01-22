from django.urls import path

from . import views

app_name = 'relays'

urlpatterns = [
    path('', views.index, name='index'),
    path('server/<int:server>', views.server, name='server'),
    path('relays/ajax/server_messages', views.server_messages, name="server_messages"),
]
