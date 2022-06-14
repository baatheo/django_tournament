from django.db import models
from knox.models import User


class Tournament(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    createdDate = models.DateField(auto_now=True)


class Team(models.Model):
    name = models.CharField(db_column='name', max_length=40, null=False)
    tournamentId = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(default=True)


class Match(models.Model):
    stage = models.PositiveIntegerField(null=False)  # 8 - 1/8, 4 - 1/4, 2 - 1/2, 1 - finał
    # myślę że nie ma sensu tworzenia osobnej tabela z etapami ponieważ,
    # indeksowanie po tym polu będzie tak samo szybkie jak po foreign key.
    firstTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='firstTeam')
    secondTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='secondTeam')
    firstTeamScore = models.PositiveIntegerField(null=True)
    secondTeamScore = models.PositiveIntegerField(null=True)
    played = models.BooleanField(default=False)


