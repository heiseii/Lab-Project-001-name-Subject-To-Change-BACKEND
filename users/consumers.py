from django.db import models
from channels.generic.websocket import AsyncWebsocketConsumer
from users.forms import forms
import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Message
#from .models import Message, Conversation


class ChatConsumer(AsyncWebsocketConsumer):

    #Funcion de Conectar    

    async def connect(self):
        
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    #Funcion de desconectar

    async def disconnect(self, close_code):
        await self.channel.layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        
    #Funcion de recibir mensajes

    async def receive(self, text_data):
        data = json.data(text_data)
        message_content = data['message']
        sender_id = data['sender_id']

        message = await self.save_message(sender_id, message_content) #--> Guarda en la db el mensaje

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender_id': sender_id,
                'sender_username': message['sender_username'],
                'timestamp': message['timestamp']
            }
        )       
#@database_sync_to_async
    async def chat_message(self, event):
        await self.send (text_data=json.dumps({
            'message': event['message'],
            'self_id': event['self_id'],
            'sender_username': event['sender_username'],
            'timestamp': event['timestamp'],
    }))


    def save_message(self, sender_id, content):
        sender = User.objects.get(id=sender_id)
        conversation = User.objecs.get(id=self.conversation_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content
        )
        
        return {
            'sender_username': sender.username,
            'timestamp': message.timestamp.isoformat()
        }