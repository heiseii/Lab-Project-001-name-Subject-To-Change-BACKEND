from django.db import models
from channels.generic.websocket import AsyncWebsocketConsumer
from users.forms import forms
import json


class SimpleChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        