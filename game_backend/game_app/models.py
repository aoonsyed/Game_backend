from django.db import models
from django.core.validators import MaxValueValidator

class User(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    last_game_score = models.IntegerField(null=True, blank=True)
    high_score = models.IntegerField(null=True, blank=True)
    lives = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username

    