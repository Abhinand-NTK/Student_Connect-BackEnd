# # consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message_type = text_data_json.get('type')

#         if message_type == 'chat':
#             await self.handle_chat_message(text_data_json)

#     async def handle_chat_message(self, data):
#         message = data.get('message')

#         # Send the message to the connected client
#         await self.send(text_data=json.dumps({"message": message}))


import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging  
logger = logging.getLogger(__name__)  

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"user_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        logger.info(self.room_name)


        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        logger.info("WebSocket data active users are established")

        # message = event['message']
        # sender = event['sender']
        # receiver = event['receiver']
        

        # await self.send(text_data=json.dumps({
        #     'message': message,
        #     'sender': sender,
        #     'receiver': receiver,
        # }))


        content = event.get('content', '')
        sender = event.get('sender', '')
        receiver = event.get('receiver', '')
        timestamp = event.get('timestamp', '')

        await self.send(text_data=json.dumps({
            'content': content,
            'sender': sender,
            'receiver': receiver,
            'timestamp': timestamp,
        }))
        
    # async def chat_message(self, event):

    #     logger.info("WebSocket data active users are established")

    #     message = event['message']
    #     sender = event['sender']
    #     receiver = event['receiver']

    #     logger.info("WebSocket data active users are established")


    #     # Send the message to the WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'sender': sender,
    #         'receiver': receiver,
    #     }))
