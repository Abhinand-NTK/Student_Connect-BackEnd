# # views.py
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from .models import Message
# from superadmin.models import UserAccount
# from rest_framework.permissions import IsAuthenticated
# from .serializers import MessageSerializer
# class SendMessageView(ModelViewSet):
#     """
#     Class for the sending the messages
#     """
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         """
#         Funtion for creating the messages
#         """
#         sender = request.user
#         print(request.data)
#         receiver_username = request.data.get('receiver')
#         message_text = request.data.get('message')

#         # Get the receiver
#         receiver = UserAccount.objects.get(id=receiver_username)


#         # Create the message instance
#         chat_message = Message.objects.create(sender=sender, receiver=receiver, content=message_text)

#         # Send the message to the specific user's WebSocket
#         user_channel_name = f"user_{receiver.id}"
#         channel_layer = get_channel_layer()

#         async_to_sync(channel_layer.group_send)(
#             user_channel_name,
#             {
#                 "type": "chat.message",
#                 "message": chat_message.content,
#             },
#         )

#         return Response({"status": "success"}, status=status.HTTP_201_CREATED)


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message
from superadmin.models import UserAccount
from superadmin.serializer import UserDetailsSerilzer
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer


class SendMessageView(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        sender = request.user
        receiver_username = request.data.get('receiver')
        message_text = request.data.get('content')

        try:
            receiver = UserAccount.objects.get(id=receiver_username)
        except UserAccount.DoesNotExist:
            return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)

        receiver = UserAccount.objects.get(id=receiver_username)

        chat_message = Message.objects.create(
            sender=sender, receiver=receiver, content=message_text)

        user_channel_name = f"user_{receiver.id}"
        channel_layer = get_channel_layer()

        # Serialize the UserAccount instance
        serilizer = MessageSerializer(chat_message)

        print(serilizer.data, "This is the output ____-")

        async_to_sync(channel_layer.group_send)(
            user_channel_name,
            {
                "type": "chat.message",
                "content": chat_message.content,
                "sender": serilizer.data['sender'],
                "receiver": serilizer.data['receiver'],
                "timestamp": serilizer.data['timestamp'],
            },
        )

        # async_to_sync(channel_layer.group_send)(
        #     user_channel_name,
        #     {
        #         "type": "chat.message",
        #         "message": chat_message.content,
        #         "sender": chat_message.sender,
        #         "receiver": chat_message.receiver,
        #     },
        # )

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        """
        receiver_id = request.GET.get('reciver_id')
        sender_id = request.user.id

        if not receiver_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = UserAccount.objects.get(id=receiver_id)
        except UserAccount.DoesNotExist:
            return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)


        messages = Message.objects.filter(
            sender=sender_id, receiver=receiver_id)
        messagess = Message.objects.filter(
            sender=receiver_id, receiver=sender_id)
        combined_messages = messages | messagess
        sorted_messages = sorted(
            combined_messages,
            # Assuming 'timestamp' is a field in your Message model
            key=lambda message: message.timestamp
        )

        serilizer = self.get_serializer(sorted_messages, many=True)
        serilizer_2 = self.get_serializer(messagess, many=True)

        combined_data = {
            'messages': serilizer.data,
            'messagess': serilizer_2.data,
        }

        return Response(serilizer.data, status=status.HTTP_200_OK)


class Connections(ModelViewSet):
    """
    View for showing the connections
    """
    queryset = UserAccount.objects.all()
    serializer_class = UserDetailsSerilzer
    permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        """
        Funtion for retrive the connection based on the message history
        """

        user_id = request.user.id

        # message_history = Message.objects.filter(sender=request.user.id or receiver =request.user.id)
        message_history = Message.objects.filter(sender=request.user.id) | Message.objects.filter(receiver=request.user.id)

        print(message_history)

        receiver_ids = message_history.values_list('receiver', flat=True).distinct()
        sender_ids = message_history.values_list('sender', flat=True).distinct()
        connections_ids = receiver_ids.union(sender_ids)


        connections= UserAccount.objects.filter(id__in = connections_ids)
        serilizer = self.get_serializer(connections,many=True)
        return Response(serilizer.data,status=status.HTTP_200_OK)
