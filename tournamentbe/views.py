import json

from django.core import serializers
from django.db import transaction
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from tournamentbe.models import Match, Team
from tournamentbe.serializers import TournamentSerializer, MatchSerializer, TeamSerializer, UpdateMatchSerializer
from tournamentbe.utils import determineFirstStage, prepareMatches


class TournamentAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = TournamentSerializer

    def get(self, serializer):
        serializer = self.get_serializer()
        tournaments = serializer.get_tournaments(user=self.request.user)
        data = serializers.serialize('json', tournaments)
        return HttpResponse(data, content_type="application/json")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save(userId=request.user)
        return Response({
            "tournaments": TournamentSerializer(saved, context=self.get_serializer_context()).data,
            "id": saved.id
        })


class TeamAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = TeamSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        teams = []
        for team in request.data:
            serializer = TeamSerializer(data=team)
            serializer.is_valid()
            team = serializer.save()
            teams.append(team)
        stage = determineFirstStage(len(teams))
        matchesToSave = prepareMatches(stage, teams)
        matches = []
        for match in matchesToSave:
            serializer = MatchSerializer(data=match)
            serializer.is_valid()
            saved = serializer.save()
            matches.append(saved)
        return Response({
            "message": "matches have been scheduled"
        })


class StageAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        print("begin new stage")
        tournamentId = request.GET.get("tournamentId")
        print(tournamentId)
        serializer = self.get_serializer()
        stage = serializer.findLatestStage(tournamentId)
        print(stage)
        completed = serializer.checkIfAllStageMatchesWerePlayed(stage['stage__min'], tournamentId)
        print(completed)
        if not completed:
            return Response({
                "message": "Stage not completed"
            }, status=status.HTTP_400_BAD_REQUEST)
        if stage['stage__min'] == 1:
            return Response({
                "message": "Tournament is finished"
            }, status=status.HTTP_400_BAD_REQUEST)

        teams = Team.objects.filter(status=True, tournamentId_id=tournamentId)
        print(teams)
        matchesToSave = prepareMatches(stage['stage__min'] / 2, teams)
        print(matchesToSave)
        matches = []
        for match in matchesToSave:
            serializer = MatchSerializer(data=match)
            serializer.is_valid()
            saved = serializer.save()
            matches.append(saved)
        return Response({
            "message": "new stage has been scheduled"
        })


class AllStageAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        tournamentId = request.GET.get("tournamentId")
        stages = Match.objects.filter(firstTeam__tournamentId_id=tournamentId).values('stage').order_by(
            'stage').distinct()
        return Response(stages)


class MatchAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UpdateMatchSerializer

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.update_match(data=request.data)
        return Response({
            "response": "ok"
        })

    def get(self, request, *args, **kwargs):
        tournamentId = request.GET.get("tournamentId")
        if request.GET.get('stage') is not None:
            stage = request.GET.get('stage')
        else:
            stage = MatchSerializer().findLatestStage(tournamentId)
            stage = stage['stage__min']
        print(stage)
        matches = Match.objects.filter(stage=stage, firstTeam__tournamentId_id=tournamentId)
        data = serializers.serialize('json', matches)
        matches = json.loads(data)
        for match in matches:
            firstTeam = Team.objects.filter(id=match['fields']['firstTeam']).values('name')[0]['name']
            match['fields']['firstTeam'] = firstTeam
            secondTeam = Team.objects.filter(id=match['fields']['secondTeam']).values('name')[0]['name']
            match['fields']['secondTeam'] = secondTeam
        return HttpResponse(json.dumps(matches), content_type="application/json")
