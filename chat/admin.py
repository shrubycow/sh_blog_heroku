from django.contrib import admin
from .models import ChatUser, ChatRoom
# Register your models here.

@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_name', 'admin')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_name')