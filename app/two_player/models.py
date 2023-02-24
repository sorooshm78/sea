from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class GameRoomManager(models.Manager):
    def active(self):
        return super().get_queryset().filter(is_active=True)

    def empty_rooms(self):
        return self.active().filter(Q(user1=None) | Q(user2=None))

    def is_user_have_active_room(self, user):
        return self.active().filter(Q(user1=user) | Q(user2=user)).exists()

    def get_user_active_room(self, user):
        return self.active().get(Q(user1=user) | Q(user2=user))

    def create_room(self, user):
        if self.is_user_have_active_room(user):
            return self.get_user_active_room(user)

        room = self.empty_rooms().first()
        if not room:
            return super().create(user1=user, turn=user.username)

        room.user2 = user
        room.save()
        return room


class GameRoomModel(models.Model):
    user1 = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="user1",
    )
    user2 = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="user2",
    )
    is_active = models.BooleanField(default=True)
    turn = models.CharField(max_length=50)

    rooms = GameRoomManager()

    def has_capacity(self):
        if self.user1 is not None and self.user2 is not None:
            return False
        return True

    def change_turn(self):
        if self.turn == self.user1.username:
            self.turn = self.user2.username
        elif self.turn == self.user2.username:
            self.turn = self.user1.username
        self.save()

    def deactivate_game_room(self):
        self.is_active = False
        self.save()
