import json

import requests
from django.shortcuts import render
from django.views import View

from frontend.views.views import MainView


class RegisterView(View):
    template_name = 'frontend/register.html'
    authorized_name = 'frontend/index.html'

    def get(self, request):
        if MainView.authorized:
            return render(request, self.authorized_name)
        else:
            return render(request, self.template_name)

    def post(self, request):
        response = requests.post("http://localhost:8000/api/auth/register", {
            "username": request.POST['username'],
            "password": request.POST['password'],
            "email": request.POST['email'],
        })
        if int(str(response.status_code)[:1]) == 2:
            token = json.loads(response.content.decode('utf-8'))['token']
            MainView.token = token
            MainView.authorized = True
        return self.get(request)
