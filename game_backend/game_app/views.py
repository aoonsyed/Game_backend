from rest_framework import viewsets,generics
from .models import User,Score
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
            return Score.objects.select_related('user').order_by('-score')
        return super().get_queryset()
    
    def get_object(self):
        username = self.kwargs.get('pk')
        queryset = self.get_queryset()
        try:
            return queryset.get(user__username=username)
        except Score.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound(detail=f"Score not found for username: {username}")