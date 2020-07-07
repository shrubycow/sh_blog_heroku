from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.template import loader
from .models import ChatRoom, ChatUser
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

# Create your views here.
def index(request):
    rooms = ChatRoom.objects.values_list('name', flat=True)
    return render(request, 'chat/index.html', {'rooms': rooms})
    

def room(request, room_name, is_new):
    if int(is_new):
        try:
            ChatRoom.objects.get(name=room_name)
            response = render(request, "chat/403.html", {'message': 'Room already exist'})
            response.status_code = 403
            return response
        except ObjectDoesNotExist:
            new_chat_room = ChatRoom.objects.create(name=room_name, group_name="chat_"+room_name)
            ChatUser.objects.create(user=request.user, room_name=new_chat_room, admin=True)
    else:
        room = ChatUser.objects.filter(room_name__name=room_name)
        if len(room)==0:
            response = render(request, "chat/403.html", {'message': 'This room does not exist'})
            response.status_code = 403
            return response
        try:
            room.get(user=request.user)
        except ObjectDoesNotExist:
            response = render(request, "chat/403.html", {'message': 'You have not permission to access'})
            response.status_code = 403
            return response
            
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
