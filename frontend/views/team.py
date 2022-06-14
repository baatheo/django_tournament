import json

import requests
from django.shortcuts import render, redirect
from django.views import View

from frontend.views.views import MainView


class TeamView(View):
    template_name = 'frontend/login.html'
    amount_of_teams_name = 'frontend/add-teams.html'

    known_amount = False
    amount = []

    def get(self, request, tournamentId=None):
        if request.method == 'GET':
            tournamentId = request.GET.get('tournamentId')
        if MainView.authorized:
            return render(request, self.amount_of_teams_name, {
                "known_amount": self.known_amount,
                "amount": self.amount,
                "tournamentId": tournamentId
            })
        else:
            return render(request, self.template_name)

    def declareAmount(self, request):
        amount = request.POST['amount']
        self.known_amount = True
        self.amount = [None] * int(amount)
        return self.get(request, tournamentId=request.POST['tournamentId'])

    def post(self, request):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token ' + MainView.token}
        amount = request.POST['amount']
        tournamentId = request.POST['tournamentId']
        amount = len(amount.split())
        teams = []
        for index in range(amount):
            teamName = request.POST['{}'.format(index + 1)]
            team = {
                "name": teamName,
                "tournamentId": tournamentId
            }
            teams.append(team)
        print(teams)
        response = requests.post("http://localhost:8000/api/team", json.dumps(teams),
                                 headers=headers)

        if int(str(response.status_code)[:1]) == 2:
            return redirect("http://localhost:8000/app/tournament/" + str(tournamentId) + "/matches")
