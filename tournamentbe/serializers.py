from django.core.exceptions import SuspiciousOperation
from django.db.models import Min
from rest_framework import serializers

from tournamentbe.models import Tournament, Match, Team


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'createdDate',)

    def get_tournaments(self, user):
        return self.Meta.model.objects.filter(userId=user)


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('stage', 'firstTeam', 'secondTeam',)

    def findLatestStage(self, tournamentId):
        return self.Meta.model.objects.filter(firstTeam__tournamentId_id=tournamentId).aggregate(Min('stage'))

    def checkIfAllStageMatchesWerePlayed(self, stage, tournamentId):
        matches = self.Meta.model.objects.filter(stage=stage, played=True, firstTeam__tournamentId_id=tournamentId)
        allMatches = self.Meta.model.objects.filter(stage=stage, firstTeam__tournamentId_id=tournamentId)
        return matches.count() == allMatches.count()


class UpdateMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('pk', 'firtsTeamScore', 'secondTeamScore')

    def update_match(self, data):
        if data['firstTeamScore'] == data['secondTeamScore']:
            raise SuspiciousOperation('Invalid score')
        self.Meta.model.objects.filter(id=data['id']).update(firstTeamScore=data['firstTeamScore'],
                                                             secondTeamScore=data['secondTeamScore'],
                                                             played=True)
        saved = self.Meta.model.objects.filter(id=data['id'])[0]
        if saved.firstTeamScore > saved.secondTeamScore:
            looser = saved.secondTeam.id
        else:
            looser = saved.firstTeam.id
        teamSerializer = TeamSerializer()
        teamSerializer.eliminateTeam(team=looser)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'tournamentId',)

    def eliminateTeam(self, team):
        self.Meta.model.objects.filter(id=team).update(status=False)
