from django.conf import settings

from .services.ollama_api_service import OllamaApiService

# Get settings attributes
OLLAMA_BASE_URL = getattr(settings, "OLLAMA_API_URL", "http://localhost:11434")

# Services implementation
ollama_service = OllamaApiService(OLLAMA_BASE_URL)
