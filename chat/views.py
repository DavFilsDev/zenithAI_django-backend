from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
import openai
import os

class ConversationListView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

class ChatView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, conversation_id=None):
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create conversation
        if conversation_id:
            conversation = Conversation.objects.filter(
                id=conversation_id, 
                user=request.user
            ).first()
            if not conversation:
                return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Create new conversation with first message as title
            title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            conversation = Conversation.objects.create(
                user=request.user,
                title=title
            )
        
        # Save user message
        user_msg = Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        try:
            # Get conversation history
            messages = Message.objects.filter(conversation=conversation)
            chat_history = [{'role': msg.role, 'content': msg.content} for msg in messages]
            
            # Here you would integrate with OpenAI API
            # For now, we'll simulate a response
            ai_response = "This is a simulated response. Integrate with OpenAI API for real responses."
            
            # Save AI response
            ai_msg = Message.objects.create(
                conversation=conversation,
                role='assistant',
                content=ai_response
            )
            
            serializer = MessageSerializer(ai_msg)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)