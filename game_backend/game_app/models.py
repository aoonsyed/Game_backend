from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk or User.objects.get(pk=self.pk).password != self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='scores',to_field='username',db_column='username', primary_key=True)
    high_score = models.IntegerField()
    last_game_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.score}"
    