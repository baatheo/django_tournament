from django.urls import path

from .views import TournamentAPI, TeamAPI, MatchAPI, StageAPI, AllStageAPI

urlpatterns = [
    path('tournament', TournamentAPI.as_view()),
    path('team', TeamAPI.as_view()),
    path('match', MatchAPI.as_view()),
    path('stage', StageAPI.as_view()),
    path('stage/all', AllStageAPI.as_view())
]
