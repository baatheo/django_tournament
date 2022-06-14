from django.shortcuts import render
from django.views import View


class MainView(View):
    template_name = 'frontend/index.html'
    unauthorized_name = 'frontend/login.html'
    authorized = False
    token = ''

    def home(self, request):
        if self.authorized:
            return render(request, self.template_name, {
                "authorize": self.authorized
            })
        else:
            return render(request, self.unauthorized_name, {
                "authorize": self.authorized
            })
