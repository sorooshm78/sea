from django.db import models


class GameHistoryModel(models.Model):
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    win = models.CharField(max_length=100, blank=True, null=True)
    left = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player1}-{self.player2}(win:{self.win})(left:{self.left})"
