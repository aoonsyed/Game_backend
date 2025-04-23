from rest_framework import serializers
from .models import User,Score

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model= Score
        exclude = ('created_at', 'updated_at',)

class ScoreboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Score
        fields = ['username', 'score']

    def create(self, validated_data):
        user = validated_data.get('user')
        score = validated_data.get('score')

        score_obj, created = Score.objects.update_or_create(
            user=user,
            defaults={'score': score}
        )
        return score_obj
