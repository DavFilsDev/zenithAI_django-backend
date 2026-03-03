from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
import openai
import os
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

class ConversationListView(generics.ListCreateAPIView):
    """
    List all conversations or create a new one for the authenticated user.
    
    **GET**: Returns a list of all conversations belonging to the current user.
    - Ordered by most recently updated (newest first)
    - Includes message count for each conversation
    
    **POST**: Creates a new conversation with the provided title.
    - The conversation is automatically associated with the current user
    - Returns the created conversation with id and timestamps
    """
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        """Filter conversations to only show the current user's conversations"""
        return Conversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a new conversation"""
        serializer.save(user=self.request.user)
    
    @extend_schema(
        summary="List all conversations",
        description="Retrieve all conversations for the authenticated user, ordered by most recent",
        responses={
            200: OpenApiResponse(
                response=ConversationSerializer(many=True),
                description="List of conversations retrieved successfully"
            ),
            401: OpenApiResponse(
                description="Authentication credentials not provided or invalid"
            ),
        },
        examples=[
            OpenApiExample(
                'Successful Response',
                value=[
                    {
                        'id': 1,
                        'title': 'My First Conversation',
                        'created_at': '2026-03-03T10:00:00Z',
                        'updated_at': '2026-03-03T10:00:00Z',
                        'message_count': 0,
                        'messages': []
                    }
                ],
                response_only=True,
            ),
        ],
        tags=['Chat']
    )
    def get(self, request, *args, **kwargs):
        """List user's conversations"""
        return self.list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new conversation",
        description="Create a new conversation with the specified title",
        request=ConversationSerializer,
        responses={
            201: OpenApiResponse(
                response=ConversationSerializer,
                description="Conversation created successfully"
            ),
            400: OpenApiResponse(
                description="Invalid data provided (e.g., missing title)"
            ),
            401: OpenApiResponse(
                description="Authentication required"
            ),
        },
        examples=[
            OpenApiExample(
                'Create Request',
                value={
                    'title': 'My New Conversation'
                },
                request_only=True,
            ),
            OpenApiExample(
                'Create Response',
                value={
                    'id': 1,
                    'title': 'My New Conversation',
                    'created_at': '2026-03-03T10:00:00Z',
                    'updated_at': '2026-03-03T10:00:00Z',
                    'message_count': 0,
                    'messages': []
                },
                response_only=True,
            ),
        ],
        tags=['Chat']
    )
    def post(self, request, *args, **kwargs):
        """Create a new conversation"""
        return self.create(request, *args, **kwargs)

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific conversation.
    
    **GET**: Returns the conversation with all its messages.
    - Messages are ordered chronologically
    - Includes message count and full message history
    
    **PUT/PATCH**: Update the conversation title.
    
    **DELETE**: Delete the conversation and all its messages.
    
    Note: Users can only access their own conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        """Ensure users can only access their own conversations"""
        return Conversation.objects.filter(user=self.request.user)
    
    @extend_schema(
        summary="Get conversation details",
        description="Retrieve a specific conversation with all its messages",
        responses={
            200: OpenApiResponse(
                response=ConversationSerializer,
                description="Conversation details retrieved successfully"
            ),
            401: OpenApiResponse(
                description="Authentication required"
            ),
            403: OpenApiResponse(
                description="You don't have permission to access this conversation"
            ),
            404: OpenApiResponse(
                description="Conversation not found"
            ),
        },
        examples=[
            OpenApiExample(
                'Successful Response',
                value={
                    'id': 1,
                    'title': 'My First Conversation',
                    'created_at': '2026-03-03T10:00:00Z',
                    'updated_at': '2026-03-03T10:06:00Z',
                    'message_count': 2,
                    'messages': [
                        {
                            'id': 1,
                            'role': 'user',
                            'content': 'What is Django?',
                            'tokens': 0,
                            'created_at': '2026-03-03T10:04:00Z'
                        },
                        {
                            'id': 2,
                            'role': 'assistant',
                            'content': 'Django is a Python web framework...',
                            'tokens': 0,
                            'created_at': '2026-03-03T10:04:01Z'
                        }
                    ]
                },
                response_only=True,
            ),
        ],
        tags=['Chat']
    )
    def get(self, request, *args, **kwargs):
        """Get conversation details"""
        return self.retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update conversation",
        description="Update the title of a conversation",
        request=ConversationSerializer,
        responses={
            200: ConversationSerializer,
            400: OpenApiResponse(description="Invalid data"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied"),
            404: OpenApiResponse(description="Conversation not found"),
        },
        examples=[
            OpenApiExample(
                'Update Request',
                value={
                    'title': 'Updated Conversation Title'
                },
                request_only=True,
            ),
        ],
        tags=['Chat']
    )
    def put(self, request, *args, **kwargs):
        """Update conversation title"""
        return self.update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete conversation",
        description="Delete a conversation and all its messages",
        responses={
            204: OpenApiResponse(
                description="Conversation deleted successfully"
            ),
            401: OpenApiResponse(
                description="Authentication required"
            ),
            403: OpenApiResponse(
                description="Permission denied"
            ),
            404: OpenApiResponse(
                description="Conversation not found"
            ),
        },
        tags=['Chat']
    )
    def delete(self, request, *args, **kwargs):
        """Delete conversation"""
        return self.destroy(request, *args, **kwargs)

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