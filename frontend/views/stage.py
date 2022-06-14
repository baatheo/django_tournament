import requests
from django.shortcuts import redirect
from django.views import View

from frontend.views.views import MainView


class StageView(View):

    def get(self, request):
        stage = request.POST['stage']
        tournamentId = request.POST['tournamentId']

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token ' + MainView.token}
        response = requests.get("http://localhost:8000/api/stage?tournamentId=" + str(tournamentId), headers=headers)

        if int(str(response.status_code)[:1]) == 2:
            return redirect("http://localhost:8000/app/tournament/" + tournamentId + "/matches" +
                            stage)
        print(response.status_code)