import requests
from api.dto.ModelListDTO import ModelListDTO


class OllamaApiService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.role = "user"

    def server_is_present(self):
        try:
            response = requests.get(self.base_url, json={})
            if response.text == "Ollama is running":
                return response.text
            else:
                return Exception("Ollama server is not running")
        except requests.exceptions.RequestException:
            return Exception("Connection error")

    def list_all_models(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            output = ModelListDTO(models=response.json())
            return list(output)
        except requests.exceptions.RequestException:
            return Exception("Connection error")

    def list_running_models(self):
        try:
            response = requests.get(f"{self.base_url}/api/ps")
            output = ModelListDTO(models=response.json())
            return list(output)
        except requests.exceptions.RequestException:
            return Exception("Connection error")

    def run_model(self, model_name):
        try:
            models_list = self.list_all_models()
            if type(models_list) is Exception:
                return models_list

            model_names = list(map(lambda model: model["name"], models_list))
            if model_name in model_names:
                response = requests.post(
                    f"{self.base_url}/api/generate", json={"model": model_name}
                )
                return response.json().get("done")
            else:
                return Exception("No model with this name")
        except requests.exceptions.RequestException:
            return Exception("Connection error")

    def stop_model(self, model_name):
        try:
            if model_name in map(
                lambda model_obj: model_obj["name"], self.list_running_models()
            ):
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={"model": model_name, "keep_alive": 0},
                )
                return response.json().get("done")
            else:
                return Exception("No model with this name")
        except requests.exceptions.RequestException:
            return Exception("Connection error")

    def send_request(self, model_name, content, role=None):
        try:
            if role is None:
                role = self.role
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model_name,
                    "stream": False,
                    "messages": [{"role": "user", "content": content}],
                },
            )
            response = response.json()
            if response.get("done") is True:
                return response
            else:
                return Exception("Chat response error")
        except requests.exceptions.RequestException as e:
            return Exception("Connection error")
