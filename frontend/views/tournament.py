import json

import requests
from django.shortcuts import render, redirect
from django.views import View

from frontend.views.views import MainView


class TournamentView(View):
    template_name = 'frontend/login.html'
    new_tournament_name = 'frontend/new-tournament.html'
    get_tournament_name = 'frontend/tournament-view.html'

    def new(self, request):
        if MainView.authorized:
            return render(request, self.new_tournament_name)
        else:
            return render(request, self.template_name)

    def get(self, request):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token ' + MainView.token}
        response = requests.get("http://localhost:8000/api/tournament",
                                headers=headers)
        tournaments = json.loads(response.content.decode('utf-8'))
        if MainView.authorized:
            return render(request, self.get_tournament_name, {
                "tournaments": tournaments
            })
        else:
            return render(request, self.template_name)

    def post(self, request):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token ' + MainView.token}
        data = json.dumps({
            "name": request.POST['name'],
        })
        response = requests.post("http://localhost:8000/api/tournament",
                                 data, headers=headers)
        if int(str(response.status_code)[:1]) == 2:
            tournament = json.loads(response.content.decode('utf-8'))
            print(tournament)
            print(tournament['id'])
            print("http://localhost:8000/app/team?tournamentId=" + str(tournament['id']))
            return redirect("http://localhost:8000/app/team?tournamentId=" + str(tournament['id']))
