from django.shortcuts import render
from django.views import View


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "home.html", context)


class ChatPageView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "index.html", context)
