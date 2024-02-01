

import logging  

logger = logging.getLogger(__name__)  
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract user ID from the channel name (e.g., 'user_123')
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        # self.user_channel_name = f'user_{user_id}'
        print(self.user_id)
        logger.info("WebSocket notifications established for user %s", self.user_id)

        # logger.info("WebSocket notifications established", self.user_id)
        self.user_channel_name = f'user_{self.user_id}'

        # Join the user-specific channel group
        await self.channel_layer.group_add(
            self.user_channel_name,
            self.channel_name
        )
        

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the user-specific channel group
        await self.channel_layer.group_discard(
            self.user_channel_name,
            self.channel_name
        )

    async def send_notification(self, event):
        # Send the WebSocket notification to the client
        logger.info("WebSocket notifications established")
        message = event['notification']
        blog_creator_id = event.get('blog_creator_id')
        
        # if blog_creator_id == self.user_id:
        await self.send(text_data=json.dumps({'notification': message}))
