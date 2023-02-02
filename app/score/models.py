from django.db import models
from django.contrib.auth.models import User


class ScoreBoardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} score is {self.score}"
