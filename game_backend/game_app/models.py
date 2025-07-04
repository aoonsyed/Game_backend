from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    last_game_score = models.IntegerField(null=True, blank=True)
    high_score = models.IntegerField(null=True, blank=True)
    lives = models.IntegerField()
    pathToGloryLives = models.IntegerField()
    arcticFortuneLives = models.IntegerField()
    investment = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username

class Reward(models.Model):
    wallet_id = models.CharField(unique=True)
    amount = models.FloatField()
    score = models.IntegerField()
    mode = models.CharField()

    def __str__(self):
        return self.wallet_id

class LeaderboardHistory(models.Model):
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    high_score = models.IntegerField()
    last_game_score = models.IntegerField()
    backup_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.high_score}"
