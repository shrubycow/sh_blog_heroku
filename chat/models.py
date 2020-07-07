from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    
    name = models.CharField(max_length=250)
    group_name = models.CharField(max_length=255)


    class Meta:
        verbose_name = "chat room"
        verbose_name_plural = "chat rooms"

    def __str__(self):
        return self.name

class ChatUser(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    room_name = models.ForeignKey(ChatRoom, verbose_name="Наименование чата", on_delete=models.CASCADE)
    admin = models.BooleanField()
