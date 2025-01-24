from django.shortcuts import render
from django.views import View


class ChatPageView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "index.html", context)
