import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *

class TextRoomConsumer(WebsocketConsumer):
    def connect(self):
        print('reached the consumer ------------------------------------------------------ ')

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        print('message reached  ------------------------------------------------------ ')
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender = text_data_json['sender']

        family_id = text_data_json.get('room_id')

        # Save the message to the Message model
        if family_id:
            family = Families.objects.get(pk=family_id)
            Message.objects.create(
                family=family,
                sender=sender,
                text=text
            )
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text,
                'sender': sender
            }
        )

    def chat_message(self, event):
        # Receive message from room group
        text = event['message']
        sender = event['sender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': text,
            'sender': sender
        }))