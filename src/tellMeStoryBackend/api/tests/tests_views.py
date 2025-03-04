import json
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse


class ApiPresentTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("api.views.ollama_service.server_is_present")
    def test_present_positive(self, mock_server_is_present):
        mock_server_is_present.return_value = "Ollama is running"
        response = self.client.get(reverse("present"))
        self.assertJSONEqual(response.content, {"present": "Ollama is running"})

    @patch("api.views.ollama_service.server_is_present")
    def test_present_exception(self, mock_server_is_present):
        mock_server_is_present.return_value = Exception("Connection error")
        response = self.client.get(reverse("present"))
        self.assertJSONEqual(response.content, {"error": ["Connection error"]})


class ApiListAllModelsTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("api.views.ollama_service.list_all_models")
    def test_all_models_positive(self, mock_list_all_models):
        mock_list_all_models.return_value = [{"name": "llama3.2:3b", "size": "2.02 GB"}]
        response = self.client.get(reverse("model_all"))
        self.assertJSONEqual(
            response.content,
            {"models": [{"name": "llama3.2:3b", "size": "2.02 GB"}]},
        )

    @patch("api.views.ollama_service.list_all_models")
    def test_connection_exception(self, mock_list_all_models):
        mock_list_all_models.return_value = Exception("Connection error")
        response = self.client.get(reverse("model_all"))
        self.assertJSONEqual(response.content, {"error": ["Connection error"]})


class ApiListRunningModelsTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("api.views.ollama_service.list_running_models")
    def test_model_running_positive(self, mock_list_running_models):
        mock_list_running_models.return_value = [
            {"name": "llama3.2:3b", "size": "2.02 GB"}
        ]
        response = self.client.get(reverse("model_running"))
        self.assertJSONEqual(
            response.content,
            {"models": [{"name": "llama3.2:3b", "size": "2.02 GB"}]},
        )

    @patch("api.views.ollama_service.list_running_models")
    def test_model_running_exception(self, mock_list_running_models):
        mock_list_running_models.return_value = Exception("Connection error")
        response = self.client.get(reverse("model_running"))
        self.assertJSONEqual(response.content, {"error": ["Connection error"]})


class ApiRunModelTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("api.views.ollama_service.run_model")
    def test_model_run_positive(self, mock_run_model):
        mock_run_model.return_value = True
        response = self.client.post(
            reverse("model_run"),
            data=json.dumps({"model": "llama3.2:3b"}),
            content_type="application/json",
        )
        self.assertJSONEqual(response.content, {"done": True})

    @patch("api.views.ollama_service.run_model")
    def test_model_run_exception(self, mock_list_running_models):
        mock_list_running_models.return_value = Exception("Connection error")
        response = self.client.post(
            reverse("model_run"),
            data=json.dumps({"model": "llama3.2:3b"}),
            content_type="application/json",
        )
        self.assertJSONEqual(response.content, {"error": ["Connection error"]})


class ApiStopModelTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("api.views.ollama_service.stop_model")
    def test_model_stop_positive(self, mock_stop_model):
        mock_stop_model.return_value = True
        response = self.client.post(
            reverse("model_stop"),
            data=json.dumps({"model": "llama3.2:3b"}),
            content_type="application/json",
        )
        self.assertJSONEqual(response.content, {"done": True})

    @patch("api.views.ollama_service.stop_model")
    def test_model_stop_exception(self, mock_stop_model):
        mock_stop_model.return_value = Exception("Connection error")
        response = self.client.post(
            reverse("model_stop"),
            data=json.dumps({"model": "llama3.2:3b"}),
            content_type="application/json",
        )
        self.assertJSONEqual(response.content, {"error": ["Connection error"]})


class ApiResponseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_model_response_value = {
            "model": "llama3.2:3b",
            "created_at": "2025-03-03T22:00:45.546535516Z",
            "message": {
                "role": "assistant",
                "content": "Blue sky response.",
            },
            "done_reason": "stop",
            "done": True,
            "total_duration": 2039091606,
            "load_duration": 1467806492,
            "prompt_eval_count": 34,
            "prompt_eval_duration": 116000000,
            "eval_count": 44,
            "eval_duration": 453000000,
        }
        self.view_response_value = {
            "response": {
                "model": "llama3.2:3b",
                "created_at": "2025-03-03T22:00:45.546535516Z",
                "message": {
                    "role": "assistant",
                    "content": "Blue sky response.",
                },
                "done_reason": "stop",
                "done": True,
                "total_duration": 2039091606,
                "load_duration": 1467806492,
                "prompt_eval_count": 34,
                "prompt_eval_duration": 116000000,
                "eval_count": 44,
                "eval_duration": 453000000,
            }
        }

    @patch("api.views.ollama_service.send_request")
    def test_all_request_info(self, mock_model_response):
        mock_model_response.return_value = self.mock_model_response_value
        response = self.client.get(
            reverse("response"),
            {"model": "llama3.2:3b", "content": "Blue sky question", "role": "user"},
        )
        self.assertJSONEqual(response.content, self.view_response_value)

    @patch("api.views.ollama_service.send_request")
    def test_no_role(self, mock_model_response):
        mock_model_response.return_value = self.mock_model_response_value
        response = self.client.get(
            reverse("response"),
            {"model": "llama3.2:3b", "content": "Blue sky question"},
        )
        self.assertJSONEqual(response.content, self.view_response_value)

    @patch("api.views.ollama_service.send_request")
    def test_no_content(self, mock_model_response):
        mock_model_response.return_value = self.mock_model_response_value
        response = self.client.get(
            reverse("response"),
            {"model": "llama3.2:3b", "role": "user"},
        )
        self.assertJSONEqual(
            response.content, {"error": "Request should contain model and content"}
        )
