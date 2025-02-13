import json
from datetime import datetime

import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.dto.ModelListDTO import ModelListDTO


class PresentView(View):
    def get(self, request, *args, **kwargs):
        output = "Unknown error"
        try:
            response = requests.get("http://localhost:22545", json={})
            output = response.text
        except requests.exceptions.RequestException as e:
            print(e)
            output = "Ollama server is not running"
        return JsonResponse({"present": output})


class ModelAllView(View):
    def get(self, request, *args, **kwargs):
        response = requests.get("http://127.0.0.1:22545/api/tags", json={})
        output = ModelListDTO(models=response.json())
        return JsonResponse({"models": list(output)})


class ModelRunningView(View):
    def get(self, request, *args, **kwargs):
        response = requests.get("http://127.0.0.1:22545/api/ps", json={})
        output = ModelListDTO(models=response.json())
        return JsonResponse({"models": list(output)})


@method_decorator(csrf_exempt, name="dispatch")
class ModelRunView(View):
    def post(self, request, *args, **kwargs):
        model = json.loads(request.body)["model"]
        print()
        print(request.POST)
        response = requests.post(
            "http://127.0.0.1:22545/api/generate", json={"model": model}
        )
        return JsonResponse({"result": response.json()})


@method_decorator(csrf_exempt, name="dispatch")
class ModelStopView(View):
    def post(self, request, *args, **kwargs):
        model = json.loads(request.body)["model"]
        print()
        print(request.POST)
        response = requests.post(
            "http://127.0.0.1:22545/api/generate",
            json={"model": model, "keep_alive": 0},
        )
        return JsonResponse({"result": response.json()})


class ResponseView(View):
    def get(self, request, *args, **kwargs):
        role = request.GET.get("role")
        content = request.GET.get("content")
        response = requests.get(
            "http://127.0.0.1:22545/response", json={"role": role, "content": content}
        )
        return JsonResponse({"message": response.json(), "time": datetime.now()})
