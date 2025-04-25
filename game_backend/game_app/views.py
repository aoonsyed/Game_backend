from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import User, Score
from .serializers import UserSerializer, ScoreboardSerializer, ScoreSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ScoreboardSerializer
        return ScoreSerializer
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Score.objects.select_related('user').order_by('-high_score')
        return super().get_queryset()
    
    def get_object(self):
        username = self.kwargs.get('pk')
        queryset = self.get_queryset()
        try:
            return queryset.get(user__username=username)
        except Score.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound(detail=f"Score not found for username: {username}")

    def create(self, request):
        userID = request.data.get('user')
        user = User.objects.filter(id=userID).first()
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        username = user.username
        last_game_score = request.data.get('last_game_score')

        score_obj = Score.objects.filter(user=user).first()
        if score_obj:
            if last_game_score > score_obj.high_score:
                score_obj.high_score = last_game_score
            score_obj.last_game_score = last_game_score
            score_obj.save()
            return Response({"username": username, "high_score": score_obj.high_score, 'last_game_score': last_game_score},status=status.HTTP_200_OK)
        else:
            score_obj = Score.objects.create(user=user, high_score=last_game_score, last_game_score=last_game_score)
            return Response(
            {"username": username, "high_score": score_obj.high_score, 'last_game_score': last_game_score},
            status=status.HTTP_201_CREATED
            )