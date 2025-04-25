from rest_framework import serializers
from .models import User,Score

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    high_score = serializers.IntegerField(source='scores.high_score', read_only=True)
    last_game_score = serializers.IntegerField(source='scores.last_game_score', read_only=True)
    class Meta:
        model= User
        fields = ['id', 'name', 'username', 'password', 'high_score','last_game_score']
        # exclude = ('created_at', 'updated_at',)

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model= Score
        exclude = ('created_at', 'updated_at',)
        extra_kwargs = {
            'high_score': {'read_only': True}
        }

class ScoreboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Score
        fields = ['username', 'high_score']

    def create(self, validated_data):
        user = validated_data.get('user')
        high_score = validated_data.get('high_score')

        score_obj, created = Score.objects.update_or_create(
            user=user,
            defaults={'high_score': high_score}
        )
        return score_obj
