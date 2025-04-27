import json

import requests
from django.shortcuts import render
from django.views import View


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        try:
            print("hello")
            response = requests.get("http://localhost:8000/api/model/all")
            response.raise_for_status()
            if response.content:
                content = response.json()
                model_names = [name["name"] for name in content["models"]]
                context = {
                    "status": response.status_code,
                    "model_names": model_names,
                }
            else:
                context = {
                    "status": 502,
                    "message": "Received empty response from the server.",
                }

        except requests.exceptions.ConnectionError:
            context = {
                "status": 503,
                "message": "A connection error occurred. Please check your internet connection.",
            }
        except requests.exceptions.Timeout:
            context = {
                "status": 504,
                "message": "The request timed out.",
            }
        except requests.exceptions.HTTPError as e:
            context = {
                "status": response.status_code,
                "message": f"HTTP Error: {e.response.status_code}",
            }
        except requests.exceptions.RequestException:
            context = {
                "status": 500,
                "message": "An RequestException error occurred",
            }
        except json.JSONDecodeError:
            context = {
                "status": 502,
                "message": "Failed to decode JSON response.",
            }
        except Exception:
            context = {
                "status": 500,
                "message": "An unknown error occurred",
            }

        finally:
            return render(request, "home.html", context)


class ChatPageView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "index.html", context)
