from rest_framework import serializers
from .models import LeaderboardHistory

class LeaderboardHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderboardHistory
        fields = ['user_id', 'username', 'high_score', 'last_game_score', 'backup_time']
