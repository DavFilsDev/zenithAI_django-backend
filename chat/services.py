# chat/services.py
from google import genai
from google.genai import types
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    """Service to handle Google Gemini AI interactions using new genai package"""
    
    # Available models with correct paths
    AVAILABLE_MODELS = {
        'gemini-2.0-flash-exp': 'gemini-2.0-flash-exp',
        'gemini-1.5-flash': 'gemini-1.5-flash',
        'gemini-1.5-pro': 'gemini-1.5-pro',
    }
    
    def __init__(self):
        """Initialize Gemini with API key and configuration"""
        try:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self.model_name = settings.GEMINI_MODEL
            self.available = True
            logger.info(f"✅ Gemini AI service initialized with model: {self.model_name}")
            
            # Test the connection
            self._test_connection()
            
        except Exception as e:
            self.available = False
            logger.error(f"❌ Failed to initialize Gemini: {str(e)}")
    
    def _test_connection(self):
        """Test if the model is accessible"""
        try:
            # Simple test prompt
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Test",
                config=types.GenerateContentConfig(
                    max_output_tokens=5,
                )
            )
            logger.info(f"✅ Connection test successful with model: {self.model_name}")
        except Exception as e:
            logger.warning(f"⚠️ Model test failed: {str(e)}")
    
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
            return "⚠️ AI service is currently unavailable. Please try again later."
        
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
            
            logger.info(f"Generating response with model: {self.model_name}")
            
            # Generate response using the client
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.GEMINI_CONFIG.get('temperature', 0.7),
                    max_output_tokens=settings.GEMINI_CONFIG.get('max_output_tokens', 2048),
                    top_p=settings.GEMINI_CONFIG.get('top_p', 0.95),
                    top_k=settings.GEMINI_CONFIG.get('top_k', 40),
                )
            )
            
            return response.text
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Gemini API error: {error_msg}")
            
            # Provide helpful error messages
            if "404" in error_msg:
                return f"⚠️ Model '{self.model_name}' not accessible. Try using 'gemini-1.5-flash' instead."
            elif "API key" in error_msg or "403" in error_msg:
                return "⚠️ Invalid API key. Please check your GEMINI_API_KEY setting."
            else:
                return f"⚠️ Sorry, I encountered an error: {error_msg[:150]}"

# Create a singleton instance
gemini_service = GeminiService()