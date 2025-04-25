from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.generativeai as genai
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Gemini API key configuration
GENAI_API_KEY = "AIzaSyDLsN1tJQWw00Eh57Rnw_tLLH5VfN5DFkk"
genai.configure(api_key=GENAI_API_KEY)
chat_model = genai.GenerativeModel("gemini-1.5-flash")

@api_view(['POST'])
def get_chat_dataWEB(request):
    user_input = request.data.get("message", "").strip()
    
    if not user_input:
        return Response({"error": "Message is required"}, status=400)

    try:
        # Let Gemini generate a response directly
        prompt = f"""You are a helpful assistant. Answer the following question:

User's Question:
{user_input}

Answer:"""

        response = chat_model.generate_content(prompt)
        answer = getattr(response, 'text', str(response))

        return Response({"response": answer})
    
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return Response({"error": "Something went wrong while processing your request."}, status=500)
