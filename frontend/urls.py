from django.urls import path

from frontend.views.matches import MatchesView
from frontend.views.register import RegisterView
from frontend.views.stage import StageView
from frontend.views.team import TeamView
from frontend.views.tournament import TournamentView
from frontend.views.views import MainView
from frontend.views.login import LoginView

urlpatterns = [
    path('', MainView().home, name='home'),
    path('login', LoginView().get, name='get'),
    path('logout', LoginView().logout, name='logout'),
    path('register', RegisterView().get, name='get'),
    path('tournament/new', TournamentView().new, name='new'),
    path('tournament/add', TournamentView().post, name='post'),
    path('tournament/all', TournamentView().get, name='get'),
    path('tournament/<tournamentId>/matches/<stage>', MatchesView.get, name='get'),
    path('tournament/<tournamentId>/matches', MatchesView.get, name='get'),
    path('match/put/<id>', MatchesView.put, name='put'),
    path('login/verify', LoginView().post, name='post'),
    path('team', TeamView().get, name='get'),
    path('team/amount', TeamView().declareAmount, name='declareAmount'),
    path('teams', TeamView().post, name='post'),
    path('stage', StageView().get, name='get'),
    path('register/verify', RegisterView().post, name='post')
]
