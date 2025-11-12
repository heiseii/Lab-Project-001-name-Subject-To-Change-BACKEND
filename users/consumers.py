from django.db import models
from channels.generic.websocket import AsyncWebsocketConsumer
from users.forms import forms
import json
from django.contrib.auth.models import User
#from .models import Message, Conversation


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.conv