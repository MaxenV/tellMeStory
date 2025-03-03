import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import ollama_service


class PresentView(View):
    def get(self, request, *args, **kwargs):
        if ollama_service.server_is_present():
            output = "Ollama is running"
        else:
            output = "Ollama server is not running"

        return JsonResponse({"present": output})


class ModelAllView(View):
    def get(self, request, *args, **kwargs):
        output = ollama_service.list_all_models()
        if type(output) is Exception:
            return JsonResponse({"error": output.args})
        else:
            return JsonResponse({"models": output})


class ModelRunningView(View):
    def get(self, request, *args, **kwargs):
        output = ollama_service.list_running_models()
        if type(output) is Exception:
            return JsonResponse({"error": output.args})
        else:
            return JsonResponse({"models": output})


@method_decorator(csrf_exempt, name="dispatch")
class ModelRunView(View):
    def post(self, request, *args, **kwargs):
        model = json.loads(request.body)["model"]
        output = ollama_service.run_model(model)
        if type(output) is Exception:
            return JsonResponse({"error": output.args})
        else:
            return JsonResponse({"done": output})


@method_decorator(csrf_exempt, name="dispatch")
class ModelStopView(View):
    def post(self, request, *args, **kwargs):
        model = json.loads(request.body)["model"]
        output = ollama_service.stop_model(model)
        if type(output) is Exception:
            return JsonResponse({"error": output.args})
        else:
            return JsonResponse({"done": output})


class ResponseView(View):
    def get(self, request, *args, **kwargs):
        model, content, role = self._get_request_attributes(request)
        response = ollama_service.send_request(model, content, role)
        if type(response) is Exception:
            return JsonResponse({"error": response.args})
        else:
            return JsonResponse({"response": response})

    def _get_request_attributes(self, request):
        loads = json.loads(request.body)
        if not {"model", "content"}.issubset(loads):
            return JsonResponse({"error": "Request should contain model and content"})
        model = loads["model"]
        content = loads["content"]
        role = loads["role"] if "role" in loads.keys() else None
        return model, content, role
