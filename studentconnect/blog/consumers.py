import logging  
logger = logging.getLogger(__name__)  
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Class view for connect the ws connctions of the users 
    """
    async def connect(self):
        """
        The async funtion will make the connection between the user
        """
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
        """
        The async funtion will close the connection between the user
        """
        # Leave the user-specific channel group
        await self.channel_layer.group_discard(
            self.user_channel_name,
            self.channel_name
        )

    async def send_notification(self, event):
        """
        Fucntion for sending the info about the post and the user name that the post liked 
        """
        # Send the WebSocket notification to the client
        logger.info("WebSocket notifications established")
        message = event['notification']
        blog_creator_id = event.get('blog_creator_id')
        await self.send(text_data=json.dumps({'notification': message}))


class ActiveUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('active_user_channel', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when the websocket disconnects
        await self.channel_layer.group_discard('active_user_channel', self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    async def broadcast_active_users(self, event):
        logger.info("WebSocket data active users are established")
        data = event['data']
        logger.info(f"WebSocket data received: {data}")
        await self.send(text_data=json.dumps(data))

