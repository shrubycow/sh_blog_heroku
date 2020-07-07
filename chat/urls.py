from .views import index, room
from django.urls import path, re_path

app_name = "chat"

urlpatterns = [
    path('', index, name='index'),
    re_path(r'(?P<room_name>[\w]+)/(?P<is_new>[0|1])/', room, name='room'),
]
