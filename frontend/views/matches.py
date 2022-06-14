import json

import requests
from django.shortcuts import render, redirect
from django.views import View

from frontend.views.views import MainView


class MatchesView(View):
    template_name = 'frontend/login.html'
    matches_name = 'frontend/matches.html'

    def get(request, tournamentId, stage=None):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token ' + MainView.token}
        if stage is None:
            response = requests.get("http://localhost:8000/api/match?tournamentId="
                                    + tournamentId,
                                    headers=headers)
        else:
            response = requests.get("http://localhost:8000/api/match?tournamentId="
                                    + tournamentId + "&stage=" + stage,
                                    headers=headers)
        matches = json.loads(response.content.decode('utf-8'))
        response = requests.get("http://localhost:8000/api/stage/all?tournamentId=" + tournamentId,
                                headers=headers)
        stages = json.loads(response.content.decode('utf-8'))
        if MainView.authorized:
            return render(request, MatchesView.matches_name, {
                "matches": matches,
                "stages": stages,
                "tournamentId": tournamentId
            })
        else:
            return render(request, MatchesView.template_name)

    def put(request, id):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token ' + MainView.token}
        tournamentId = request.POST['tournamentId']
        data = {
            "id": id,
            "firstTeamScore": request.POST['firstTeamScore'],
            "secondTeamScore": request.POST['secondTeamScore'],
        }
        response = requests.put("http://localhost:8000/api/match", json.dumps(data), headers=headers)
        return redirect("http://localhost:8000/app/tournament/" + tournamentId + "/matches")
