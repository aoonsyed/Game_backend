from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetScoreboard(APIView):
    def get(self, request):
        users = User.objects.all().order_by('-high_score')
        return Response(users.values('user_id', 'high_score'), status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id', 'username', 'last_game_score'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='User ID'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'last_game_score': openapi.Schema(type=openapi.TYPE_INTEGER, description='Last game score')
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'high_score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'last_game_score': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            ),
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'high_score': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'last_game_score': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
        }
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        last_game_score = request.data.get('last_game_score')
        user = User.objects.filter(user_id=user_id).first()
        if user:
            if last_game_score > user.high_score:
                user.high_score = last_game_score
            user.last_game_score = last_game_score
            user.save()
            return Response({"user_id": user.user_id, "last_game_score": user.last_game_score,"high_score": user.high_score}, status=status.HTTP_200_OK)
        else:
            user = User.objects.create(user_id=user_id, username=username, last_game_score=last_game_score, high_score=last_game_score)
            return Response({"user_id": user.user_id, "last_game_score": user.last_game_score,"high_score": user.high_score}, status=status.HTTP_201_CREATED)
    
