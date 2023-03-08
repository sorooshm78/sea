from django.db import models
from django.contrib.auth.models import User


class GameHistoryModel(models.Model):
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player1}-{self.player2} -> {self.status}"
