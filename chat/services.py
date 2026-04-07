# chat/services.py
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    """Service to handle Google Gemini AI interactions"""
    
    def __init__(self):
        """Initialize Gemini with API key and configuration"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            self.generation_config = {
                'temperature': settings.GEMINI_CONFIG.get('temperature', 0.7),
                'max_output_tokens': settings.GEMINI_CONFIG.get('max_output_tokens', 2048),
                'top_p': settings.GEMINI_CONFIG.get('top_p', 0.95),
                'top_k': settings.GEMINI_CONFIG.get('top_k', 40),
            }
            self.available = True
            logger.info("✅ Gemini AI service initialized successfully")
        except Exception as e:
            self.available = False
            logger.error(f"Failed to initialize Gemini: {str(e)}")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate AI response using Gemini
        
        Args:
            message: Current user message
            conversation_history: List of previous messages (optional)
        
        Returns:
            str: AI response text
        """
        if not self.available:
            return "AI service is currently unavailable. Please try again later."
        
        try:
            # Build context from conversation history
            if conversation_history:
                # Format conversation history for context
                context = []
                for msg in conversation_history:
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    context.append(f"{role}: {msg['content']}")
                context.append(f"User: {message}")
                prompt = "\n".join(context)
            else:
                prompt = message
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return response.text
        
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)[:100]}"

# Create a singleton instance
gemini_service = GeminiService()