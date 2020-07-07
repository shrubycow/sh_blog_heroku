# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatUser

class ChatConsumer(WebsocketConsumer):

    users = dict()
    admins = dict()

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        if ChatConsumer.users.get(self.room_group_name) is None:
            ChatConsumer.users[self.room_group_name] = [self.user.username]
        else:
            ChatConsumer.users[self.room_group_name].append(self.user.username)
        
        # Take this room admin name
        for chat_user in ChatUser.objects.filter(room_name__name=self.room_name):
            if chat_user.admin:
                ChatConsumer.admins[self.room_group_name] = chat_user.user.username

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # Send usernames to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_users',
                'users': ChatConsumer.users[self.room_group_name],
                'admin': ChatConsumer.admins[self.room_group_name]
            }
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        ChatConsumer.users[self.room_group_name].remove(self.user.username)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_users',
                'users': ChatConsumer.users[self.room_group_name]
            }
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Send delete room message to room group
        if text_data_json.get('delete') != None and self.user.username == ChatConsumer.admins[self.room_group_name]:
            delete = text_data_json['delete']
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_delete',
                'delete': delete
            }
            )
        elif text_data_json.get('message') != None:
            message = text_data_json['message']

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user
            
        }))

    # Receive usernames from room group
    def chat_users(self, event):
        users = event['users']
        admin = event['admin']
        
        # Send usernames to WebSocket
        self.send(text_data=json.dumps({
            'users': users,
            'admin': admin
        }))

    # Receive delete chat command from room group
    def chat_delete(self, event):
        delete = event['delete']

        self.send(text_data=json.dumps({
            'delete': delete
        }))